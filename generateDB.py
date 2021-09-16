# Execute once to create sqlite DB and orders table.

queries = ["""CREATE TABLE IF NOT EXISTS orders
(
    orderID INTEGER PRIMARY KEY AUTOINCREMENT,
    orderdata TEXT,
    cost INT,
    paid TEXT,
    orderTime TEXT,
    deliveryTime TEXT
);"""]

import sqlite3

db = sqlite3.connect('roboticCoffee.db')
try:
  cursor = db.cursor()
  for query in queries:
      cursor.execute(query)

  #commit both changes at once:
  db.commit()
  print("Query executed successfully.")

except Exception as error:
  db.rollback()
  print("Error: " + str(error))

finally:
  db.close()