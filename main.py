from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk, ImageGrab
from paint import *
import time


class App(Paint):
    def __init__(self):
        super().__init__()
        self.window = Tk()
        self.window.geometry("1920x1080")
        self.window.title('New File')
        self.display = Canvas(self.window)
        self.display.configure(background='white')
        self.display.pack(expand=1, fill=BOTH)
        self.menu = Menu(self.window)
        self.window.config(menu=self.menu)
        self.display.bind("<Button 1>", self.motion)
        self.window.bind("<Control-z>", self.undo)
        self.display.bind("<B1-Motion>", self.pencil_draw)
        self.figure_menu = Menu(self.menu, tearoff=0)
        self.file_menu = Menu(self.menu, tearoff=0)
        self.color_menu = Menu(self.menu, tearoff=0)
        self.size_menu = Menu(self.menu, tearoff=0)

        self.make_template()

    def make_template(self):
        for i in self.base_colors:
            self.color_menu.add_command(label=i, command=lambda color=i: self.change_color(color), font=("Verdana", 12))
        self.color_menu.add_command(label='More..', command=self.change_color, font=("Verdana", 12))

        for i in self.figures:
            self.figure_menu.add_command(label=i, command=lambda figure=i: self.change_figure(figure),
                                         font=("Verdana", 12))

        self.file_menu.add_command(label='New', command=self.new_img, font=("Verdana", 12))
        self.file_menu.add_command(label='Open', command=self.open_file, font=("Verdana", 12))
        self.file_menu.add_command(label='Save', command=self.save_img, font=("Verdana", 12))
        self.file_menu.add_command(label='Save As', command=self.save_as, font=("Verdana", 12))
        self.file_menu.add_command(label='Exit', command=self.window.destroy, font=("Verdana", 12))
        self.size_menu.add_command(label='Size', command=self.change_size, font=("Verdana", 12))

        self.menu.add_cascade(label='File', menu=self.file_menu)
        self.menu.add_cascade(label='Color', menu=self.color_menu)
        self.menu.add_cascade(label='Draw', menu=self.figure_menu)
        self.menu.add_cascade(label='Size', menu=self.size_menu)

    def open_file(self):
        directory = filedialog.askopenfilename(filetypes=self.file_types, defaultextension='.png')
        if not directory:
            return
        self.display.delete("all")
        self.image = ImageTk.PhotoImage(Image.open(directory))
        self.display.create_image(0, 0, image=self.image, anchor=NW)
        self.image_path = directory
        self.window.title(directory)
        self.coordinates = []

    def save_as(self):
        file = filedialog.asksaveasfilename(filetypes=self.file_types, defaultextension='.png')
        if not file:
            return
        canvas = self._canvas()
        time.sleep(1)
        self.tmp = ImageGrab.grab(bbox=canvas).save(file)
        self.image_path = file
        self.window.title(file)

    def save_img(self):
        if not self.image_path:
            self.save_as()
        canvas = self._canvas()
        time.sleep(1)
        self.tmp = ImageGrab.grab(bbox=canvas).save(self.image_path)

    def new_img(self):
        self.display.delete("all")
        self.image_path = None
        self.window.title('New File')
        self.coordinates = []

    def _canvas(self):
        x = self.display.winfo_rootx() + self.display.winfo_x() + 10
        y = self.display.winfo_rooty() + self.display.winfo_y() + 15
        x1 = x + self.display.winfo_width() + 50
        y1 = y + self.display.winfo_height() + 50

        return x, y, x1, y1

    def motion(self, event):
        coordinate = event.x, event.y
        need_draw = self.add_coordinate(coordinate)

        if need_draw:
            self.draw()
            self.coordinates = []

    def undo(self, e=None):
        if self.elements:
            self.display.delete(self.elements[-1])
            self.elements = self.elements[:-1]

    def pencil_draw(self, event):
        if self.figure == 'Brush':
            self.display.create_oval(event.x - self.size, event.y - self.size,
                                     event.x + self.size, event.y + self.size,
                                     fill=self.color, outline=self.color)

    def draw(self):
        if self.figure == 'Line':
            self.elements.append(
                self.display.create_line(self.coordinates[0][0], self.coordinates[0][1], self.coordinates[1][0],
                                         self.coordinates[1][1], fill=self.color, width=self.size * 2))
            return True
        if self.figure == 'Rectangle':
            self.elements.append(
                self.display.create_rectangle(self.coordinates[0][0], self.coordinates[0][1], self.coordinates[1][0],
                                              self.coordinates[1][1], outline=self.color, width=self.size * 2))
            return True
        if self.figure == 'Oval':
            self.elements.append(
                self.display.create_oval(self.coordinates[0][0], self.coordinates[0][1], self.coordinates[1][0],
                                         self.coordinates[1][1], outline=self.color, width=self.size * 2))
            return True

    def change_size(self):
        window = Toplevel(self.window)
        window.title('')
        window.resizable(False, False)
        window.grab_set()
        window.focus_set()

        var = StringVar()
        frame = Frame(window)
        label = Label(frame, text='Size:', font=('Arial', 10))
        size = Spinbox(frame, textvariable=var, from_=1, to=20, font=('Arial', 10))
        var.set(self.size)
        label.pack(side=TOP)
        size.pack(side=TOP)
        frame.pack(side=LEFT, fill=Y, padx=10)
        save = Button(frame, text='Save', command=lambda s=size, w=window: self.save_size(w, s), font=('Arial', 11))
        save.pack(side=LEFT, padx=5, pady=5)

    def save_size(self, window, size):
        self.size = int(size.get())
        window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
