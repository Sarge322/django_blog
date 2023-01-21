from django.core.cache import cache
from django.db.models import Count

from blog_theme.models import Category


class DataMixin:
    paginate_by = 20

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('blog_theme'))
            cache.set('cats', cats, 60)
        print(cats)
        context['cats'] = cats
        # if not self.request.user.is_authentificated:
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
