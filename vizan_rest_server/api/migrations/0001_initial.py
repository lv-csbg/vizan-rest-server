# Generated by Django 2.2 on 2019-04-18 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.TextField()),
                ('svg', models.TextField()),
                ('analysis_type', models.CharField(choices=[('FBA', 'FLUX BALANCE ANALYSIS'), ('FVA', 'FLUX VARIABILITY ANALYSIS')], default='FBA', max_length=3)),
            ],
            options={
                'ordering': ('model',),
            },
        ),
    ]