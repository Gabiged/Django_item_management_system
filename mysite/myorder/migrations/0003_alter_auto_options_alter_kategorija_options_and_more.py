# Generated by Django 4.1.2 on 2022-10-08 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myorder', '0002_alter_uzsakymoeilute_auto_item'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auto',
            options={'verbose_name_plural': 'Automobilis'},
        ),
        migrations.AlterModelOptions(
            name='kategorija',
            options={'verbose_name_plural': 'Kategorijos'},
        ),
        migrations.AlterModelOptions(
            name='likutis',
            options={'verbose_name_plural': 'Likučiai'},
        ),
        migrations.AlterModelOptions(
            name='uzsakymas',
            options={'ordering': ['due_back'], 'verbose_name_plural': 'Užsakymas'},
        ),
        migrations.AlterModelOptions(
            name='uzsakymoeilute',
            options={'verbose_name_plural': 'Užsakymo eilutė'},
        ),
    ]
