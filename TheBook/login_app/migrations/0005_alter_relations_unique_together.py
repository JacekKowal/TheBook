# Generated by Django 4.1.1 on 2022-10-21 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0004_alter_relations_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='relations',
            unique_together=set(),
        ),
    ]
