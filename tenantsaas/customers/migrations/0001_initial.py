from django.db import migrations, models
import django.db.models.deletion
from django_tenants.postgresql_backend.base import _check_schema_name

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schema_name', models.CharField(max_length=63, unique=True, db_index=True, validators=[_check_schema_name])),
                ('name', models.CharField(max_length=100)),
            ],
            options={'app_label': 'customers'},
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=253, unique=True, db_index=True)),
                ('is_primary', models.BooleanField(default=True, db_index=True)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='customers.tenant')),
            ],
            options={'app_label': 'customers'},
        ),
    ]
