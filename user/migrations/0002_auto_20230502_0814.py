# Generated by Django 2.2 on 2023-05-02 08:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangePassword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_password', models.CharField(max_length=50)),
                ('confirm_new_password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ChangePasswordCode',
            fields=[
                ('user_email', models.EmailField(max_length=50)),
                ('user_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Whatsapp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default='0', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='pair',
            field=models.CharField(default='USD', max_length=50),
        ),
    ]
