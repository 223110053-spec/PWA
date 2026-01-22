from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0002_auto_20210222_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='created',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='updated',
        ),
    ]
