
class Compose():

    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, item):
        for transform in self.transforms:
            item = transform(item)
        return item
