import mysql.connector
from mysql.connector import Error
import sys
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

class Administration(User):

      
   def __init__(self):
      print("Welcome Admin!")
      
   def valid_cid(self, cid):
      try:
         cur.execute("SELECT ID FROM customer")
         flag = 0
         for value in cur.fetchall():
            if cid == value[0]:
               flag = 1
               return True
         if flag == 0:
            return False
      except Error as e:
         print(e)

   def valid_pid(self, pid):
      try:
         cur.execute("SELECT Product_ID FROM product")
         flag = 0
         for value in cur.fetchall():
            if pid == value[0]:
               flag = 1
               return True
               break
         if flag == 0:
            return False
      except Error as e:
         print(e)
 
   

   def delete_cust(self):
       
        cid = int(input("Enter customer id:"))
        if self.valid_cid(cid):
           try:
              sql = "DELETE from customer where ID = %s"           # Delete the customer with customer id
              cur.execute(sql,(cid,))
              print("Customer deleted")
              con.commit()
              cls()
              self.manag_cust()
            
           except Error as e:
              print(e)
        else:
           print("Invalid cid, try again!")
           self.manag_cust()
         

   def edit_cust(self):
       
        print('''1.Edit customer name
2.Edit customer's date of registration
3.Return to previous menu''')
        t = int(input("Please enter your choice: "))

        if t == 1:
            cus_id = int(input("Enter the customer id: "))
            if self.valid_cid(cus_id):
               new_name = input("Enter new name: ")
               try:
                  sql = "UPDATE customer SET Name = %s WHERE ID = %s"        # Edits the customer id
                  cur.execute(sql,(new_name, cus_id))
                  print("Name updated")
                  con.commit()
                  cls()
                  self.edit_cust()
               except Error as e:
                  print(e)
            else:
               print("This customer id does not exist. Try again!")
               self.edit_cust()

        elif t == 2:
            cus_id = int(input("Enter customer id: "))
            if self.valid_cid(cus_id):
               new_date = input("Enter new date(yyyy-mm-dd):")
               newdate1 = time.strptime(new_date, "%Y/%m/%d")
               today = str(date.today().strftime('%Y/%m/%d'))
               today1 = time.strptime(today, "%Y/%m/%d")
               if newdate1 > today1:
                  print("Date of registration exceeds today's date. This is not possible. Try again!")
                  self.edit_cust()
               else:
                  try:
                     cur.execute("UPDATE customer SET Date_of_Registration=%s WHERE ID = %s",(new_date, cus_id))      # Edits the customer date of registration
                     print("Date updated")
                     con.commit()
                     cls()
                     self.edit_cust()
                  
                  except Error as e:
                     print (e)
            else:
               print("This customer id does not exist. Try again!")
               self.edit_cust()

        elif t == 3:
            cls()
            self.manag_cust()

        else:
            print("Invalid option entered. Try again!")
            cls()
            self.edit_cust()

   def manag_cust(self):
        print('''1.Edit Customer
2.Delete Customer
3.Return to previous menu''')
        e = int(input("Please enter your Choice: "))
        if(e == 1):
            cls()
            self.edit_cust()
            cls()
        elif(e == 2):
            cls()
            self.delete_cust()
            cls()
        elif(e == 3):
            cls()
            self.adminMenu()
        else:
            print("Invalid option entered. Try again!")
            cls()
            self.manag_cust()

   def add_prod(self):
        
        pid = int(input("Enter product id:"))
        pname = input("Enter product name:")
        cat = input("Enter category to which product belongs:")
        cg = int(input("Enter the GST of the product:"))
        price = int(input("Enter price of the product:"))
        quant = int(input("Enter the Quantity of the product:"))
        if cg<0 or price<0 or quant<0:
           print(''' The following cannot be negative:
                              1. GST
                              2. Price
                              3.Quantity
                           Please check the values you have entered and try again!''')
           self.add_prod()
        else:
           try:
              sql = "INSERT INTO product values(%s, %s, %s, %s, %s, %s)"   # Adds the Product
              cur.execute(sql,(pid, pname, cat, cg, price, quant))
              con.commit()
              print("Product added")
              self.manag_prod()
              
           except Error as e:
              print(e)

   def edit_prod(self):
        
        print('''1. Edit product name
2. Edit category
3. Edit GST  on a category
4. Edit  price
5. Edit quantity
6. Return to previous menu''')
        m = int(input("Please enter your choice:"))

        if m == 1:
           id_p = int(input("Enter product id of the product:"))
           if self.valid_pid(id_p):
              new_pname = input("Enter new name of the product:")
              try:
                 cur.execute("UPDATE product SET Product_Name = %s WHERE Product_ID = %s",(new_pname, id_p))   # Edit Product name
                 con.commit()
                 print("Product updated")
                 cls()
                 self.edit_prod()
              except Error as e:
                 print(e)
           else:
              print("Invalid pid, try again")
              self.edit_prod()
            

        elif m == 2:
            id_p = int(input("Enter product id of the product:"))
            if self.valid_pid(id_p):
               new_cat = input("Enter new category of the product:")
               new_cg = int(input("Enter new category's corresponding GST:"))
               try:
                  cur.execute("UPDATE product SET Category=%s WHERE Product_ID = %s",(new_cat, id_p))  # Edit the category and also edits its corresponding GST
                  cur.execute("UPDATE product SET GST = %s WHERE Product_ID = %s",(new_cg, id_p))
                  con.commit()
                  print("Category updated!")
                  cls()
                  self.edit_prod()
               except Error as e:
                  print(e)
            else:
               print("This product id does not exist. Try again!")
               self.edit_prod()
                    

        elif m == 3:
            id_p = int(input("Enter product id of the product:"))
            if self.valid_pid(id_p):
               new_gst = int(input("Enter GST of the corresponding Product id:"))
               if new_gst<0:
                  print("GST can't be negative!")
                  self.edit_prod()
               else:
                  try:
                     cur.execute("UPDATE product SET GST=%s WHERE Product_ID = %s",(new_gst, id_p))  # Edit GST of the product
                     #con.commit()
                     print("GST updated!")
                     cls()
                     self.edit_prod()
                  except Error as e:
                     print(e)
            else:
               print("This product id does not exist. Try again!")
               self.edit_prod()


        elif m == 4:
            id_p = int(input("Enter product id of the product:"))
            if self.valid_pid(id_p):
               new_price = int(input("Enter the new price of the product:"))
               if new_price<0:
                  print("Price cannot be negative.")
                  self.edit_prod()
               else:
                  try:
                     cur.execute("UPDATE product SET Price=%s WHERE Product_ID = %s",(new_price, id_p))  # Edits price
                     con.commit()
                     print("Price updated!")
                     cls()
                     self.edit_prod()
                  
                  except Error as e:
                     print(e)
            else:
               print("This product id does not exist. Try again!")
               self.edit_prod()

        elif m == 5:
                id_p = int(input("Enter product id of the product:"))
                if self.valid_pid(id_p):
                   new_q = int(input("Enter new quantity of the product:"))
                   if new_q<0:
                      print("Quantity can't be negative")
                      self.edit_prod()
                   else:
                      try:
                         cur.execute("UPDATE product SET Quantity=%s WHERE Product_ID = %s",(new_q, id_p))  # Edits Product quantity
                         #con.commit()
                         print("Quantity updated!")
                         cls()
                         self.edit_prod()

                      except Error as e:
                         print(e)
                else:
                   print("This product id does not exist. Try again!")
                   self.edit_prod()

        elif m == 6:
            cls()
            self.manag_prod()
            
        else:
            print("Invalid option entered, please try again!")
            cls()
            self.edit_prod()

                
   def manag_prod(self):
        print('''1.Add Product
2.Edit Product
3.Return to previous menu''')
        f= int(input("please Enter your Choice:"))
        if(f == 1):
            cls()
            self.add_prod()
            cls()
        elif(f == 2):
            cls()
            self.edit_prod()
            cls()
        elif(f == 3):
            cls()
            self.adminMenu()
        else:
            print("Invalid option entered, please try again!")
            cls()
            self.manag_prod()
            
        
        
   def report_gener(self):
        print('''1.View report of all Customer
2.View report of All Products
3.View all customer's shopping history
4.Return to previous menu''')
        h = int(input("Please Enter your Choice:"))

        if(h == 1):
            try:
                cur.execute("SELECT * FROM customer")     # Report of all Customer
                print(from_db_cursor(cur))
            except Exception as e:
                print(e)
            self.report_gener()

        elif(h == 2):
            try:
                cur.execute("SELECT * FROM product")     # Report of All Products
                print(from_db_cursor(cur))
            except Exception as e:
                print(e)
            self.report_gener()

        elif(h == 3):
            try:
                cur.execute("SELECT * FROM buys")       # All customer shopping history
                print(from_db_cursor(cur))
            except Exception as e:
                print(e)
            self.report_gener()

        elif(h == 4):
            cls()
            self.adminMenu()

        else:
            print("Invalid option entered, try again!")
            cls()
            self.report_gener()


   def delete_history(self):
        try:
            cur.execute(("delete from buys"))
            print("Data deleted")
        except Error as e:
            print(e)

   def validate(self, bill_id):
      password = input("Please enter password:")
      if(password == "admin123"):
          cls()
          self.adminMenu()

      else:
          print('''Incorrect password!
1. Try again
2. Quit''')
          valOption = int(input("Option(1/2): "))
          if valOption == 1:
                          cls()
                          self.validate()
          elif valOption == 2:
                          return
          else:
                          print("Invalid option, try again!")
                          cls()
                          self.validate()
                              

   def adminMenu(self):
      print('''1.Manage customer
2.Manage product
3.Report generation
4.Delete history
5.Logout as admin''')                             
      d = int(input("Please enter your Choice:"))
      if(d == 1):
         cls()
         self.manag_cust()
      elif(d == 2):
         cls()
         self.manag_prod()
      elif(d == 3):
         cls()
         self.report_gener()
      elif(d == 4):
         cls()
         self.delete_history()
      elif(d == 5):
         return 
      else:
         print("Invalid option entered, try again!")
         cls()
         self.adminmenu()
         

                
