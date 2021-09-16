import sqlite3

# Generic function for DB commits
def runQuery(query, data):
    db = sqlite3.connect('roboticCoffee.db')
    try:
      cursor = db.cursor()
      cursor.execute(query, data)
      db.commit()
    except Exception as error:
      db.rollback()
      print(str(error))
    finally:
      db.close()

# Generic function for returning data from the DB
def getQuery(query, data):
    db = sqlite3.connect('roboticCoffee.db')
    try:
      cursor = db.cursor()
      cursor.execute(query, data)
      return cursor.fetchall()
    except Exception as error:
      print(str(error))
    finally:
      db.close()

# Function to retrieve all orders that have not been delivered
def getOrders():
    db = sqlite3.connect('roboticCoffee.db')
    try:
      cursor = db.cursor()
      cursor.execute('''SELECT * FROM orders WHERE deliveryTime IS NULL''')
      return cursor.fetchall()
    except Exception as error:
      print(str(error))
    finally:
      db.close()

# Function to retrieve total funds raised
def getTotal():
    db = sqlite3.connect('roboticCoffee.db')
    try:
      cursor = db.cursor()
      cursor.execute('''SELECT SUM("cost") FROM "orders"''')
      return cursor.fetchall()
    except Exception as error:
      print(str(error))
    finally:
      db.close()


# Queries
insertOrder = '''INSERT INTO orders (orderdata, cost, paid, orderTime) VALUES (?, ?, ?, ?)'''
getOrder = '''SELECT * FROM orders WHERE orderID = ?'''
updatePaid = '''UPDATE orders SET paid = "Yes" WHERE orderID = ?'''
updateOrder = '''UPDATE orders SET orderdata = ?, cost = ?, paid = ? WHERE orderID = ?'''
processDelivery = '''UPDATE orders SET deliveryTime = ? WHERE orderID = ?'''
getOrderID = '''SELECT seq FROM sqlite_sequence WHERE name=?'''
getOrderTimes = '''SELECT orderID, orderTime, deliveryTime FROM "orders" WHERE deliveryTime IS NOT NULL ORDER BY ? DESC'''
