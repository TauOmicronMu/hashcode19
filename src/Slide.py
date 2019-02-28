class Slide:
    def __init__(self, vertical, tags):
        self.vertical = vertical
        self.tags = tags
        self.prev_slide = None
        self.next_slide = None
        self.start = False
        self.end = False

    def set_start(self, start):
        self.start = start

    def get_start(self, start):
        self.start = start
