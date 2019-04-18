# Generated by Django 2.2 on 2019-04-18 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.FileField(upload_to='')),
                ('svg', models.FileField(upload_to='')),
                ('analysis_type', models.CharField(choices=[('FBA', 'FLUX BALANCE ANALYSIS'), ('FVA', 'FLUX VARIABILITY ANALYSIS')], default='FBA', max_length=3)),
            ],
            options={
                'ordering': ('model',),
            },
        ),
    ]
