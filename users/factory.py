from abc import ABC, abstractmethod

from django.contrib.auth.models import Permission

from users.models import User

class UserCreator(ABC):

    @abstractmethod
    def factory_method(self):
        raise NotImplementedError

    def register(self, **kwargs):
        new_user = self.factory_method()
        return new_user.create(**kwargs)



class WorkerCreator(UserCreator):

    def factory_method(self):
        return WorkerUser()


class SensorNodeCreator(UserCreator):

    def factory_method(self):
        return SensorNodeUser()


## Products

class UserProduct(ABC):

    @abstractmethod
    def create(self, **kwargs):
        raise NotImplementedError


class WorkerUser(UserProduct):

    def create(self, **kwargs):
        new_user = User()

        new_user.first_name = kwargs.get('name')
        new_user.last_name = kwargs.get('last_name')
        new_user.email = kwargs.get('email')
        new_user.username = kwargs.get('username')
        new_user.set_password(kwargs.get('password'))

        new_user.department = kwargs.get('department')
        new_user.tensor_faces = kwargs.get('faces')
        new_user.face = kwargs.get('face')

        new_user.save()

        new_user.groups.add(new_user.department.group)

        return new_user


class SensorNodeUser(UserProduct):

    def create(self, **kwargs):
        node = User()
        node.username = kwargs.get('username')
        node.set_password(kwargs.get('password'))
        node.is_device = True
        node.save()

        node.user_permissions.add(Permission.objects.get(codename="create_data_sensor"))

        return node

