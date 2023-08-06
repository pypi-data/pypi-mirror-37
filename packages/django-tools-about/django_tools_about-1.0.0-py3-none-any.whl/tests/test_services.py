from django.test import TestCase
from djtools.about.services import get_about
from djtools.about.models import About


class ServicesTestCase(TestCase):
    def test_get_about(self):
        about = get_about()
        assert about is None

        first_about = About.objects.create(title="first")
        about = get_about()
        assert about == first_about

        About.objects.create(title="second")
        about = get_about()
        assert about == first_about
