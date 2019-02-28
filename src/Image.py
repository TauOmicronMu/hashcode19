from typing import List


class Image():

    def __init__(self, image_num: int, tags: List[str], vertical: bool):
        self.image_num = image_num
        self.tags = tags
        self.vertical = vertical
