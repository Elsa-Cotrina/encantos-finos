# Generated by Django 3.2 on 2023-12-05 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20231204_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='matrial',
        ),
        migrations.AddField(
            model_name='producto',
            name='material',
            field=models.CharField(choices=[('p', 'plata'), ('c', 'cobre'), ('o', 'oro')], default='o', max_length=1),
        ),
    ]
