from core.models import Classes


def get_classes() -> list:
    return Classes.objects.all()


def search_classes(id: int) -> Classes:
    return Classes.objects.get(id=id)
