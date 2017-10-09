import sqlite3
import datetime

class Database: #Create class for all database functions. 

    def __init__(self): #No class variables needed
        pass

                
    def execute(self, sql, values):      
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()
        
    def select_all(self, table_name):   #Returns all data from all records from a certain table, as passed as a parameter
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select * from {0}".format(table_name))
            everything = cursor.fetchall()
            return everything

    def create_table(self, db_name, table_name, sql):  #Funtion to create a new table when given the sql statement needed 
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("select name from sqlite_master where name=?", (table_name,))    #Checks if a table with the same name alredy exists
            result = cursor.fetchall()
            keep_table = True
            if len(result) == 1:
                response = input("The table {0} already exists, do you wish to recreate it? (y/n): ".format(table_name)) #User prompted if a table with the same name already exists
                if response == "y":
                    keep_table = False
                    print("The {0} table will be recreated  - all existing data will be lost".format(table_name))
                    cursor.execute("drop table if exists {0}".format(table_name))
                    db.commit
                else:
                    print("The existing table was kept")
            else:
                keep_table = False
            if not keep_table:
                cursor.execute(sql) #Runs sql statement that has been passed to function through 'sql' variable
                db.commit()

    def restart_tables(self):   #Function to restart all three tables; ITEMS, ORDERS and ORDERITEMS
        db_name = 'warehouse.db' #warehouse.db to be standard database filename throughout project
        sql = """ CREATE TABLE ITEMS(
        ItemID integer,
        ItemDescription text, 
        ItemStock text,
        ItemLocation text,
        ItemBarcode text,
        ItemWeight text,
        Primary Key(ItemID))"""
        self.create_table(db_name, "ITEMS", sql)    #Creates ITEMS table with primary key set to ItemID field
        db_name = 'warehouse.db'
        sql = """ CREATE TABLE ORDERS(
        OrderID integer,
        OrderTime text, 
        CompletedTime text,
        Duration text,
        Primary Key(OrderID))"""
        self.create_table(db_name, "ORDERS", sql) #Creates ORDERS table with OrderID as primary key
        db_name = 'warehouse.db'
        sql = """ CREATE TABLE ORDERITEMS(
        OrderItemID integer,
        OrderID integer, 
        ItemID integer,
        OrderItemQuantity text,
        OrderItemPicked boolean,
        Primary Key(OrderItemID)
        Foreign Key(OrderID) references ORDERS(OrderID)
        Foreign Key(ItemID) references ITEMS(ItemID))"""
        self.create_table(db_name, "ORDERITEMS", sql) #Creates a relational ORDERITEMS table with primary key as OrderItemID and OrderID and ItemID as forign keys linking to ORDERS and ITEMS tables

    def insert_data(self, table_name): #Function to add a new item to the ITEMS table
        if table_name == "ITEMS":
            name = input("Enter the description of the new product: ")  #Prompts for item info
            stock = input("Enter the stock level of the new product: ")
            location = input("Enter the location of the new product: ")
            barcode = input("Enter the barcode number of the new product: ")
            weight = input("Enter the items weight (g): ")
            values = (name, stock, location, barcode, weight)
            sql = "insert into ITEMS(ItemDescription, ItemStock, ItemLocation, ItemBarcode, ItemWeight) values (?,?,?,?,?)"
            self.execute(sql, values)
            print("Item added succesfully")
            
        if table_name == "ORDERS":
            order_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            #print(order_time)
            more = True
            items = {}
            while more == True:
                item = input("Enter the item ID of an item to be added to the order: ")
                quantity = input("Enter the desired quantity of the item to be added to the order: ")
                items[item] = quantity
                choice = input("Do you want to add another item? y/n ")
                if choice == "n":
                    more = False
            values = (order_time,)
            sql = "insert into ORDERS(OrderTime) values (?)"
            self.execute(sql, values)
            self.insert_orderitem(order_time, items)
            print("Order added succesfully")

    def insert_orderitem(self, order_time, items):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select OrderID from ORDERS where OrderTime=?", (order_time,))
            ID_list = cursor.fetchall()
            ID = ID_list[0][0]
        for x in items:
            values = (ID, str(x), items[x])
            sql = "insert into ORDERITEMS(OrderID, ItemID, OrderItemQuantity) values (?,?,?)"
            self.execute(sql, values)

    def print_all(self, table_name): #Prints all items as a well formatted table
        if table_name == "ITEMS":
            headers = ("ItemID", "Item Description", "Stock", "Location", "Barcode Number", "Weight")
            print("\n\n\nItem Table:\n\n")
        elif table_name == "ORDERS":
            headers = ("OrderID", "OrderTime", "Completed Time", "Duration")
            print("\n\n\nOrder Table:\n\n")
        for x in headers:
            print(str(x)+" "*(30-len(str(x))), end="")
        print("\n")
        records = self.select_all(table_name) #Calls select_all function to gather all info on all records in the ITEMS table
        for x in records:
            counter = 0
            for y in x:
                print(str(y)+" "*(30-len(str(y))), end="")
                counter += 1
                if counter == len(headers):
                    print("")
        print("\n")

    def edit_data(self, table_name):
        if table_name == "ITEMS":
            ID_field = "ItemID"
            ID = int(input("Enter the ItemID: "))
            choice = int(input("\nWhich field would you like to update?\n1:Item Description\n2:Stock\n3:Location\n4:Barcode Number\n5:Weight\n\n>"))
            if choice == 1:
                field = "ItemDescription"
            elif choice == 2:
                field = "ItemStock"
            elif choice == 3:
                field = "ItemLocation"
            elif choice == 4:
                field = "ItemBarcode"
            elif choice == 5:
                field = "ItemWeight"
        data = input("Enter the new data: ")
        sql = ("update %s set %s=? where %s=?" % (table_name, field, ID_field))
        values = (data, ID)
        self.execute(sql, values)

    def delete_record(self, table_name):
        if table_name == "ITEMS":
            ID_field = "ItemID"
        elif table_name == "ORDERS":
            ID_field = "OrderID"
        ID = input("Enter the ID of the record you wish to remove: ")
        sql = ("delete from %s where %s=?" % (table_name, ID_field))
        values = (ID,)
        self.execute(sql, values)


#print(datetime.datetime.now())
#test = Database()
#test.delete_record("ORDERS")
#test.delete_record("ITEMS")
