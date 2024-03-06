import matplotlib.pyplot as plt


class DataReport:
    def __init__(self, x, y, title='', xlabel='', ylabel='', color='blue', figsize=(10, 6)):
        self.x = x
        self.y = y
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.color = color
        self.figsize = figsize
