from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = "templates/about/author.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['just_title'] = 'Привет, меня зовут Дмитрий Волков)'
        context['just_text'] = 'Эта страничка обо мне'
        context['just_text_2'] = ('учусь программировать,',
                                  'маленькими шагами иду в необъятный мир',)
        return context


class AboutTechView(TemplateView):
    template_name = "templates/about/tech.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
