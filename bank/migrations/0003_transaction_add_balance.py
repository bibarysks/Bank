from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0002_transaction'),
    ]

    operations = [
        migrations.RunSQL(
            '''
            alter table transfer add balance numeric;
            ''',
            'alter table transfer drop column balance;'
        )
    ]