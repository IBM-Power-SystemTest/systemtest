from django.template import Library

register = Library()


@register.filter("is_legacy")
def is_legacy(user_agent) -> bool:
    browser, version = user_agent.split()[-1].split('/')
    version = int(version.split(".")[0])
    browser = str.lower(browser)

    return True if browser == "firefox" and version <= 3 else False
