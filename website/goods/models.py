from django.db import models


class Post(models.Model):
    post_title = models.CharField(blank=True, max_length=100)
    post_description = models.TextField(max_length=400)
    post_image = models.FileField(upload_to='img/')
    post_date = models.DateField(null=True, auto_now_add="True")

    def __str__(self):
        return self.post_title

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
        verbose_name_plural = 'Коментарии'
