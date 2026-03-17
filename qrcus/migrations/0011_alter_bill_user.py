# Generated migration to fix Bill model - change from registration to Customer

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qrcus', '0010_product_quantity_delete_billitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='user',
        ),
        migrations.AddField(
            model_name='bill',
            name='customer',
            field=models.ForeignKey(default=1, to='qrcus.customer', on_delete=django.db.models.deletion.CASCADE),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bill',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
    ]
