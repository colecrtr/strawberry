# Generated by Django 3.1.3 on 2020-11-15 23:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mx_atrium", "0002_auto_20201114_2135"),
    ]

    operations = [
        migrations.AlterField(
            model_name="institution",
            name="code",
            field=models.CharField(
                help_text="A unique identifier for each institution, defined by MX.",
                max_length=256,
                unique=True,
                verbose_name="code",
            ),
        ),
        migrations.AlterField(
            model_name="institution",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
        ),
        migrations.AlterField(
            model_name="institution",
            name="medium_logo_url",
            field=models.URLField(
                help_text=(
                    "URL for a 100px X 100px logo for each institution. A generic logo is returned "
                    "for institutions that don't have one."
                ),
                verbose_name="Medium logo URL",
            ),
        ),
        migrations.AlterField(
            model_name="institution",
            name="name",
            field=models.CharField(
                help_text=(
                    'An easy-to-read name for an institution, e.g., "Chase Bank" or "Wells Fargo '
                    'Bank".'
                ),
                max_length=256,
                verbose_name="name",
            ),
        ),
        migrations.AlterField(
            model_name="institution",
            name="small_logo_url",
            field=models.URLField(
                help_text=(
                    "URL for a 50px X 50px logo for each institution. A generic logo is returned "
                    "for institutions that don't have one."
                ),
                verbose_name="Small logo URL",
            ),
        ),
        migrations.AlterField(
            model_name="institution",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="institution",
            name="url",
            field=models.URLField(
                help_text="Website URL for a particular institution, e.g., www.chase.com.",
                verbose_name="URL",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="aggregated_at",
            field=models.DateTimeField(
                help_text="The date and time the account was last aggregated.",
                verbose_name="Aggregated at",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="connection_status",
            field=models.CharField(
                choices=[("CHA", "Challenged"), ("CON", "Connected")],
                help_text="The status of a member's aggregation.",
                max_length=3,
                verbose_name="Connection status",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
        ),
        migrations.AlterField(
            model_name="member",
            name="guid",
            field=models.CharField(
                help_text="A unique identifier for the member. Defined by MX.",
                max_length=256,
                unique=True,
                verbose_name="GUID",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="institution",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="mx_atrium.institution",
                verbose_name="Institution",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="name",
            field=models.CharField(
                help_text=(
                    "The name of the member. If omitted as a parameter when creating the member, "
                    'the institution name within the MX platform will be used, e.g., "Chase Bank."'
                ),
                max_length=256,
                verbose_name="Name",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="successfully_aggregated_at",
            field=models.DateTimeField(
                help_text="The date and time the member was successfully aggregated.",
                verbose_name="Successfully aggregated at",
            ),
        ),
        migrations.AlterField(
            model_name="member",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
        migrations.AlterField(
            model_name="member",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="mx_atrium.user",
                verbose_name="MX Atrium user",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="account_user",
            field=models.OneToOneField(
                help_text="Application User this MX Atrium User belongs to",
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Account user",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="Created at"),
        ),
        migrations.AlterField(
            model_name="user",
            name="guid",
            field=models.CharField(
                help_text="A unique identifier, defined by MX.",
                max_length=256,
                unique=True,
                verbose_name="GUID",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="is_disabled",
            field=models.BooleanField(
                help_text="True if you want the user disabled, false otherwise.",
                verbose_name="Is disabled",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, verbose_name="Updated at"),
        ),
    ]
