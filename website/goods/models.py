from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Category(MPTTModel):
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

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    CURRENCY = (
        ('BYN', 'BYN'),
        ('DOLL', 'DOLL'),
        ('EURO', 'EURO')
    )

    CITY = (
        ("Минск", "Минск"),
        ("Брест", "Брест"),
        ("Гродно", 'Гродно'),
        ("Гомель", "Гомель"),
        ("Витебск", "Витебск"),
        ("Могилев", "Могилев"),
    )
    author = models.ForeignKey(User, null=True, related_name='posts', on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(blank=True, max_length=100, verbose_name='Тема')
    slug = models.SlugField(max_length=255, unique=False, default=None, verbose_name="URL")
    category = TreeForeignKey("Category", related_name='category', null=True, on_delete=models.CASCADE,
                              verbose_name='Категория')
    description = models.TextField(max_length=400, verbose_name='Описание')
    image = models.ImageField(upload_to='img/', verbose_name='Изображение', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    phone = models.CharField(blank=True, max_length=100, verbose_name='Контактный номер')
    city = models.CharField(max_length=10, choices=CITY, default='', verbose_name='Город')
    price = models.IntegerField(default=0)
    currency = models.CharField(max_length=10, choices=CURRENCY, default='BYN')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_on']


class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_on']


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    avatar = models.ImageField("Аватар", upload_to="profile/", blank=True, null=True)
    email_two = models.EmailField("Доп. email")
    phone = models.CharField("Телефон", max_length=25)
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50, blank=True, null=True)
    slug = models.SlugField("URL", max_length=50, default='')

    def str(self):
        return self.first_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = "{}{}".format(self.user_id, self.first_name)

    # def get_absolute_url(self):
    #     return reverse("profile-detail", kwargs={"slug": self.user.username})

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профиля"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя при регистрации"""
    if created:
        Profile.objects.create(user=instance)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()