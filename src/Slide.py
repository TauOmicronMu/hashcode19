from typing import List


class Slide:

    def __init__(self, image: List):
        self.image = image
        self.vertical = image[0].vertical
        self.tags = image[0].tags
        if len(image) == 2:
            self.tags += list(set(image[1].tags) -
                              set(image[0].tags))
        self.prev_slide = None
        self.next_slide = None
        self.start = False
        self.end = False
