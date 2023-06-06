from core.models import Child


def get_students() -> list:
    return Child.objects.all()


def search_student(id: int) -> Child:
    return Child.objects.get(id=id)
