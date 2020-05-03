# Generated by Django 3.0.4 on 2020-05-03 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meetingauth', '0003_auto_20200503_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menulist',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parentlevel', to='meetingauth.MenuList', verbose_name='上级菜单'),
        ),
    ]
