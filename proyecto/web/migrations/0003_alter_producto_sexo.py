# Generated by Django 3.2 on 2023-12-01 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_producto_sexo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='sexo',
            field=models.CharField(choices=[('c', 'children'), ('m', 'women'), ('h', 'men')], default='5', max_length=1),
        ),
    ]
