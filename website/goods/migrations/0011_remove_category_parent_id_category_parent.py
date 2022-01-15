# Generated by Django 4.0.1 on 2022-01-15 16:38

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_alter_category_options_remove_category_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_id',
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='goods.category', verbose_name='Родитель'),
        ),
    ]
