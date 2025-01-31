import back_end.model.item

class Order:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.table: int = -1
        # A list of tuples containing the amount of items and the item itself
        self.items: list[tuple[int, back_end.model.item.Item]] = []

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "table": self.table,
            "items": [((item[0], item[1].serialize())) for item in self.items]
        }

    @classmethod
    def deserialize(cls, data: dict):
        order = cls(data["id"])
        order.table = data["table"]
        for item in data["items"]:
            order.items.append((item[0], back_end.model.item.Item.deserialize(item[1])))
        return order

    def add_item(self, item: back_end.model.item) -> None:
        self.items.append(item)

    def remove_item(self, item: back_end.model.item) -> None:
        self.items.remove(item)