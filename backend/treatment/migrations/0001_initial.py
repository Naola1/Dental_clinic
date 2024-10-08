# Generated by Django 5.1 on 2024-09-10 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TreatmentHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('treatment_date', models.DateField(auto_now_add=True)),
                ('description', models.TextField()),
                ('follow_up_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-treatment_date'],
            },
        ),
    ]
