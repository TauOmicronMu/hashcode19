class Slide:
    def __init__(self, image_num, vertical, tags):
        self.vertical = vertical
        self.tags = tags
        self.prev_slide = None
        self.next_slide = None
        self.start = False
        self.end = False
        self.image_num = image_num

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end
