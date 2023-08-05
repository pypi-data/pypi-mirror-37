from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from .models import Tag


class TagUnsubscribeView(TemplateView):
    template_name = 'email/tag.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(
            **kwargs
        )

        context['tag'] = get_object_or_404(
            Tag,
            hash=self.kwargs['hash']
        )

        return context
