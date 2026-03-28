from django.contrib.auth.models import Group, Permission


def create_group(name, permissions):
    group = Group.objects.create(name=name)

    for permission in permissions:
        group.permissions.add(Permission.objects.filter(codename=permission))

    return group
