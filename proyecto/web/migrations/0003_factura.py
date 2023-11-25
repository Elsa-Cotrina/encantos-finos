# Generated by Django 3.2 on 2023-11-25 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20231123_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('nro_factura', models.DecimalField(decimal_places=0, max_digits=5)),
                ('monto_total', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('estado', models.CharField(choices=[('$', 'SOLICITADO'), ('p', 'PAGADO')], default='5', max_length=1)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.cliente')),
            ],
            options={
                'db_table': 'tbl_factura',
            },
        ),
    ]