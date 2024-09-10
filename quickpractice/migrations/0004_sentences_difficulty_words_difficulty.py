# Generated by Django 4.2.7 on 2024-08-05 11:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("quickpractice", "0003_alter_sentences_sentence_alter_words_word"),
    ]

    operations = [
        migrations.AddField(
            model_name="sentences",
            name="difficulty",
            field=models.CharField(
                choices=[
                    ("B1", "B1"),
                    ("C1", "C1"),
                    ("B2", "B2"),
                    ("A2", "A2"),
                    ("A1", "A1"),
                    ("C2", "C2"),
                ],
                default="",
                max_length=2,
            ),
        ),
        migrations.AddField(
            model_name="words",
            name="difficulty",
            field=models.CharField(
                choices=[
                    ("B1", "B1"),
                    ("C1", "C1"),
                    ("B2", "B2"),
                    ("A2", "A2"),
                    ("A1", "A1"),
                    ("C2", "C2"),
                ],
                default="",
                max_length=2,
            ),
        ),
    ]
