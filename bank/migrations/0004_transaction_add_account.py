from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0003_transaction_add_balance'),
    ]

    operations = [
        migrations.RunSQL(
            '''
            alter table transfer add account_id text;
            ''',
            'alter table transfer drop column account_id;'
        )
    ]