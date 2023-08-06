from importlib import import_module

from typing import List
from codemirror2.widgets import AdminCodeMirrorEditor

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.handlers.wsgi import WSGIRequest

__all__ = (
    'get_protocol',
    'get_domain',
    'to_list',
    'to_str',
    'default_language',
    'get_html_field_widget',
)


def get_protocol() -> str:
    """
    Returns data transfer protocol name.
    The value is determined by bool variable 'USE_HTTPS' in settings.

    Returns:
        str: 'https' if 'USE_HTTPS' is True, otherwise - 'http'.
    """

    return 'https' if getattr(settings, 'USE_HTTPS', False) else 'http'


def get_domain(request: WSGIRequest=None) -> str:
    """
    Returns domain name this site.

    Args:
        request (WSGIRequest): Request.

    Returns:
        str: Domain name.
    """

    site_name = Site.objects.get_current(request).domain

    return site_name


def to_list(string: str) -> List[str]:
    """
    Transforms string to list.

    Args:
        string (str): String to transform.

    Returns:
        List[str]: List
    """

    return string.split(',')


def to_str(_list: List[str]) -> str:
    """
    Transforms list to str.

    Args:
        _list (List[str]): List to transform to str

    Returns:
        str: Transformed list
    """

    return ','.join(_list)


def default_language() -> str:
    """
    Returns default site language.

    Returns:
        str: Default site language
    """
    if hasattr(settings, 'PARLER_LANGUAGES') and settings.PARLER_LANGUAGES:
        return (
            settings.PARLER_LANGUAGES.get('default', {}).get('fallback')
        )
    else:
        return settings.LANGUAGE_CODE


def get_html_field_widget() ->object:
    """
    Get custom widget from settings

    Returns:
        object: HTML field widget
    """
    if hasattr(settings, 'POSTIE_HTML_ADMIN_WIDGET') and settings.POSTIE_HTML_ADMIN_WIDGET:
        custom_widget = getattr(
            import_module(settings.POSTIE_HTML_ADMIN_WIDGET['widget_module']),
            settings.POSTIE_HTML_ADMIN_WIDGET['widget']
        )
        return custom_widget(**settings.POSTIE_HTML_ADMIN_WIDGET.get('attrs', {}))

    return AdminCodeMirrorEditor(
        modes=['css', 'xml', 'javascript', 'htmlmixed']
    )
