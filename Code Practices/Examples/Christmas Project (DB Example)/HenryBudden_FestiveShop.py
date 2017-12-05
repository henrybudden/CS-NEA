import sqlite3

def create_table(db_name, table_name, sql):
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()
        cursor.execute("select name from sqlite_master where name=?", (table_name,))
        result = cursor.fetchall()
        keep_table = True
        if len(result) == 1:
            response = input("The table {0} already exists, do you wish to recreate it? (y/n): ".format(table_name))
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
            cursor.execute(sql)
            db.commit()

def insert_product_data(values):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        sql = "insert into Products (Category, Name, Price, Stock) values (?,?,?,?)"
        cursor.execute(sql, values)
        db.commit()

def insert_customer_data(values):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        sql = "insert into Customers (FirstName, LastName, Gender) values (?,?,?)"
        cursor.execute(sql, values)
        db.commit()

def insert_order_data(values):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        sql = "insert into Orders (CustomerID, ProductName, Quantity, TotalCost) values (?,?,?,?)"
        cursor.execute(sql, values)
        db.commit()

def update_stock(data):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        sql = "update Products set Stock=? where ProductID=?"
        cursor.execute(sql, data)
        db.commit()

def update_customer(data):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        sql = "update Customers set FirstName=?, LastName=?, Gender=? where CustomerID=?"
        cursor.execute(sql, data)
        db.commit()

def delete_product(data):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        sql = "delete from Products where ProductID=?"
        cursor.execute(sql, data)
        db.commit()

def delete_customer(data):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        sql = "delete from Customers where CustomerID=?"
        cursor.execute(sql, data)
        db.commit()

def select_all(table_name):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from {0}".format(table_name))
        everything = cursor.fetchall()
        return everything

def select_in_stock_products():
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from Products where stock > 0")
        products = cursor.fetchall()
        return products
    
def select_products_category(category):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        if category == "Decorations":
            cursor.execute("select * from Products where Category = 'Decorations'")
        elif category == "Electricals":
            cursor.execute("select * from Products where Category = 'Electricals'")
        elif category == "Food":
            cursor.execute("select * from Products where Category = 'Food'")
        products = cursor.fetchall()
        return products

def select_product_info(info, product_id):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        if info == "Stock":
            cursor.execute("select Stock from Products where ProductID=?", (product_id,))
        elif info == "Name":
            cursor.execute("select Name from Products where ProductID=?", (product_id,))
        elif info == "Price":
            cursor.execute("select Price from Products where ProductID=?", (product_id,))
        product = cursor.fetchone()
        return product

def select_customer_orders(customer_id):
    with sqlite3.connect("festiveshop.db") as db:
        cursor = db.cursor()
        cursor.execute("select * from Orders where CustomerID=?", (customer_id))
        orders = cursor.fetchall()
        return orders

def print_products(products):
    headers = ("ProductID", "Category", "Name", "Price", "Stock")
    print("\n\n\nProduct Table:\n\n")
    for x in headers:
        print(str(x)+" "*(20-len(str(x))), end="")
    print("\n")
    for x in products:
        counter = 0
        for y in x:
            print(str(y)+" "*(20-len(str(y))), end="")
            counter += 1
            if counter == 5:
                print("")
    print("\n")

def print_customers(customers):
    headers = ("CustomerID", "FirstName", "LastName", "Gender")
    print("\n\n\nCustomer Table:\n\n")
    for x in headers:
        print(str(x)+" "*(20-len(str(x))), end="")
    print("\n")
    for x in customers:
        counter = 0
        for y in x:
            print(str(y)+" "*(20-len(str(y))), end="")
            counter += 1
            if counter == 4:
                print("")
    print("\n")

def print_orders(orders):
    headers = ("OrderID", "CustomerID", "Product Name", "Quantity", "Total Cost")
    print("\n\n\nOrder Table:\n\n")
    for x in headers:
        print(str(x)+" "*(20-len(str(x))), end="")
    print("\n")
    for x in orders:
        counter = 0
        for y in x:
            print(str(y)+" "*(20-len(str(y))), end="")
            counter += 1
            if counter == 5:
                print("")
    print("\n")

if __name__ == "__main__":

    print("Welcome to the Festive Shop!")
    
    while True:
        try:
            print("\nMain Menu:\n\n1. Product Options\n2. Customer Options\n3. Order Options\n0. Exit")
            option = int(input("\nSelect an Option: > "))
            if option > 3 or option < 0:
                print("\n Invalid Option")



            if option == 1:         #Product Options

                
                print("\n\nProduct Menu:\n\n1. (Re)Create Product Table\n2. View Products\n3. Add New Product\n4. Edit Stock Level\n5. Delete Existing Product\n0. Go Back")
                option = int(input("\nSelect an option > "))
                if option > 5 or option < 0 :
                    print("\nInvalid Option")


                    
                elif option == 1:                                       #Recreate products table

                    db_name = 'festiveshop.db'
                    sql = """ CREATE TABLE Products(
                    ProductID integer,
                    Category text, 
                    Name text,
                    Price real,
                    Stock integer,
                    Primary Key(ProductID))"""
                    create_table(db_name, "Products", sql)



                elif option == 2:                                       #View Products

                    choice = int(input("\n\n1. All\n2. In Stock\n3. By Category\n0. Go Back\n\n> "))
                    if choice > 3 or choice < 0:
                        print("\nInvalid Option")

                    elif choice == 1:
                        products = select_all("Products")
                        print_products(products)

                    elif choice == 2:
                        products = select_in_stock_products()
                        print_products(products)

                    elif choice == 3:
                        category = int(input("\n\n1. Decorations\n2. Electricals\n3. Food\n0. Go Back\n> "))
                        if category > 3 or category < 0:
                            print("\nInvalid Option")

                        elif category == 1:
                            products = select_products_category("Decorations")
                            print_products(products)

                        elif category == 2:
                            products = select_products_category("Electricals")
                            print_products(products)

                        elif category == 3:
                            products = select_products_category("Food")
                            print_products(products)
                    

                    
                elif option == 3:                                       #Add new product

                    name = input("Enter the name of the new product: ")
                    category_choice = int(input("Enter the category of the new product:\n1. Decorations\n2. Electricals\n3. Food\n\n> "))
                    if category_choice == 1:
                        category = "Decorations"
                    elif category_choice == 2:
                        category = "Electricals"
                    elif category_choice == 3:
                        category = "Food"
                    else:
                        print("Invalid Input")
                        break
                    price = input("Enter the price of the new product: ")
                    stock = input("Enter the stock level of the new product: ")
                    product = (category, name, price, stock)
                    insert_product_data(product)



                elif option == 4:                                       #Edit Stock level 

                    products = select_all("Products")
                    print_products(products)
                    ProductID = int(input("Enter the ProductID of the Item: "))
                    for x in select_product_info("Stock", ProductID):
                        stock_level = x
                    print("\nThe current stock level is", stock_level, "units.")
                    choice = int(input("\nChoose method of stock change:\n1. Sale (Decrease Stock)\n2. Delivery (Increase Stock)\n\n> "))
                    if choice == 1:
                        decrease = int(input("Enter the number of items sold: "))
                        if decrease > stock_level:
                            warning = input(("WARNING: You are attempting to sell more products than you have available. Continue? y/n: "))
                            if warning == "y":
                                continue
                            else:
                                break  
                        new_stock = stock_level - decrease
                    elif choice == 2:
                        increase = int(input("Enter the number of items delivered: "))
                        new_stock = stock_level + increase
                    data = (new_stock, ProductID)
                    update_stock(data)
                    for x in select_product_info("Stock", ProductID):
                        stock_level = x
                    print("\nThe current stock level is", stock_level, "units.")



                elif option == 5:                                       #Delete existing product

                    products = select_all("Products")
                    print_products(products)
                    ProductID = int(input("Enter the ProductID of the product you wish to remove: "))
                    data = (ProductID,)
                    delete_product(data)







            elif option == 2:       #Customer Options


                print("\n\nCustomer Menu:\n\n1. (Re)Create Customer Table\n2. View Customer Table\n3. View Customer's Order History\n4. Add New Customer\n5. Edit Customer Detials\n6. Delete Existing Customer\n0. Go Back")
                option = int(input("\nSelect an option > "))
                if option > 6 or option < 0 :
                    print("\nInvalid Option")



                if option == 1:                                         #(Re)Create Customer Table

                    db_name = 'festiveshop.db'
                    sql = """ CREATE TABLE Customers(
                    CustomerID integer,
                    FirstName text, 
                    LastName text,
                    Gender text,
                    Primary Key(CustomerID))"""
                    create_table(db_name, "Customers", sql)


                if option == 2:                                         #View Customer List

                    customers = select_all("Customers")
                    print_customers(customers)


                if option == 3:                                         #View Order History

                    customers = select_all("Customers")
                    print_customers(customers)
                    customer_id = input("Enter the Customer's CustomerID: ")
                    orders = select_customer_orders(customer_id)
                    print_orders(orders)

                if option == 4:                                         #Add New Customer

                    first_name = input("Enter the First Name of the new Customer: ")
                    last_name = input("Enter the Last Name of the new Customer: ")
                    gender = input("Enter the Gender of the new Customer: ")
                    customer = (first_name, last_name, gender)
                    insert_customer_data(customer)

        
                if option == 5:                                         #Edit Customer Details

                    customers = select_all("Customers")
                    print_customers(customers)
                    customer_id = int(input("Enter the Customer's CustomerID: "))
                    new_first_name = input("Enter the Customer's new First Name: ")
                    new_last_name = input("Enter the Customer's new Last Name: ")
                    new_gender = input("Enter the Customer's new Gender: ")
                    data = (new_first_name, new_last_name, new_gender, customer_id)
                    update_customer(data)


                if option == 6:                                         #Delete Existing Customer

                    customers = select_all("Customers")
                    print_customers(customers)
                    CustomerID = int(input("Enter the Customer's CutomerID that you wish to remove: "))
                    data = (CustomerID,)
                    delete_customer(data)





                    

            elif option == 3:       #Order Options

                
                print("\n\Orders Menu:\n\n1. (Re)Create Order Table\n2. View Order Table\n3. Make an Order\n0. Go Back")
                option = int(input("\nSelect an option > "))
                if option > 3 or option < 0 :
                    print("\nInvalid Option")


                elif option == 1:                               #(Re)Create Orders Table

                    db_name = 'festiveshop.db'
                    sql = """ CREATE TABLE Orders(
                    OrderID integer,
                    CustomerID integer,
                    ProductName text,
                    Quantity integer,
                    TotalCost integer,
                    Primary Key(OrderID)
                    Foreign Key(CustomerID) references Customers(CustomerID))"""
                    create_table(db_name, "Orders", sql)


                elif option == 2:                               #View Order Table

                    orders = select_all("Orders")
                    print_orders(orders)
                    

                elif option == 3:                               #Make an Order

                    customers = select_all("Customers")
                    print_customers(customers)
                    customer_id = int(input("Enter the Customer's CustomerID: "))
                    products = select_in_stock_products()
                    print_products(products)
                    product_id= int(input("Enter the ProductID of the product to be ordered: "))
                    for x in select_product_info("Stock", product_id):
                        stock_level = x
                    quantity = int(input("Enter the quantity to be ordered: "))
                    if quantity > stock_level:
                        print("WARNING: You cannot order more than the current stock level (",stock_level,").")
                        continue
                    for x in select_product_info("Name", product_id):
                        product_name = x
                    for x in select_product_info("Price", product_id):
                        price = x  
                    total_cost = price * quantity
                    order = (customer_id, product_name, quantity, total_cost)
                    insert_order_data(order)
                    new_stock = stock_level - quantity
                    data = (new_stock, product_id)
                    update_stock(data)
                    print("Order Successful")
                    
            else:
                exit()
                
        except:
            print("\nERROR: Invalid Selection")
            continue
