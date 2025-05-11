from uuid import uuid4

def generate_id(prefix: str):
	return f"{prefix}-{uuid4()}"