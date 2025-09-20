import sqlite3
from tabulate import tabulate

DB_NAME = "Restaurant_food_data.db"

foods = ["Idly", "Dosa", "Vada", "Roti", "Meals", "Veg Biryani",
         "Egg Biryani", "Chicken Biryani", "Mutton Biryani",
         "Ice Cream", "Noodles", "Manchooriya", "Orange juice",
         "Apple Juice", "Pineapple juice", "Banana juice"]


def connect_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    return conn, c


def create_table():
    conn, c = connect_db()
    c.execute("""
            CREATE TABLE IF NOT EXISTS item (
              Item_name TEXT PRIMARY KEY NOT NULL,
              No_of_customers INTEGERS NOT NULL DEFAULT 0,
              No_of_positive_reviews INTEGERS NOT NULL DEFAULT 0,
              No_of_negative_reviews INTEGERS NOT NULL DEFAULT 0,
              Positive_percentage TEXT NOT NULL DEFAULT '0.0%',
              Negative_percentage TEXT NOT NULL DEFAULT '0.0%'
            )
        """)
    
    conn.commit()
    conn.close()


def init_data():
    conn, c = connect_db()
    for item in foods:
        c.execute("""
                  INSERT OR IGNORE INTO item
                  (Item_name, No_of_customers, No_of_positive_reviews, 
                  No_of_negative_reviews, Positive_percentage, Negative_percentage)
                  VALUES (?, ?, ?, ?, ?, ?)
                  """, (item, 0, 0, 0, '0.0%', '0.0%')
                  )

    conn.commit()
    conn.close()


def clear_item(item_name):
    conn, c = connect_db()
    c.execute("""
            UPDATE item
            SET No_of_customers = ?,
                No_of_positive_reviews = ?,
                No_of_negative_reviews = ?,
                Positive_percentage = ?,
                Negative_percentage = ?
            WHERE Item_name = ?
                """, (0, 0, 0, '0.0%', '0.0%', item_name)
            )
            
    conn.commit()
    conn.close()


def clear_all():
    conn, c = connect_db()
    c.execute("""
            UPDATE item
            SET No_of_customers = ?,
                No_of_positive_reviews = ?,
                No_of_negative_reviews = ?,
                Positive_percentage = ?,
                Negative_percentage = ?
            """, (0, 0, 0, '0.0%', '0.0%')
            )
            
    conn.commit()
    conn.close()


def get_all_items():
    conn, c = connect_db()
    c.execute("SELECT *, oid FROM item")
    records = c.fetchall()
    conn.close()
    return records


def update_item(item_name, no_of_customers, no_of_positive_reviews, no_of_negative_reviews, positive_percentage, negative_percentage):
    conn, c = connect_db()
    c.execute("""
              UPDATE item
              SET No_of_customers = ?,
                  No_of_positive_reviews = ?,
                  No_of_negative_reviews = ?,
                  Positive_percentage = ?,
                  Negative_percentage = ?
              WHERE Item_name = ?
              """, (
                  no_of_customers,
                  no_of_positive_reviews,
                  no_of_negative_reviews,
                  f"{positive_percentage}%",
                  f"{negative_percentage}%",
                  item_name
              ))
    
    conn.commit()
    conn.close()


# for debugging usage
def pretty_print(items):
    headers = ["Item", "Total", "Positive", "Negative", "Positive %", "Negative %", "ID"]
    print(tabulate(items, headers = headers, tablefmt = "pretty"))
    