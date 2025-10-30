import mysql.connector
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="admin",
    database="pythonbatch"
)
cursor = connection.cursor()
cursor.execute("SELECT name, mob, gmail FROM user")
while True:
    n = input("How many rows do you want to print  ")
    if n.strip() == "":
        print("Over")
        break
    n = int(n)
    if n <= 0:
        print("enter positive value ")
    rows = cursor.fetchmany(n)
    if not rows:
        print("No more data ")
        break
    for x in rows:
        id , name, mob, gmail = x
        print(f"id : {id} , name : {name}, mob : {mob}, gmail : {gmail}")
cursor.close()
connection.close()
