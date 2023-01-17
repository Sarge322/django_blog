from django.db.models import Count

from blog_theme.models import Category


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('blog_theme'))
        print(cats)
        context['cats'] = cats
        # if not self.request.user.is_authentificated:
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
