# Generated by Django 5.2.1 on 2025-05-31 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_unit_user_alter_task_status_alter_task_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=256),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField(max_length=256)),
                ('tasks', models.ManyToManyField(blank=True, to='main.task')),
                ('unit', models.ManyToManyField(blank=True, to='main.unit')),
            ],
        ),
    ]
