# Generated by Django 2.2.5 on 2019-12-03 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='last_read_message',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chats.Message'),
        ),
    ]
