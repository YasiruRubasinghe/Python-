from sqlite3.dbapi2 import Time
import sys
import os
import uuid 
import sqlite3
from collections import namedtuple

__db_location__ = "db"
__session_file__ = f"{__db_location__}/session.db"
__item_file__ = f"{__db_location__}/item.db"
__order_file__ = f"{__db_location__}/order.db"
cur = ""

User = namedtuple("User","id name")

def init():
    if_exits = os.path.exists(__db_location__)
    if if_exits==False:
        os.makedirs(__db_location__)

def view():
    open(__session_file__,"r")
    conUser = sqlite3.connect(__session_file__)  
    cur = conUser.cursor()
    user = cur.execute("SELECT * FROM users limit 1")
    for u in user:
        us = User(*u)
        print(us.id)
        print(us.name)
        return us.name
    conUser.commit()
    conUser.close()

def login(username):
    open(__session_file__,"w")
    conUser = sqlite3.connect(__session_file__)
    cur = conUser.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id text, name text)''')
    cur.execute("INSERT INTO users (id,name) VALUES (?,?)",(str(uuid.uuid1()),username))
    conUser.commit()
    conUser.close()
    

class Item:
    def __init__(self):
        os.path.exists(__item_file__)

    def save(self):
        conItem = sqlite3.connect(__item_file__)  
        cur = conItem.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS items
               (id text, name text,price real, sellingPrice real, qty int)''')
        cur.execute("INSERT INTO items (id,name,price,sellingPrice,qty) VALUES (?,?,?,?,?)",(str(uuid.uuid1()),self.name,self.price,self.sellingPrice,self.qty))
        conItem.commit()
        conItem.close()

    def getAll(self):
        conItem = sqlite3.connect(__item_file__)  
        cur = conItem.cursor()
        for row in cur.execute('SELECT * FROM items ORDER BY price'):
            print(row)
        conItem.commit()
        conItem.close()

    def getSingleItem(self):
        conItem = sqlite3.connect(__item_file__)  
        cur = conItem.cursor()
        items = cur.execute("SELECT * FROM items WHERE name LIKE '%s'" % self.name)
        for item in items:
            print(item)
        conItem.commit()
        conItem.close()
    
    def getSingleItemByID(self):
        conItem = sqlite3.connect(__item_file__)  
        cur = conItem.cursor()
        items = cur.execute("SELECT sellingPrice FROM items WHERE id LIKE '%s'" % self.id)
        for item in items:
            return item
        conItem.commit()
        conItem.close()

def item_create(name,price,selling_price,qty):
    item = Item()
    item.name = name
    item.price = price
    item.sellingPrice = selling_price
    item.qty = qty
    item.save()

def item_all():
    print("get all items...")
    item = Item()
    item.getAll()

def item_view(name):
    print("View item ",name)
    item = Item()
    item.name = name
    item.getSingleItem()

class Order:
    def __init__(self):
        os.path.exists(__order_file__)

    def save(self):
        cus_name = view()
        item = Item()
        item.id = self.item_id
        item_price = item.getSingleItemByID()
        qty = int(self.qty)
        order_total = item_price[0] * qty

        conOrder = sqlite3.connect(__order_file__)  
        cur = conOrder.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS orders
               (id text, cus_name text,total real, item_id text, qty int)''')
        cur.execute("INSERT INTO orders (id,cus_name,total,item_id,qty) VALUES (?,?,?,?,?)",
        (str(uuid.uuid1()),cus_name,order_total,self.item_id,qty))
            
        conOrder.commit()
        conOrder.close()

def order_place(item_id,qty):
    order = Order()
    order.item_id = item_id
    order.qty = qty
    order.save()

if __name__=="__main__":
    arguments = sys.argv[1:]

    section = arguments[0]
    command = arguments[1]
    params = arguments[2:]
    
    init()

    if section == "user":
        if command == "login":
           login(*params)    
        elif command == "view":
           view()  
    elif section == "item":
        if command == "create":
            item_create(*params)
        elif command == "all":
            item_all()
        elif command == "view":
            item_view(*params)
    elif section == "order":
        if command == "place":
            order_place(*params)