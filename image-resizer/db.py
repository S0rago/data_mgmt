import typing


class ImageFile:
    def __init__(self):
        self.id: int = 0
        self.name: str = ""
        self.content: bytes = None

    def __init__(self, id, name, content):
        self.id: int = id
        self.name: str = name
        self.content: bytes = content
    


class Database:
    def __init__(self):
        self._items: typing.Dict[int, ImageFile] = {}
        self._seq: int = 0

    def getbyid(self, id: int) -> ImageFile:
        image = self._items.get(id)
        if image is not None:
            return image
        else:
            raise ValueError(f"Image not found with id = {id}")

    def getbyname(self, name: str) -> ImageFile:
        for id, image in self._items.items():
            if image.name == name:
                return image
        else:
            raise ValueError(f"Image not found with name = {name}")
        

    def add(self, filename: str, image: bytes) -> int:
        self._seq += 1
        self._items[self._seq] = ImageFile(self._seq, filename, image)
        return self._seq

    def delete(self, id: int):
        if self._items.pop(id, None):
            raise ValueError(f"Image not found with id = {id}")
