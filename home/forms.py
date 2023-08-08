from django import forms
from mdeditor.fields import MDTextFormField
from .models import Post

class PostUploadForm(forms.Form):
    title = forms.CharField(max_length=100)
    post_image = forms.ImageField()
    content = MDTextFormField()
    tech_stack = forms.ChoiceField(
        choices=(('HTML & CSS', 'HTML & CSS'), ('HTML, CSS & Javascript', 'HTML, CSS & Javascript'), ('Flutter', 'Flutter'), ('React', 'React')),
    )

class PostUploadModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'post_image', 'content', 'tech_stack')
