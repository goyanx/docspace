# Generated by Django 3.2.14 on 2022-12-11 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_document_upload_session_alter_chunk_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunk',
            name='summary',
            field=models.TextField(blank=True, null=True),
        ),
    ]