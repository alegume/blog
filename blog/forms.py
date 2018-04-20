from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Post, Comment, Reuniao

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text', 'tags', )
        widgets = {
            'tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'tags',                   
            }),
        }
        labels = {
            'title': _('Título'),
            'text': _('Texto'),
        }
        help_texts = {
            'title': _('Coloque o titulo, uai.'),
            'text': _('Coloque o textículo =).'),
            'tags': _('Selecione uma ou mais tags.'),
        }

        
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text', )

class ReuniaoForm(forms.ModelForm):

    class Meta:
        model = Reuniao
        fields = ('assunto', 'data', 'presenca', )
        attrs = ({'class': 'selectpicker'})
        widgets = {
            'presenca': forms.SelectMultiple(attrs={'class': 'selectpicker show-tick'}),
        }
            

class ContatoForm(forms.Form):

    emissor = forms.EmailField(required=True)
    assunto = forms.CharField(required=True)
    msg = forms.CharField(widget=forms.Textarea)
        