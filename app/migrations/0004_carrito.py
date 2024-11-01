# Generated by Django 5.1 on 2024-10-30 05:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_carritoingrediente_carrito_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('carrito_id', models.AutoField(primary_key=True, serialize=False)),
                ('precio_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hora_de_creacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.usuario')),
            ],
        ),
    ]
