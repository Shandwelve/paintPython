from tkinter.colorchooser import askcolor


class Paint:
    base_colors = ('Red', 'Green', 'Blue', 'Black', 'White')
    figures = ('Line', 'Oval', 'Rectangle', 'Brush')
    file_types = [
        ('PNG', '*.png'),
        ('JPG', '*.jpg'),
        ('JPEG', '*.jpeg')
    ]

    def __init__(self):
        self.color = 'black'
        self.figure = 'Brush'
        self.image_path = None
        self.image = None
        self.tmp = None
        self.coordinates = []
        self.elements = []
        self.size = 3

    def change_color(self, color=None):
        if not color:
            color = askcolor()[1]
        if color:
            self.color = color

    def change_figure(self, figure):
        self.figure = figure
        self.coordinates = []

    def add_coordinate(self, point):
        if len(self.coordinates) > 1000:
            self.coordinates = self.coordinates[100:]

        self.coordinates.append(point)

        if len(self.coordinates) == 2:
            return True
        return False
