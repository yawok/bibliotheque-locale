# Generated by Django 4.1.3 on 2022-11-17 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_marked_returnsed', 'Set book as returned'),)},
        ),
    ]