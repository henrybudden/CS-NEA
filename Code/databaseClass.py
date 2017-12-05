import sqlite3
import datetime
import operator

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

    def select_main(self):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select OrderID, OrderTime from ORDERS")
            everything = cursor.fetchall()
            return everything

    def get_used_locations(self):
        locations = []
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select ItemLocation from ITEMS")
            description = cursor.fetchall()
            for x in description:
                locations.append(x[0])
            return locations

    def get_used_barcodes(self):
        barcodes = []
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select ItemBarcode from ITEMS")
            codes = cursor.fetchall()
            for x in codes:
                barcodes.append(x[0])
            return barcodes

    def insert_order(self): 
        order_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        values = (order_time,)
        sql = "insert into ORDERS(OrderTime) values (?)"
        self.execute(sql, values)
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select OrderID from ORDERS where OrderTime=?", (order_time,))
            description = cursor.fetchone()
            return description[0]        

    def insert_item(self, ItemDescription, ItemStock, ItemLocation, ItemBarcode, ItemWeight):
        values = (ItemDescription, ItemStock, ItemLocation, ItemBarcode, ItemWeight)
        sql = "insert into ITEMS(ItemDescription, ItemStock, ItemLocation, ItemBarcode, ItemWeight) values (?,?,?,?,?)"
        self.execute(sql, values)
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select ItemID from ITEMS where ItemDescription=?", (ItemDescription,))
            description = cursor.fetchone()
            return description[0]
        
    def insert_order_complete_time(self,orderid):
        order_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("update ORDERS set CompletedTime=? where OrderID=?", (order_time,orderid))
            db.commit()

    def remove_blanks(self):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("delete from ORDERS where CompletedTime is NULL")
            db.commit()

    def insert_orderitem(self, order_id, item_id, quantity):
        values = (order_id, item_id, quantity)
        sql = "insert into ORDERITEMS(OrderID, ItemID, OrderItemQuantity) values (?,?,?)"
        self.execute(sql, values)

    def update_item(self, itemid, description, stock, location, barcode, weight):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("update ITEMS set ItemDescription=?, ItemStock=?, ItemLocation=?, ItemBarcode=?, ItemWeight=? where ItemID=?",(description, stock, location, barcode, weight, itemid))
            db.commit()

    def get_item_singleinfo(self, ItemID, field):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select %s from Items where ItemID=?" % (field,), (ItemID,))
            description = cursor.fetchone()
            try:
                return description[0]
            except:
                return description

    def get_item_info(self, ItemID):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select ItemDescription, ItemStock, ItemLocation, ItemBarcode, ItemWeight from Items where ItemID=?", (ItemID,))
            description = cursor.fetchall()
            return description

    def get_item_info_barcode(self, barcode):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select ItemID, ItemDescription, ItemStock, ItemLocation, ItemWeight from Items where ItemBarcode=?", (barcode,))
            description = cursor.fetchall()
            return description
        
    def update_stock(self, itemid, change):
        oldstock = self.get_item_singleinfo(itemid, "ItemStock")
        newstock = int(oldstock) - int(change)
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("update ITEMS set ItemStock=? where ItemID=?",(newstock, itemid))
            db.commit()

    def get_orderitems(self, orderid):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select ItemID, OrderItemQuantity from ORDERITEMS where OrderID=?", (orderid,))
            description = cursor.fetchall()
            return description

    def get_order_analysis(self):
        items = {}
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select OrderID from ORDERS")
            orderids = cursor.fetchall()
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select ItemID, OrderItemQuantity from ORDERITEMS")
            itemids = cursor.fetchall()
        no_items = 0
        for x in itemids:
            no_items += int(x[1])
        no_orders = len(orderids)
        for x in itemids:
            if x[0] in items:
                items[x[0]] += int(x[1])
            else:
                items[x[0]] = int(x[1])
        return(no_items, no_orders, sorted(items.items(), key=operator.itemgetter(1), reverse=True))


    def get_id_location(self, location):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("select ItemID from ITEMS where ItemLocation=?", (location,))
            itemid = cursor.fetchone()
            return itemid[0]

    def update_location(self, itemid, location):
        with sqlite3.connect("warehouse.db") as db:
            cursor = db.cursor()
            cursor.execute("update ITEMS set ItemLocation=? where ItemID=?",(location, itemid))
            db.commit()
            

