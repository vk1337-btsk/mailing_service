from django.forms import ModelForm
from core.forms import StyleFormMixin
from apps.blog.models import Articles


class ArticleForm(StyleFormMixin, ModelForm):

    class Meta:
        model = Articles
        fields = ('title', 'text', 'is_published')
