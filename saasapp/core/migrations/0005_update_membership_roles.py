from django.db import migrations


def rename_staff_to_member(apps, schema_editor):
    Membership = apps.get_model("core", "Membership")
    Membership.objects.filter(role="staff").update(role="member")


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_membership_and_foia"),
    ]

    operations = [
        migrations.RunPython(rename_staff_to_member, migrations.RunPython.noop),
    ]
