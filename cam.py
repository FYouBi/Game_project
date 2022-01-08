from settings import HEIGHT


class Camera:
    def __init__(self):
        self.dy = 0

    def apply(self, obj):
        obj.rect.y += self.dy

    def update(self, target):
        self.dy = -(target.rect.y + target.rect.h // 1.5 - HEIGHT // 1.5)


camera = Camera()
