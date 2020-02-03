# Generated by Django 3.0.2 on 2020-02-02 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('paging', '0001_initial'),
        ('accounting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.TextField(verbose_name='متن')),
                ('author', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='author', to='accounting.Account', verbose_name='author')),
                ('page', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='paging.Page')),
                ('parent_tweet', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='comment', to='twitting.Tweet')),
            ],
        ),
    ]