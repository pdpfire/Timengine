# Generated by Django 4.2.23 on 2025-07-08 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DiaryEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('strtime', models.DateTimeField()),
                ('title', models.CharField(max_length=200)),
                ('tasktime', models.CharField(max_length=100)),
                ('taskdetails', models.TextField()),
                ('detailtime', models.CharField(max_length=100)),
                ('endtime', models.DateTimeField()),
            ],
            options={
                'db_table': 'diaryapp',
            },
        ),
    ]
