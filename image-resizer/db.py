import typing
from numpy import ndarray


class Database:
    def __init__(self):
        self._items: typing.Dict[int, ndarray] = {}
        self._seq: int = 0

    def get(self, id: int) -> ndarray:
        image = self._items.get(id)
        if image is not None:
            return image
        else:
            raise ValueError("Image not found with id =", id)

    def add(self, image: ndarray) -> int:
        self._seq += 1
        self._items[self._seq] = image
        return self._seq

    def delete(self, id: int):
        if id in self._items.keys:
            del self._items[id]
        else:
            raise ValueError("Image not found with id =", id)
