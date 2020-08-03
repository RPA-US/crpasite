# Generated by Django 3.0.7 on 2020-08-03 16:34

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields
import taxcategs.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTerm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('term', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_tax_categ', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=False)),
                ('categoryChars', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), size=None)),
            ],
            options={
                'verbose_name': 'Category Term',
                'verbose_name_plural': 'Category Terms',
            },
        ),
        migrations.CreateModel(
            name='TaxCateg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='taxcategs.TaxCateg', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'Taxonomic category',
                'verbose_name_plural': 'Taxonomic categories',
            },
            managers=[
                ('tree', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.CharField(choices=[(taxcategs.models.DecisionChoice['OK'], 'Accepted'), (taxcategs.models.DecisionChoice['KO'], 'Refused'), (taxcategs.models.DecisionChoice['KK'], 'Accepted with changes')], max_length=30)),
                ('result', models.CharField(choices=[(taxcategs.models.ResultChoice['NC'], 'New category term'), (taxcategs.models.ResultChoice['NT'], 'New taxonomic category'), (taxcategs.models.ResultChoice['CT'], 'Taxonomic category proposal save as new category term'), (taxcategs.models.ResultChoice['TE'], 'Taxonomic category edited')], max_length=60)),
                ('explanation', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Reviewer')),
            ],
            options={
                'verbose_name': 'Decision',
                'verbose_name_plural': 'Decisions',
            },
        ),
        migrations.CreateModel(
            name='KnowledgeSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creator')),
            ],
            options={
                'verbose_name': 'Knowledge Source',
                'verbose_name_plural': 'Knowledge Sources',
            },
        ),
        migrations.CreateModel(
            name='InputFormatSupported',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(verbose_name='slug')),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='taxcategs.InputFormatSupported', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'Input Format Supported',
                'verbose_name_plural': 'Input Formats Supported',
            },
            managers=[
                ('tree', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('category_term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxcategs.CategoryTerm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.AddField(
            model_name='categoryterm',
            name='formats_supported',
            field=models.ManyToManyField(blank=True, to='taxcategs.InputFormatSupported'),
        ),
        migrations.AddField(
            model_name='categoryterm',
            name='knowledge_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxcategs.KnowledgeSource'),
        ),
        migrations.AddField(
            model_name='categoryterm',
            name='tax_categ',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='taxcategs.TaxCateg'),
        ),
        migrations.AddField(
            model_name='categoryterm',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Creator'),
        ),
    ]
