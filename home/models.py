from django.db import models
from django_resized import ResizedImageField
from mdeditor.fields import MDTextField
from django.db.models.signals import pre_save
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.dispatch import receiver


def postImagePath(instance, filename):
    ext = str(filename).split(".")[-1]
    return f'images/{instance.title}.{ext}'


def profileImagePath(_, filename):
    return f'profile/{filename}'


from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    profile_picture = ResizedImageField(size=[300, 300], crop=['middle', 'center'], upload_to=profileImagePath, null=True, blank=True)
    social_profile_picture = models.CharField(max_length=256, blank=True, null=True)
    buymeacoffee = models.CharField(max_length=55, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.pk}. {self.email} ({self.username})"


class Post(models.Model):
    title = models.CharField(max_length=100, null=False)
    post_image = models.ImageField(upload_to=postImagePath)
    url = models.SlugField(unique=True, blank=True)
    content = MDTextField(null=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    tech_stack = models.CharField(
        max_length=22, 
        choices=(('HTML & CSS', 'HTML & CSS'), ('HTML, CSS & Javascript', 'HTML, CSS & Javascript'), ('Flutter', 'Flutter'), ('React', 'React')), 
    )
    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField('User', related_name='liked_posts', blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

@receiver(pre_save, sender=Post)
def set_post(sender, instance, *args, **kwargs):
    if not instance.pk:
        instance.views = 0
    if not instance.url:
        instance.url = slugify(instance.title)
        found_posts = Post.objects.filter(url__startswith=instance.url)
        if(found_posts):
            instance.url += f'-{len(found_posts) + 1}'


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, null=True, default=None)
    message_type = models.CharField(
        max_length=15,
        choices=(('Feature Request', 'Feature Request'), ('Questions', 'Questions'), ('Suggestion', 'Suggestion'), ('Bug Reports', 'Bug Reports'), ('Comments', 'Comments'), ('Other', 'Other'))
    )
    message = models.TextField(max_length=100)
    datetime = models.DateTimeField(auto_now_add=True)