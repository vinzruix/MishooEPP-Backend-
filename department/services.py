from django.contrib.auth.models import Group, Permission

from department.models import Department



def get_department(department):
    try:
        return Department.objects.get(id=department)
    except Department.DoesNotExist:
        raise ValueError("Department does not exist")


def create_group(name, permissions):

    if not name:
        raise ValueError("There is no name")

    if Group.objects.filter(name=name).exists():
        raise ValueError("Group name already exist")

    group = Group()
    group.name = name
    group.save()


    add_permissions(group,permissions)

    return group



def add_permissions(group, permissions):

    for permission in permissions:
        try:
            group.permissions.add(Permission.objects.get(codename=permission))
        except Permission.DoesNotExist:
            group.delete()
            raise ValueError("Permission does not exist")

    return group



def create_department(group,epp):

    if not group.name:
        raise ValueError("There is no name")

    if Department.objects.filter(name=group.name).exists():
        raise ValueError("Department already exist")

    new_department = Department()
    new_department.name = group.name
    new_department.group = group
    new_department.epp = epp
    new_department.save()

    return new_department