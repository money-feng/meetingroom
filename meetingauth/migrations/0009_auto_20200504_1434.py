# Generated by Django 3.0.4 on 2020-05-04 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meetingauth', '0008_auto_20200503_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menulist',
            name='path',
            field=models.CharField(blank=True, default='', max_length=20, null=True, verbose_name='路由'),
        ),
    ]
