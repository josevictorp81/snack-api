from django.contrib.auth.models import User


def get_fathers() -> list:
    return User.objects.all()


def search_father(id: int) -> User:
    return User.objects.get(id=id)
