from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_client_and_task_user'),
        ('customers', '0002_remove_tenant_auto_create_schema_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=20)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.tenant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FoiaRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_foia_requests', to=settings.AUTH_USER_MODEL)),
                ('resident', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='foia_requests', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('user', 'tenant')},
        ),
    ]
