from uuid import uuid4
#Generiere eine ID aus einem Prefix und einer zufällig generierten UUID
def generate_id(prefix: str):

	return f"{prefix}-{uuid4()}"