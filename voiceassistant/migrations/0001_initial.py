# Generated by Django 4.2.7 on 2024-09-19 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LlmPrompt",
            fields=[
                (
                    "id",
                    models.AutoField(primary_key=True, serialize=False, unique=True),
                ),
                ("prompt_type", models.CharField(default="None", max_length=20)),
                ("input_prompt", models.TextField(default="")),
            ],
        ),
    ]
