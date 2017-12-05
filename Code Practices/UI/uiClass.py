from tkinter import *
import datetime

class ui():

    def __init__(self):
        self.root = Tk()
        self.home_screen = Frame(self.root)
        self.new_order_screen = Frame(self.root)
        self.background_colour = "#7fcc7c"
        self.contrast_colour = "#aeffaa"
        self.items = []

    def initialise_root(self):
        print("Test")
        self.root.title("Warehouse Picking Control Interface")
        self.root.maxsize(750,500)
        self.initialise_home_screen()        

    def initialise_buttons(self, screen):
        title = Label(screen,
                  fg = "black",
                  font = "Arial 30 bold",
                  text="Automated Picking Control Interface",
                  bg = self.background_colour).grid(row=0, column=0, columnspan=3)
        stop_image = PhotoImage(file = "stop.png")
        stop_button = Button(screen, width=100, height=100, image=stop_image)
        stop_button.image = stop_image
        stop_button.grid(row=4, column=2)
        home_image = PhotoImage(file = "home.png")
        home_button = Button(screen, width=100, height=100, image=home_image, command = self.initialise_home_screen)
        home_button.image = home_image
        home_button.grid(row=4, column=0)

    def initialise_home_screen(self):
        self.home_screen.grid(row=4, column=2)
        for x in range(0,5):
            self.home_screen.grid_rowconfigure(x, minsize = 100)
        for y in range(0,3):
            self.home_screen.grid_columnconfigure(y, minsize=250)
        self.home_screen.configure(background = self.background_colour)
        warehouse_options_button = Button(self.home_screen,
                        fg = "black",
                        font = "Arial 20 italic",
                        text = "Warehouse Options",
                        width = 15,
                        height = 2,
                        bg = self.contrast_colour).grid(row=2, column=1)
        new_order_button = Button(self.home_screen,
                        fg = "black",
                        font = "Arial 20 italic",
                        text = "New Order",
                        width = 15,
                        height = 2,
                        bg = self.contrast_colour,
                        command = self.initialise_new_order_screen).grid(row=3, column=1)
        view_orders_button = Button(self.home_screen,
                        fg = "black",
                        font = "Arial 20 italic",
                        text = "View Orders",
                        width = 15,
                        height = 2,
                        bg = self.contrast_colour).grid(row=4, column=1)
        self.initialise_buttons(self.home_screen)
        self.home_screen.tkraise()

    def initialise_new_order_screen(self):
        def clear_items():
            self.items =[]
            item_list.grid_remove()
            self.initialise_new_order_screen()
        def enter_item():
            item = item_box.get()
            item_box.delete(0, 'end')
            self.items.append(item)
            self.initialise_new_order_screen()
        self.new_order_screen.grid(row=4, column=2)
        for x in range(0,5):
            self.new_order_screen.grid_rowconfigure(x, minsize = 100)
        for y in range(0,3):
            self.new_order_screen.grid_columnconfigure(y, minsize=250)
        self.new_order_screen.configure(background = self.background_colour)
        time_label = Label(self.new_order_screen,
                           text = "Order Time:",
                           fg = "black",
                           font = "Arial 20 bold",
                           bg = self.background_colour).grid(row=1, column=0)
        time_text = Label(self.new_order_screen,
                          text = str(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")),
                          fg = "black",
                          font = "Arial 15 italic",
                          width = 20,
                          height = 2,
                          bg = self.contrast_colour).grid(row=1, column=1)
        item_label = Label(self.new_order_screen,
                           text = "Item:",
                           fg = "black",
                           font = "Arial 20 bold",
                           bg = self.background_colour).grid(row=2, column=0)
        item_box = Entry(self.new_order_screen,
                        font = "Arial 15 italic")
        item_box.grid(row=2, column=1)
        item_entry_button = Button(self.new_order_screen,
                             fg = "black",
                             font = "Arial 10 italic",
                             text = "Add Item\nto Order",
                             width = 10,
                             height = 3,
                             bg = self.contrast_colour,
                             command = enter_item).grid(row=2, column=2)
        item_list_label = Label(self.new_order_screen,
                           text = "Items:",
                           fg = "black",
                           font = "Arial 20 bold",
                           bg = self.background_colour).grid(row=3, column=0, columnspan = 2)
        item_list = Label(self.new_order_screen,
                           text = self.items,
                           fg = "black",
                           font = "Arial 15 italic",
                           bg = self.background_colour)
        item_list.grid(row=3, column=1)
        clear_button = Button(self.new_order_screen,
                             fg = "black",
                             font = "Arial 18 italic",
                             text = "Clear Items",
                             width = 15,
                             height = 2,
                             bg = self.contrast_colour,
                             command = clear_items).grid(row=3, column=2)
        save_button = Button(self.new_order_screen,
                             fg = "black",
                             font = "Arial 20 italic",
                             text = "Save and Go",
                             width = 15,
                             height = 2,
                             bg = self.contrast_colour).grid(row=4, column=1)
        self.initialise_buttons(self.new_order_screen)
        self.new_order_screen.tkraise()
    
        
                              
ui= ui()
ui.initialise_root()
