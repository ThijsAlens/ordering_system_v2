

class Item():
    def __init__(self, id: int, name: str, destination: str, price: float) -> None:
        self.id: int = id
        self.name: str = name
        self.destination: str = destination
        self.price: float = price

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "destination": self.destination,
            "price": self.price
        }

    @classmethod
    def deserialize(cls, data: dict):
        return cls(data["id"], data["name"], data["destination"], data["price"])