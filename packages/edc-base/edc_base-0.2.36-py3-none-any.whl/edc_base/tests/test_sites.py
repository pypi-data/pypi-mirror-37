from django.contrib.sites.models import Site
from django.test import TestCase, tag
from django.test.utils import override_settings

from .models import TestModelWithSite
from .site_test_case_mixin import SiteTestCaseMixin


class TestSites(SiteTestCaseMixin, TestCase):

    @override_settings(SITE_ID=20)
    def test_20(self):
        obj = TestModelWithSite.objects.create()
        self.assertEqual(obj.site.pk, 20)
        self.assertEqual(obj.site.pk, Site.objects.get_current().pk)

    @override_settings(SITE_ID=30)
    def test_30(self):
        obj = TestModelWithSite.objects.create()
        self.assertEqual(obj.site.pk, 30)
        self.assertEqual(obj.site.pk, Site.objects.get_current().pk)

    @override_settings(SITE_ID=30)
    def test_override_current(self):
        site = Site.objects.get(pk=40)
        obj = TestModelWithSite.objects.create(site=site)
        self.assertEqual(obj.site.pk, 40)
        self.assertNotEqual(obj.site.pk, Site.objects.get_current().pk)
