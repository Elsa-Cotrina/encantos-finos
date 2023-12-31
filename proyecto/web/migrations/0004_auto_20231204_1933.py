# Generated by Django 3.2 on 2023-12-05 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_alter_producto_sexo'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='dimensiones',
            field=models.CharField(default='30 x 10 cm', max_length=100),
        ),
        migrations.AddField(
            model_name='producto',
            name='pais',
            field=models.CharField(default='Perú', editable=False, max_length=100),
        ),
        migrations.AddField(
            model_name='producto',
            name='peso',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='producto',
            name='sexo',
            field=models.CharField(choices=[('c', 'children'), ('h', 'men'), ('m', 'women')], default='5', max_length=1),
        ),
    ]
