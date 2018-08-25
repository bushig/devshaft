# Generated by Django 2.0.6 on 2018-08-24 23:10

import apps.assets.utils
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import image_cropping.fields
import mptt.fields
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('languages', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('frameworks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=5000)),
                ('repository', models.URLField(blank=True, max_length=300, null=True)),
                ('site', models.URLField(blank=True, max_length=300, null=True)),
                ('repo_stars', models.IntegerField(blank=True, null=True, verbose_name='Stars')),
                ('repo_forks', models.IntegerField(blank=True, null=True, verbose_name='Repo forks')),
                ('repo_description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Repo description')),
                ('repo_updated', models.DateTimeField(blank=True, null=True)),
                ('commits', models.CharField(blank=True, max_length=500, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('asset_type', models.PositiveSmallIntegerField(choices=[(0, 'Github releases'), (1, 'Versions'), (2, 'Link')])),
                ('github_releases', models.BooleanField(default=False)),
                ('changelog', models.BooleanField(default=False)),
                ('locked', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'entries',
                'ordering': ['-updated'],
            },
        ),
        migrations.CreateModel(
            name='AssetImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', image_cropping.fields.ImageCropField(blank=True, upload_to='uploaded_images')),
                ('cropping', image_cropping.fields.ImageRatioField('image', '300x300', adapt_rotation=False, allow_fullsize=False, free_crop=False, help_text=None, hide_image_field=False, size_warning=False, verbose_name='cropping')),
                ('order', models.IntegerField(default=10, verbose_name='Display order')),
                ('entry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Asset')),
            ],
            options={
                'ordering': ['-order'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='assets.Category')),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Release',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=25)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date of this release')),
                ('changelog', models.TextField(blank=True, max_length=10000)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='releases', to='assets.Asset')),
            ],
            options={
                'verbose_name_plural': 'version history',
                'ordering': ('-timestamp',),
                'get_latest_by': 'timestamp',
            },
        ),
        migrations.CreateModel(
            name='ReleaseUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to=apps.assets.utils.version_filename_save)),
                ('release', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploads', to='assets.Release')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='category',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.Category'),
        ),
        migrations.AddField(
            model_name='asset',
            name='frameworks',
            field=models.ManyToManyField(blank=True, related_name='assets', to='frameworks.Framework'),
        ),
        migrations.AddField(
            model_name='asset',
            name='languages',
            field=models.ManyToManyField(blank=True, related_name='assets', to='languages.Language'),
        ),
        migrations.AddField(
            model_name='asset',
            name='license',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.License'),
        ),
        migrations.AddField(
            model_name='asset',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asset',
            name='users_liked',
            field=models.ManyToManyField(blank=True, related_name='entry_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
