from .models import About


def get_about():
    try:
        return About.objects.all()[0]
    except IndexError:
        return None
