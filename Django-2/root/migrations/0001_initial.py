# Generated by Django 4.2 on 2025-03-03 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years_experience', models.PositiveIntegerField(default=0)),
                ('projects_completed', models.PositiveIntegerField(default=0)),
                ('happy_clients', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
