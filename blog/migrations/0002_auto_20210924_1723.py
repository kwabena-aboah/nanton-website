# Generated by Django 3.2.6 on 2021-09-24 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categories',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='postcomment',
            options={'verbose_name': 'Comment', 'verbose_name_plural': 'Comments'},
        ),
    ]
