# Generated by Django 4.1.1 on 2022-10-21 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0003_relations'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relations',
            unique_together={('initiator', 'receiver')},
        ),
    ]
