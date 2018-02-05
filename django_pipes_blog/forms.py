from django.forms import ModelForm, inlineformset_factory, Textarea
from django.utils.translation import gettext_lazy

from .models import Post, TextBlock, PostImage

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'published', 'tags']
        widgets = {
            'tags': Textarea(attrs={'rows': 3}),
        }
        help_texts = {
            'tags': gettext_lazy('Space seperated list of tags relevant to the post.'),
        }


class TextBlockForm(ModelForm):
    class Meta:
        model = TextBlock
        fields = ['block_title', 'text']
        widgets = {
            'text': Textarea(attrs={'rows': 20}),
        }

TextBlockFormSet = inlineformset_factory(Post, TextBlock, form=TextBlockForm, extra=1)
