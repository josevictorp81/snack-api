from core.models import Snack


def get_snacks() -> list:
    return Snack.objects.filter(available=True)


def search_snack(id: int) -> Snack:
    return Snack.objects.get(id=id)
