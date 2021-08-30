# Generated by Django 3.1.13 on 2021-08-30 20:19

import django.core.serializers.json
from django.db import migrations, models
import nautobot.core.fields
import taggit.managers
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("extras", "0014_scheduled_job"),
    ]

    operations = [
        migrations.CreateModel(
            name="Secret",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("created", models.DateField(auto_now_add=True, null=True)),
                ("last_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "_custom_field_data",
                    models.JSONField(blank=True, default=dict, encoder=django.core.serializers.json.DjangoJSONEncoder),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "slug",
                    nautobot.core.fields.AutoSlugField(blank=True, max_length=100, populate_from="name", unique=True),
                ),
                ("provider", models.CharField(max_length=100)),
                ("parameters", models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder)),
                ("tags", taggit.managers.TaggableManager(through="extras.TaggedItem", to="extras.Tag")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]
