import back_end.model.item

class Order:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.items: list[back_end.model.item.Item] = []

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "items": [item.serialize() for item in self.items]
        }

    @classmethod
    def deserialize(cls, data: dict):
        order = cls(data["id"])
        order.items = [back_end.model.item.deserialize(item) for item in data["items"]]
        return order

    def add_item(self, item: back_end.model.item) -> None:
        self.items.append(item)

    def remove_item(self, item: back_end.model.item) -> None:
        self.items.remove(item)