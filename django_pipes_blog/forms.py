from django.forms import ModelForm, inlineformset_factory

from .models import Post, TextBlock, PostImage

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'published', 'tags']


class TextBlockForm(ModelForm):
    class Meta:
        model = TextBlock
        fields = ['text', 'block_title']

TextBlockFormSet = inlineformset_factory(Post, TextBlock, form=TextBlockForm, extra=1)
