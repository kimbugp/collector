# Generated by Django 2.1.1 on 2019-04-29 18:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['date_created']},
        ),
    ]
