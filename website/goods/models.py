from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=10)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    CATEROGIES = (
        ("men's", "Men's"),
        ("women's", "Women's"),
        ("children's", "Children's"),
    )
    CITY = (
        ("Минск", "минск"),
        ("Брест", "брест"),
        ("Гродно", "гродно"),
        ("Гомель", "гомель"),
        ("Витебск", "витебск"),
        ("Могилев", "могилев")
    )
    author = models.ForeignKey(User, null=True, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(blank=True, max_length=100)
    category = models.CharField(max_length=10, choices=CATEROGIES)
    description = models.TextField(max_length=400)
    image = models.FileField(upload_to='img/')
    publish = models.DateTimeField(default=timezone.now)
    date = models.DateField(null=True, auto_now_add="True")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    phone = models.CharField(blank=True, max_length=100)
    city = models.CharField(max_length=10, choices=CITY, default='')
    categories = models.ManyToManyField("Category", related_name='posts')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author_name = models.CharField(blank=True, max_length=50)
    text = models.TextField(max_length=200)

    def __str__(self):
        return self.author_name

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
