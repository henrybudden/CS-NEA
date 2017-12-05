from databaseClass import *  #Import class Database from database.py
db = Database() #Instantiate class Database as db

print("Welcome to the Warehouse management system!")
while True:
    try:
        print("\nMain Menu:\n\n1. Database Options\n2. Item Options\n3. Order Options")    #Main menu options
        option = int(input("\nSelect an Option: > "))
        if option > 3 or option < 1:    #If choice out of range
            print("\nInvalid Option")
        elif option == 1:
            print("\nDatabase Menu:\n\n1. Restart all tables\n0. Exit") #Database menu options
            option = int(input("\nSelect an Option: > "))
            if option >1 or option <0:
                print("\n Invalid Option")
            elif option == 1:
                db.restart_tables() #Reset all three tables
        elif option == 2:
            print("\nItem Menu:\n\n1. View Items\n2. Add new Item\n3. Edit Item\n4. Delete Item\n0. Exit")  #Item menu options
            option = int(input("\nSelect an Option: > "))
            if option >4 or option <0:
                print("\nInvalid Option")
            elif option == 1:
                db.print_all("ITEMS")    #Print a list of all items in tabular form
            elif option == 2:
                db.insert_data("ITEMS")   #Add a new item
            elif option == 3:
                db.edit_data("ITEMS")     #Edit item data
            elif option == 4:
                db.delete_record("ITEMS")        #Remove item completely
        elif option == 3:
            print("\nOrder Menu:\n\n1. View Orders\n2. Add new Order\n0. Exit")  #Item menu options
            option = int(input("\nSelect an Option: > "))
            if option >2 or option <0:
                print("\nInvalid Option")
            elif option == 1:
                db.print_all("ORDERS")
            elif option == 2:
                db.insert_data("ORDERS")
            #elif option == 3:
                
    except: #If choice not integer
        print("Error. Please only enter a numeric value from the menu choices.")

