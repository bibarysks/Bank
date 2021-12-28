from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            '''
            create table transfer(
            id text,
            amount numeric,
            from_account text,
            to_account text,
            date_time text
            );
            ''',
            'drop table transfer;'
        )
    ]