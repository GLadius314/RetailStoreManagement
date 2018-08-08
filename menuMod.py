import custMod
import adminMod
import sys

def cls():
    print("\n" * 2)

bill_id = 0
    
def userMenu():
    print('=========Welcome to SAP Retail Store=========')
    print()


    userOption =int(input('''Please select your option:
    1. Admin
    2. Customer
    3. Exit

option(1/2/3): '''))
    if userOption == 1:
        admin = adminMod.Administration()             #admin object created
        admin.validate()
        cls()
        userMenu()

    elif userOption == 2:
        print()
        print('''Are you:
    1. Existing customer
    2. New customer''')

    

        custOption = int(input("option(1/2): "))
        if (custOption == 1):
              global bill_id
              bill_id = bill_id + 1
              customer = custMod.Customer()         #customer object created
              customer.validate(bill_id)
              cls()
              userMenu()
        elif (custOption == 2):
              customer = custMod.Customer()
              customer.regNew()
              cls()
              userMenu()
        else:
              print("Invalid option entered. Try again!")
              cls()
              userMenu()
              
        
    elif userOption == 3:
        sys.exit("Exiting program")
        
    else:
        print("Invalid option entered, Try again!")
        cls()
        userMenu()

userMenu()
