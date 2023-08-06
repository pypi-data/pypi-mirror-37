from django.views.generic import TemplateView

from .services import get_about


class AboutView(TemplateView):
    template_name = "about/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['about'] = get_about()
        return context
