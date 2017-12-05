from tkinter import *
from tkinter import messagebox
from databaseClass import *
from shortestClass import *
from improvementsClass import *
import datetime

db = Database()
sh = ShortestPath()
imp = Improvements()

class ui():

    def __init__(self):
        self.root = Tk()
        self.home_screen = Frame(self.root)
        self.new_order_screen = Frame(self.root)
        self.warehouse_options_screen = Frame(self.root)
        self.item_info_screen =  Frame(self.root)
        self.view_orders_screen = Frame(self.root)
        self.new_item_screen = Frame(self.root)
        self.robot_control_screen = Frame(self.root)
        self.warehouse_improvements_screen = Frame(self.root)
        self.background_colour = "#7fcc7c"
        self.contrast_colour = "#aeffaa"
        self.startlocation = "I2"
        self.droplocation = "I1"
        self.items = []

    def initialise_robot_control_screen(self):
        self.robot_control_screen.grid(row=4, column=2)
        for x in range(0,5):
            self.robot_control_screen.grid_rowconfigure(x, minsize = 100)
        for y in range(0,3):
            self.robot_control_screen.grid_columnconfigure(y, minsize=250)
        self.robot_control_screen.configure(background = self.background_colour)

        self.initialise_buttons(self.robot_control_screen)
        self.robot_control_screen.tkraise()

    def initialise_root(self):
        self.root.title("Warehouse Picking Control Interface")
        self.root.maxsize(750,500)
        self.initialise_home_screen()        

    def initialise_buttons(self, screen):
        title = Label(screen,
                  fg = "black",
                  font = "Arial 28 bold",
                  text="Automated Picking Control Interface",
                  bg = self.background_colour).grid(row=0, column=0, columnspan=3)
        stop_image = PhotoImage(file = "Files/stop.png")
        stop_button = Button(screen, width=100, height=100, image=stop_image, command = self.emergency_stop)
        stop_button.image = stop_image
        stop_button.grid(row=4, column=2)
        home_image = PhotoImage(file = "Files/home.png")
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
                        bg = self.contrast_colour,
                        command = self.initialise_warehouse_options_screen).grid(row=2, column=1)
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
                        bg = self.contrast_colour,
                        command = self.initialise_view_orders_screen).grid(row=4, column=1)
        robot_button = Button(self.home_screen,
                        fg = "black",
                        font = "Arial 20 italic",
                        text = "Robot\nControl",
                        width = 10,
                        height = 4,
                        bg = self.contrast_colour,
                        command = self.initialise_robot_control_screen).grid(row=2, column=2, rowspan = 2)
        self.initialise_buttons(self.home_screen)
        self.home_screen.tkraise()

    def initialise_new_order_screen(self):
        db.remove_blanks()
        def scan():
            barcodebox.delete(0, END)
            barcodebox.focus_set()
        def clear_items():
            listbox.delete(0, END)
            itemdict.clear()
        def enter_item():
            good = True
            itemid = item_box.get()
            if itemid == "":
                barcode = barcodebox.get()
                try:
                    itemid = db.get_item_info_barcode(barcode)[0][0]
                except:
                    messagebox.showwarning("Warning", "Item not Found")
                    barcodebox.delete(0, END)
                    good = False
            if itemid in itemdict:
                messagebox.showwarning("Warning", "Item already in order. Please try a different item")
                barcodebox.delete(0, END)
                item_box.delete(0, 'end')
                quantity_box.delete(0, 'end')
                good = False
            try:
                description = db.get_item_singleinfo(itemid, "ItemDescription")
                quantity = int(quantity_box.get())
                if quantity > int(db.get_item_singleinfo(itemid, "ItemStock")):
                    messagebox.showwarning("Warning", "Item not availiable")
                    good = False
            except:
                messagebox.showwarning("Warning", "Item not Found")
                barcodebox.delete(0, END)
                item_box.delete(0, 'end')
                quantity_box.delete(0, 'end')
                quantity_box.insert(0, "1")
                good = False
           
            if good:                        
                item_box.delete(0, 'end')
                barcodebox.delete(0, END)
                quantity_box.delete(0, 'end')
                string = (str(quantity)+" * "+description)
                listbox.insert(0, string)
                itemdict[itemid]=quantity
                quantity_box.insert(0, "1")
                currentweight = weightbox.get()
                newweight = (float(currentweight) + (int(db.get_item_singleinfo(itemid, "ItemWeight"))/1000))
                weightbox.delete(0, 'end')
                weightbox.insert(0, newweight)               
        def go():
            if len(itemdict) != 0:
                locations = []
                for x in itemdict:
                    db.insert_orderitem(order_no, x, itemdict[x])
                    db.update_stock(x, int(itemdict[x]))
                for x in itemdict:
                    locations.append(db.get_item_singleinfo(x, "ItemLocation"))
                path  = sh.find_route(self.startlocation, locations, self.droplocation)
                message = ("Route: " +  str(path[0]))
                messagebox.showinfo("Success", str(message))
                db.insert_order_complete_time(order_no)
                self.initialise_home_screen()
            else:
                messagebox.showwarning("Warning", "No Items in Order")
        itemdict = {}
        order_no = str(db.insert_order())    
        self.new_order_screen.grid(row=4, column=2)
        for x in range(0,5):
            self.new_order_screen.grid_rowconfigure(x, minsize = 100)
        for y in range(0,3):
            self.new_order_screen.grid_columnconfigure(y, minsize=250)
        self.new_order_screen.configure(background = self.background_colour)
        ordertext = str("Order Number: "+order_no)
        id_label = Label(self.new_order_screen,
                           text = ordertext,
                           fg = "black",
                           font = "Arial 12",
                           bg = self.background_colour).grid(row=1, column=1, sticky= N)
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
                           text = "Item Number:",
                           fg = "black",
                           font = "Arial 20 bold",
                           bg = self.background_colour).grid(row=2, column=0)
        item_box = Entry(self.new_order_screen,
                        font = "Arial 20 italic",
                         width = 7)
        item_box.grid(row=2, column=1, sticky = W)
        quantity_box = Entry(self.new_order_screen,
                        font = "Arial 15 italic",
                         width = 7)
        quantity_box.grid(row=2, column=1, sticky = SW)
        barcodebox = Entry(self.new_order_screen,
                        font = "Arial 15 italic",
                         width = 10)
        barcodebox.grid(row=3, column=1, sticky = NW)
        item_entry_button = Button(self.new_order_screen,
                             fg = "black",
                             font = "Arial 15 italic",
                             text = "Add Item",
                             width = 10,
                             bg = self.contrast_colour,
                             command = enter_item).grid(row=2, column=1, sticky= E)
        quantity_label = Label(self.new_order_screen,
                           text = "Item Quantity:",
                           fg = "black",
                           font = "Arial 10 bold",
                           bg = self.background_colour).grid(row=2, column=0, sticky = SE)
        barcode_label = Label(self.new_order_screen,
                           text = "Barcode:",
                           fg = "black",
                           font = "Arial 10 bold",
                           bg = self.background_colour).grid(row=3, column=0, sticky = NE)
        quantity_box.insert(0, '1')
        scan_barcode_button = Button(self.new_order_screen,
                        fg = "black",
                        font = "Arial 10 italic",
                        text = "Scan Barcode",
                        width = 10,
                        bg = self.contrast_colour,
                        command = scan).grid(row=3, column=0, sticky = N)
        scrollbar = Scrollbar(self.new_order_screen)
        scrollbar.grid(row=1, column = 3, rowspan=3, sticky = E) 
        listbox = Listbox(self.new_order_screen)
        listbox.grid(row=1, column = 2, rowspan = 2)
        listbox.config(yscrollcommand=scrollbar.set,
                       width =25,
                       height=10,
                       font = "Arial 10")
        scrollbar.config(command=listbox.yview)
        weightlab = Label(self.new_order_screen,
                           text = "Total Weight:",
                           fg = "black",
                           font = "Arial 10 bold",
                           bg = self.background_colour).grid(row=3, column=2, sticky = NW)
        weightbox = Entry(self.new_order_screen,
                           font = "Arial 10 bold",
                           width = 7)
        weightbox.grid(row=3, column=2, sticky = N)
        weightbox.insert(0, "0")
        kglab = Label(self.new_order_screen,
                           text = "kg",
                           fg = "black",
                           font = "Arial 10 bold",
                           bg = self.background_colour).grid(row=3, column=2, sticky = NE)
        clear_button = Button(self.new_order_screen,
                             fg = "black",
                             font = "Arial 18 italic",
                             text = "Clear Items",
                             width = 15,
                             bg = self.contrast_colour,
                             command = clear_items).grid(row=3, column=2)
        save_button = Button(self.new_order_screen,
                             fg = "black",
                             font = "Arial 20 italic",
                             text = "Save and Go",
                             width = 15,
                             height = 2,
                             bg = self.contrast_colour,
                             command = go).grid(row=4, column=1)
        self.initialise_buttons(self.new_order_screen)
        self.new_order_screen.tkraise()
    
    def initialise_warehouse_options_screen(self):
        self.warehouse_options_screen.grid(row=4, column=2)
        for x in range(0,5):
            self.warehouse_options_screen.grid_rowconfigure(x, minsize = 100)
        for y in range(0,3):
            self.warehouse_options_screen.grid_columnconfigure(y, minsize=250)
        self.warehouse_options_screen.configure(background = self.background_colour)
        warehouse_image = PhotoImage(file = "Files/warehouse.png")
        warehouse_button = Button(self.warehouse_options_screen, width=250, height=100, image=warehouse_image)
        warehouse_button.image = warehouse_image
        warehouse_button.grid(row=1, column=1)
        warehouse_options_button = Button(self.warehouse_options_screen,
                        fg = "black",
                        font = "Arial 18 italic",
                        text = "View/Edit Item Information",
                        width = 23,
                        height = 2,
                        bg = self.contrast_colour,
                        command = self.initialise_item_info_screen).grid(row=2, column=1) 
        new_item_button = Button(self.warehouse_options_screen,
                        fg = "black",
                        font = "Arial 15 italic",
                        text = "Add New Item",
                        width = 25,
                        height = 2,
                        bg = self.contrast_colour,
                        command = self.initialise_item_info_screen).grid(row=3, column=1)
        warehouse_improvement_button = Button(self.warehouse_options_screen,
                        fg = "black",
                        font = "Arial 15 italic",
                        text = "View Warehouse Improvements",
                        width = 25,
                        height = 2,
                        bg = self.contrast_colour,
                        command = self.initialise_warehouse_improvements_screen).grid(row=4, column=1)
        self.initialise_buttons(self.warehouse_options_screen)
        self.warehouse_options_screen.tkraise()

    def initialise_item_info_screen(self):
        def validate(option):
            good = True
            itemid = itemidbox.get()
            description = descriptionbox.get()
            stock = stockbox.get()
            try:
                int(stock)
            except:
                messagebox.showwarning("Warning", "Stock must be an integer")
                good = False
                stockbox.delete(0, END)
            if int(stock) <0:
                messagebox.showwarning("Warning", "Stock Level Cannot be\nLess than 0")
                stockbox.delete(0, END)
                good = False
            location = locationbox.get()
            if location not in sh.graph:
                messagebox.showwarning("Warning", "Location does not Exist")
                locationbox.delete(0, END)
                good = False
            for x in db.get_used_locations():
                if x == location and x != db.get_item_singleinfo(itemid, "ItemLocation"):
                    messagebox.showwarning("Warning", "Location in Use")
                    locationbox.delete(0, END)
                    good = False
            barcode = barcodebox.get()
            for x in db.get_used_barcodes():
                if x == barcode and x != db.get_item_singleinfo(itemid, "ItemBarcode"):
                    messagebox.showwarning("Warning", "Barcode in Use")
                    barcodebox.delete(0, END)
                    good = False
            try:
                int(barcode)
                if len(barcode) != 9:
                    messagebox.showwarning("Warning", "Barcode is not valid")
                    barcodebox.delete(0, END)
                    good = False
            except:
                messagebox.showwarning("Warning", "Barcode is not valid")
                barcodebox.delete(0, END)
                good = False
            weight = weightbox.get()
            try:
                int(weight)
            except:
                messagebox.showwarning("Warning", "Weight must be an integer")
                good = False
                weightbox.delete(0, END)
            if int(weight) <0:
                messagebox.showwarning("Warning", "Weight Cannot be\nLess than 0")
                weightbox.delete(0, END)
                good  = False
            if good:
                if option == "new":
                    new(description, stock, location, barcode, weight)
                else:
                    update(description, stock, location, barcode, weight)

        def new(description, stock, location, barcode, weight):
            newid = db.insert_item(description, stock, location, barcode, weight)
            string = ("Item Information Updated Successfully\nNew Item ID: " + str(newid))
            messagebox.showinfo("Success", string)
            descriptionbox.delete(0, END)
            stockbox.delete(0, END)
            barcodebox.delete(0, END)
            weightbox.delete(0, END)
            locationbox.delete(0, END)
            itemidbox.delete(0, END)
        
        def scan_new_barcode():
            barcodebox.delete(0, END)        
            barcodebox.focus_set()

        def search():
            itemid = itemidbox.get()
            descriptionbox.delete(0, END)
            stockbox.delete(0, END)
            barcodebox.delete(0, END)
            weightbox.delete(0, END)
            locationbox.delete(0, END)
            try:
                info = db.get_item_info(itemid)
                descriptionbox.insert(0, info[0][0])
                stockbox.insert(0, info[0][1])
                locationbox.insert(0, info[0][2])
                barcodebox.insert(0, info[0][3])
                weightbox.insert(0, info[0][4])
            except:
                messagebox.showwarning("Warning", "Item not found")
                itemidbox.delete(0, END)

        def searchbarcode():
            itemidbox.delete(0, END)
            descriptionbox.delete(0, END)
            stockbox.delete(0, END)
            barcode = barcodebox.get()
            weightbox.delete(0, END)
            locationbox.delete(0, END)
            try:
                info = db.get_item_info_barcode(barcode)
                itemidbox.insert(0, info[0][0])
                descriptionbox.insert(0, info[0][1])
                stockbox.insert(0, info[0][2])
                locationbox.insert(0, info[0][3])
                weightbox.insert(0, info[0][4])
            except:
                messagebox.showwarning("Warning", "Item not found")
                barcodebox.delete(0, END)
    
        def update(description, stock, location, barcode, weight):
            itemid = itemidbox.get()
            db.update_item(itemid, description, stock, location, barcode, weight)
            messagebox.showinfo("Success", "Item Information Updated Successfully")
            descriptionbox.delete(0, END)
            stockbox.delete(0, END)
            barcodebox.delete(0, END)
            weightbox.delete(0, END)
            locationbox.delete(0, END)
            itemidbox.delete(0, END)
        self.item_info_screen.grid(row=4, column=2)
        for x in range(0,5):
            self.item_info_screen.grid_rowconfigure(x, minsize = 100)
        for y in range(0,3):
            self.item_info_screen.grid_columnconfigure(y, minsize=250)
        self.item_info_screen.configure(background = self.background_colour)
        itemidlab = Label(self.item_info_screen,
                           text = "ItemID:",
                           fg = "black",
                           font = "Arial 15 bold",
                           bg = self.background_colour).grid(row=1, column=1, sticky = W)
        itemidbox = Entry(self.item_info_screen,
                        font = "Arial 15 italic",
                         width = 7)
        itemidbox.grid(row=1, column=1, sticky = E)
        search_button = Button(self.item_info_screen,
                        fg = "black",
                        font = "Arial 18 italic",
                        text = "Search",
                        width = 10,
                        bg = self.contrast_colour,
                        command = search).grid(row=1, column=2)
        descriptionlab = Label(self.item_info_screen,
                           text = "Description:",
                           fg = "black",
                           font = "Arial 15 bold",
                           bg = self.background_colour).grid(row=2, column=1, sticky = W)
        descriptionbox = Entry(self.item_info_screen,
                        font = "Arial 15 italic",
                         width = 22)
        descriptionbox.grid(row=2, column=1, columnspan=2)
        stocklab = Label(self.item_info_screen,
                           text = "Stock:",
                           fg = "black",
                           font = "Arial 15 bold",
                           bg = self.background_colour).grid(row=2, column=1, sticky = SW)
        stockbox = Entry(self.item_info_screen,
                        font = "Arial 15 italic",
                         width = 10)
        stockbox.grid(row=2, column=1, sticky = SE)
        locationlab = Label(self.item_info_screen,
                           text = "Location:",
                           fg = "black",
                           font = "Arial 15 bold",
                           bg = self.background_colour).grid(row=3, column=1, sticky = NW)
        locationbox = Entry(self.item_info_screen,
                        font = "Arial 15 italic",
                         width = 10)
        locationbox.grid(row=3, column=1, sticky = NE)
        usedlocations = db.get_used_locations()
        unused = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5', 'C1', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'E5', 'F1', 'F5', 'G1', 'G2', 'G3', 'G4', 'G5', 'H1', 'H2', 'H3', 'H4', 'H5']
        for x in unused:
            if x in usedlocations:
                unused.remove(x)
        print(unused)
        barcodelab = Label(self.item_info_screen,
                           text = "Barcode:",
                           fg = "black",
                           font = "Arial 15 bold",
                           bg = self.background_colour).grid(row=3, column=1, sticky = SW)
        barcodebox = Entry(self.item_info_screen,
                        font = "Arial 15 italic",
                         width = 10)
        barcodebox.grid(row=3, column=1, sticky = SE)
        weightlab = Label(self.item_info_screen,
                           text = "Weight:",
                           fg = "black",
                           font = "Arial 15 bold",
                           bg = self.background_colour).grid(row=4, column=1, sticky = NW)
        weightbox = Entry(self.item_info_screen,
                        font = "Arial 15 italic",
                         width = 10)
        weightbox.grid(row=4, column=1, sticky = NE)
        
        updatebutton = Button(self.item_info_screen,
                               fg = "black",
                               font = "Arial 15 italic",
                               text = "Update",
                               width = 8,
                               bg = self.contrast_colour,
                               command = lambda: validate("update")).grid(row=4, column=1, sticky = W)
        newbutton = Button(self.item_info_screen,
                        fg = "black",
                        font = "Arial 15 italic",
                        text = "Add New Item",
                        width = 10,
                        bg = self.contrast_colour,
                        command = lambda: validate("new")).grid(row=4, column=1, sticky = E)
        newbarcodebutton = Button(self.item_info_screen,
                        fg = "black",
                        font = "Arial 18 italic",
                        text = "Scan New\nBarcode",
                        width = 10,
                        bg = self.contrast_colour,
                        command = scan_new_barcode).grid(row=3, column=0)
        searchbarcodebutton = Button(self.item_info_screen,
                        fg = "black",
                        font = "Arial 15 italic",
                        text = "Search by Barcode",
                        width = 15,
                        bg = self.contrast_colour,
                        command = searchbarcode).grid(row=2, column=0)
        self.initialise_buttons(self.item_info_screen)
        self.item_info_screen.tkraise()      
                           
    def initialise_view_orders_screen(self):
        db.remove_blanks()
        def showitems():
            itemslistbox.delete(0, END)
            orderid = orderslistbox.get(ACTIVE)
            orderitems = db.get_orderitems(orderid[0])
            for x in orderitems:
                description = db.get_item_singleinfo(x[0],"ItemDescription")
                string = (x[1]+" * "+description)
                itemslistbox.insert(0, string)
        self.view_orders_screen.grid(row=4, column=2)
        for x in range(0,5):
            self.view_orders_screen.grid_rowconfigure(x, minsize = 100)
        for y in range(0,3):
            self.view_orders_screen.grid_columnconfigure(y, minsize=250)
        self.view_orders_screen.configure(background = self.background_colour)
        scrollbar = Scrollbar(self.view_orders_screen)
        scrollbar.grid(row=2, column = 0, rowspan = 2, sticky = E)
        orderslistbox = Listbox(self.view_orders_screen)
        orderslistbox.grid(row=2, column = 0, rowspan = 2)
        orderslistbox.config(yscrollcommand=scrollbar.set,
                       width =25,
                       height=10,
                       font = "Arial 10")
        scrollbar.config(command=orderslistbox.yview)
        for x in db.select_main():
            orderslistbox.insert(END, x)
        showbutton = Button(self.view_orders_screen,
                        fg = "black",
                        font = "Arial 15 italic",
                        text = "Show Order >>>",
                        width = 15,
                        bg = self.contrast_colour,
                        command=showitems).grid(row=2, column=1)
        itemslistbox = Listbox(self.view_orders_screen)
        itemslistbox.grid(row=2, column = 2, rowspan = 2)
        itemslistbox.config(yscrollcommand=scrollbar.set,
                       width =25,
                       height=10,
                       font = "Arial 10")
        self.initialise_buttons(self.view_orders_screen)
        self.view_orders_screen.tkraise()

    def initialise_warehouse_improvements_screen(self):
        def get_improvements():
            improvements = imp.get_improvements()
            string = ""
            for x in improvements:
                string += ("\n" + str(x) + " -> " + str(improvements[x]))
            message = ("Do you wish to make\nthe following changes?\n"+str(string))
            if messagebox.askyesno("Proceed", message):
                for x in improvements:
                    itemid = db.get_id_location(x)
                    db.update_location(itemid, improvements[x])
                messagebox.showinfo("Success", "Item Locations Optimised\nSuccessfully")

        self.warehouse_improvements_screen.grid(row=4, column=2)
        for x in range(0,5):
            self.warehouse_improvements_screen.grid_rowconfigure(x, minsize = 100)
        for y in range(0,3):
            self.warehouse_improvements_screen.grid_columnconfigure(y, minsize=250)
        self.warehouse_improvements_screen.configure(background = self.background_colour)
        data = db.get_order_analysis()
        orderstring = ("Number of Orders: " + str(data[1]))
        orderslabel = Label(self.warehouse_improvements_screen,
                           text = orderstring,
                           fg = "black",
                           font = "Arial 15 bold",
                           bg = self.background_colour).grid(row=1, column=1, sticky = N)
        itemstring = ("Number of Items Picked: " + str(data[0]))
        orderslabel = Label(self.warehouse_improvements_screen,
                           text = itemstring,
                           fg = "black",
                           font = "Arial 15 bold",
                           bg = self.background_colour).grid(row=1, column=1)
        listboxlabel = Label(self.warehouse_improvements_screen,
                           text = "Items in Decending order of Popularity:",
                           fg = "black",
                           font = "Arial 10",
                           bg = self.background_colour).grid(row=2, column=1, sticky=N)
        scrollbar = Scrollbar(self.warehouse_improvements_screen)
        scrollbar.grid(row=2, column = 1, rowspan = 2, sticky = E)
        orderslistbox = Listbox(self.warehouse_improvements_screen)
        orderslistbox.grid(row=2, column = 1, rowspan = 2, sticky=S)
        orderslistbox.config(yscrollcommand=scrollbar.set,
                       width =25,
                       height=10,
                       font = "Arial 10")
        scrollbar.config(command=orderslistbox.yview)
        title = ("ItemID:    Quantity:")
        orderslistbox.insert(END, title)
        import operator         
        for x in data[2]:
            string = (str(x[0]) + " "*int(15-(len(str(x[0]))+2)) + str(x[1]))
            orderslistbox.insert(END, string)
        improvements_button = Button(self.warehouse_improvements_screen,
                        fg = "black",
                        font = "Arial 12",
                        text = "Get Suggested\nWarehouse Improvements",
                        width = 20,
                        bg = self.contrast_colour,
                        command = get_improvements).grid(row=1, column=0)
        self.initialise_buttons(self.warehouse_improvements_screen)
        self.warehouse_improvements_screen.tkraise()
        
    def emergency_stop(self):
        messagebox.showerror("Alert", "Emergency Stop Activated")

userint = ui()
userint.initialise_root()

while True:
    mainloop()
