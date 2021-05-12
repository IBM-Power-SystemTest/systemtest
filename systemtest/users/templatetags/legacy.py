"""
Custom Django TemplaTags for Users templates,
template tags to handle browser
    References:
        https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/
"""

from django.template import Library

register = Library()


@register.filter("is_legacy")
def is_legacy(user_agent: str) -> bool:
    """
    Process the Django HttpRequest.headers['user-agent'] which is the same
    that request.META['HTTP_USER_AGENT'] to gets the browser and the
    version if the user agent is from firefox version less or equal than
    33 return True ( is a legacy browser )
        References:
            https://docs.djangoproject.com/en/3.1/ref/request-response/#attributes

    Args:
        user_agent:
            Str returned by request.META.HTTP_USER_AGENT or request.headers.user_agent

    Returns:
        True or False depends of the criteria for 'legacy'
    """

    # user_agent format: 'Mozilla/5.0 (X11; U; AIX 7.2; zh-TW; rv:1.8.1.11) Gecko/20080724 Firefox/2.0.0.11'
    # Get format like: ['Firefox', '2.0.0.11']
    browser, version = user_agent.split()[-1].split('/')

    # Only neeed the main version '2.0.0.11' -> 2
    version = int(version.split(".")[0])
    browser = str.lower(browser)

    return True if browser == "firefox" and version <= 33 else False
