import mptt
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
    """Категории объявлений"""
    name = models.CharField("Имя", max_length=50, unique=True)
    ordering = ('tree_id', 'level')
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Родитель"
    )
    slug = models.SlugField("url", max_length=50, unique=True)

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


mptt.register(Category, order_insertion_by=['name'])


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    CITY = (
        ("Минск", "Минск"),
        ("Брест", "Брест"),
        ("Гродно", 'Гродно'),
        ("Гомель", "Гомель"),
        ("Витебск", "Витебск"),
        ("Могилев", "Могилев"),
    )
    author = models.ForeignKey(User, null=True, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=100)
    slug = models.SlugField(max_length=255, unique=False, default=None, verbose_name="URL")
    description = models.TextField(max_length=400)
    image = models.ImageField(upload_to='img/goods')
    publish = models.DateTimeField(default=timezone.now)
    date = models.DateField(null=True, auto_now_add="True")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    phone = models.CharField(blank=True, max_length=100)
    city = models.CharField(max_length=10, choices=CITY, default='')
    category = TreeForeignKey("Category", related_name='category', null=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_absolute_url(self):
        return reverse('post', kwargs={'id': self.id, 'title': self.title})

    # def image_img(self):
    #     if self.image:
    #         return u'<a href ='0''

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_name = models.CharField(blank=True, max_length=50)
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
