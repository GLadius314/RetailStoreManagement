import mysql.connector
from mysql.connector import Error
from prettytable import from_db_cursor
from userMod import User
from datetime import date
import time

try:
    con = mysql.connector.connect(host = 'localhost', db = 'practice', user = 'root', password = 'password')
    cur = con.cursor()
except Error as e:
    print(e)

def cls():
    print("\n" * 2)

class Customer(User):
    
    def __init__(self):
        print("Welcome Customer !")


    def regNew(self):
        name = input("Enter your name:")
        dor = str(date.today().strftime('%Y/%m/%d'))
        cid = "null"
        try:
            sql = ("INSERT INTO Customer values (null, %s, %s)")  #Adds the customer with customer name, DOR and auto customer ID
            cur.execute(sql,(name, dor))
            print("New customer account created") 
            cur.execute("SELECT * from customer where Name = %s", (name,))
            res = from_db_cursor(cur)
            print("Your recorded info is: ")
            print(res)
            print("Kindly remember the customer ID (ID) for future reference")
            cls()
        except Error as e:
            print(e)

    def validate(self, bill_id):
        self.bill_id = bill_id
        try:
            cur.execute("SELECT ID FROM customer")
            flag = 0
            entered_cid = int(input("Enter your cid: "))
            for value in cur.fetchall():
                if entered_cid == value[0]:
                    print("Hello, ", entered_cid)
                    flag = 1
                    cls()
                    self.rateMenu(entered_cid, bill_id)
                    break
                   
            if flag == 0:
               print("Invalid customer ID, try again !!!")
               cls()
               self.validate(bill_id)

        except Error as e:
            print(e)

    def rateMenu(self, cid, bill_id):
        self.bill_id = bill_id
        self.cid = cid
        print("This is our product list:")
        try:
            cur.execute("SELECT Product_Name, Price, GST FROM Product")
            y = from_db_cursor(cur)
            print(y)
            cls()
        except Error as e:
            print(e)

        buy = input("Want to buy? (y/n): ").lower()
        if buy == 'y':
            if 1!= 0:                                                         # do condition of do while loop implementation
                cls()
                self.currentBuy(cid, bill_id)
                cls()
                while True:
                    buyMore = input("Want to buy more ? (y/n): ").lower()
                    if buyMore == 'y':
                        cls()
                        self.currentBuy(cid, bill_id)
                        continue
                    else:
                        break
            else:
                pass
        else:
            pass

        if buy == 'y':
            self.bill(cid, bill_id)
        else:
            print("Nothing ordered")

    def currentBuy(self, cid, bill_id):
        self.bill_id = bill_id
        self.cid = cid
        productBuy = input("Which product do you want to buy? Enter from rate menu: ")
        quantityBuy = int(input("Enter quantity to buy: "))

        #query1 (check entered product name matches one of in product table)
        try:
            cur.execute("SELECT Product_Name FROM Product")
            flag = 0
            for value in cur.fetchall():
                if productBuy == value[0]:
                    cur.execute("SELECT Quantity FROM Product WHERE Product_Name = %s",(productBuy,))
                    q = cur.fetchone()[0]
                    updated_quantity = q - quantityBuy
                    if updated_quantity < 0:                       #query2 (check quantity enetred does not become negative after dec it from current quantity in product table of respective product
                        print("Not sufficient stock")              #if quantity becomes negative print "not sufficient stock"
                        print("Try again with lower quantity")
                        cls()
                        self.currentBuy(cid, bill_id)
            
                    else:
                        cur.execute("UPDATE product set Quantity = %s",(updated_quantity,))
 
                        #now fetching all required info one by one to calculate gst and enter info into buys table
                        cur.execute("SELECT Product_ID FROM Product WHERE Product_Name = %s",(productBuy,))
                        pid = cur.fetchone()[0]
                        cur.execute("SELECT Price FROM Product WHERE Product_Name = %s",(productBuy,))
                        price = cur.fetchone()[0]
                        cur.execute("SELECT GST FROM Product WHERE Product_Name = %s",(productBuy,))
                        GST = cur.fetchone()[0]
                        product_amt = quantityBuy * price
                        total_gst = (GST/100) * product_amt
                        final_amt = product_amt + total_gst
                        print("Amount for selected item(s): ",final_amt)                        #query3 (insert these entered values into buys table)
                        cur.execute("INSERT INTO buys VALUES(null, %s, %s, %s ,%s ,%s ,%s ,%s, %s)",(bill_id, cid, pid, productBuy, quantityBuy, product_amt, total_gst, final_amt))
                        con.commit()

                    flag = 1            
                    break

            if flag == 0:                                      #if print invalid product name enter again and call currentBuy() again
                print("Invalid Product name! Try again.")
                cls()
                self.currentBuy(cid, bill_id)                           #call currentBuy() again

        except Error as e:
            print(e)

    def bill(self, cid, bill_id):
        self.bill_id = bill_id
        self.cid = cid
        try:
            cur.execute("select Bill_id, Customer_id, Product_id, Product_name, Quantity, Product_amount, GST, Final_amount from buys group by Product_id  having Bill_id = %s order by Quantity",(bill_id,))#query4 (fetch products ordered with quantity, group by pid)
            x = from_db_cursor(cur)
            print(x)
            cls()
            cur.execute("SELECT sum(Final_amount) FROM buys") #query5 (fetch final amount with gst (sum of all rows))
            print("Total bill amount:",cur.fetchone()[0])
            print("Thank you for shopping with us !!")

        except Error as e:
            print(e)




        




    
    
    
    
                       
        
        
                

            
            
    
        
