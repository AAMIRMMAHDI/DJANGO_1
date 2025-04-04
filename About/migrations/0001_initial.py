# Generated by Django 4.2 on 2025-03-24 18:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PAGE_NAME', models.CharField(default='test', max_length=100)),
                ('A_LITTLE_ABOUT_US', models.CharField(default='test', max_length=100)),
                ('CREATOR_NAME', models.CharField(default='test', max_length=100)),
                ('ROLE', models.CharField(default='test', max_length=100)),
                ('EMAIL', models.CharField(default='test', max_length=100)),
                ('SERVICES', models.CharField(default='test', max_length=100)),
                ('INTERESTS', models.CharField(default='test', max_length=100)),
                ('ONLINE_PRESENTATION', models.CharField(default='test', max_length=100)),
                ('WORK_HISTORY', models.CharField(default='test', max_length=100)),
                ('DESCRIPTION', models.TextField(default='test')),
                ('scheduled', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان')),
                ('percentage', models.IntegerField(help_text='عدد بین 0 تا 100', verbose_name='درصد')),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('happy_clients', models.IntegerField(default=0)),
                ('projects', models.IntegerField(default=0)),
                ('hours_of_support', models.IntegerField(default=0)),
                ('hard_workers', models.IntegerField(default=0)),
            ],
        ),
    ]
