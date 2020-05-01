# Generated by Django 3.0.4 on 2020-05-01 12:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetingauth', '0004_auto_20200501_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department_parent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='meetingauth.Department', verbose_name='上级部门'),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_sequence',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='排序'),
        ),
    ]
