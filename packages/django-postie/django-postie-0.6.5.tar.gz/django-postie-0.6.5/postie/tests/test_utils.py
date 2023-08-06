from ckeditor.widgets import CKEditorWidget
from codemirror2.widgets import AdminCodeMirrorEditor
from django.test import TestCase
from django.conf import settings
from django.core.cache import cache

from ..utils import get_domain, get_protocol, default_language, get_html_field_widget

__all__ = (
    'UtilsTestCase',
)

class UtilsTestCase(TestCase):
    def test_get_domain(self):
        site_name = get_domain()
        self.assertEqual(site_name, 'example.com')

    def test_get_protocol(self):
        self.assertEqual(get_protocol(), 'http')

        with self.settings(USE_HTTPS=True):
            self.assertEqual(get_protocol(), 'https')

    def test_default_language(self):
        # No parler settings
        with self.settings(PARLER_LANGUAGES={}):
            self.assertEqual(default_language(), settings.LANGUAGE_CODE)

        # With parler settings
        with self.settings(PARLER_LANGUAGES={'default': {'fallback': 'ru',}}):
            self.assertEqual(default_language(), 'ru')

    def test_get_html_field_widget(self):
        # No custom widget settings
        with self.settings(POSTIE_HTML_ADMIN_WIDGET={}):
            self.assertTrue(isinstance(get_html_field_widget(), AdminCodeMirrorEditor))

        # With custom widget settings
        with self.settings(POSTIE_HTML_ADMIN_WIDGET={
            'widget_module': 'ckeditor.widgets', 'widget': 'CKEditorWidget'
        }):
            self.assertTrue(isinstance(get_html_field_widget(), CKEditorWidget))
