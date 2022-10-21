import uuid


def generate_code() -> str:
    code = str(uuid.uuid4())
    return code.split('-')[0].upper()
    