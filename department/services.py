from django.contrib.auth.models import Group, Permission

from department.models import Department


def create_group(name, permissions):



    if Group.objects.filter(name=name).exists():
        raise ValueError("Group name already exist")

    group = Group()
    group.name = name
    group.save()


    for permission in permissions:
        try:
            group.permissions.add(Permission.objects.get(codename=permission))
        except Permission.DoesNotExist:
            group.delete()
            raise ValueError("Permission does not exist")

    return group


def create_department(group,epp):

    if Department.objects.filter(name=group.name).exists():
        raise ValueError("Department already exist")

    new_department = Department()
    new_department.name = group.name
    new_department.group = group
    new_department.epp = epp
    new_department.save()

    return new_department