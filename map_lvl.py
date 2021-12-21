from settings import *


class Map(name):
    def __init__(self, Name):
        super(self, Name).__init__()
        self.map_load = open(Name, encoding='utf-8')
        self.line = [len(line) for line in self.map_load.read().split('\n')[0]]
        print(self.line)
