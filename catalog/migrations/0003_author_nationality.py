# Generated by Django 4.1.3 on 2022-11-03 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_nationality_alter_author_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='nationality',
            field=models.ManyToManyField(help_text="Select author's nationality", to='catalog.nationality'),
        ),
    ]