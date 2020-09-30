import uuid


def generate_uuid():
    return ''.join(str(uuid.uuid4()).split('-'))
