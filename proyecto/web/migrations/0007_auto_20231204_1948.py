# Generated by Django 3.2 on 2023-12-05 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_auto_20231204_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='estado',
            field=models.CharField(choices=[('s', 'SOLICITADO'), ('p', 'PAGADO')], default='s', max_length=1),
        ),
        migrations.AlterField(
            model_name='producto',
            name='matrial',
            field=models.CharField(choices=[('o', 'oro'), ('c', 'cobre'), ('p', 'plata')], default='o', max_length=1),
        ),
        migrations.AlterField(
            model_name='producto',
            name='sexo',
            field=models.CharField(choices=[('h', 'men'), ('c', 'children'), ('m', 'women')], default='m', max_length=1),
        ),
    ]
