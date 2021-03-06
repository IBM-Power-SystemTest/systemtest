from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

class TemplateView(LoginRequiredMixin, TemplateView):
    pass

urlpatterns = [
    path(
        route="",
        view=TemplateView.as_view(template_name="pages/home.html"),
        name="home"
    ),
    path(
        route="about/",
        view=TemplateView.as_view(template_name="pages/about.html"),
        name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(
        route=settings.ADMIN_URL,
        view=admin.site.urls
    ),
    path(
        route="users/",
        view=include("systemtest.users.urls", namespace="users")
    ),
    path(
        route="pts/",
        view=include("systemtest.pts.urls", namespace="pts")
    ),
    path(
        route="quality/",
        view=include("systemtest.quality.urls", namespace="quality")
    ),
    path(
        route="people/",
        view=include("systemtest.people.urls", namespace="people")
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            route="400/",
            view=default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            route="403/",
            view=default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            route="404/",
            view=default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path(
            route="500/",
            view=default_views.server_error
        ),
    ]

    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [
            path(
                route="__debug__/",
                view=include(debug_toolbar.urls)
            )
        ] + urlpatterns
