import mysql.connector
from colorama import Fore, Style, init
init(autoreset=True)

connection = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='Soham@2911',
    database='python_axixa'
)

cursor = connection.cursor(dictionary=True)

choices = {
    1: 'INSERT',
    2: 'UPDATE',
    3: 'DELETE',
    4: 'VIEW'
}

menu = f"""
{Fore.CYAN}Select an option:
1 - Insert Data
2 - Update Data
3 - Delete Data
4 - View Data{Style.RESET_ALL}
"""

while True:
    user_choice = input(menu)
    if not user_choice.isdigit() or int(user_choice) not in choices:
        print(Fore.RED + "Invalid option, try again.")
        continue

    selected = choices[int(user_choice)]

    if selected == 'INSERT':
        while True:
            name = input(Fore.BLUE + "Enter name: " + Style.RESET_ALL)
            if 5 <= len(name) <= 20 and name.isalpha():
                break
            else:
                print(Fore.RED + "Name must be alphabetic and 5–20 chars long.")

        while True:
            email = input(Fore.BLUE + "Enter email: " + Style.RESET_ALL)
            if email.endswith("@gmail.com") and 13 <= len(email) <= 25:
                break
            else:
                print(Fore.RED + "Invalid email address.")

        while True:
            mobile = input(Fore.BLUE + "Enter mobile: " + Style.RESET_ALL)
            if mobile.isdigit() and len(mobile) == 10:
                break
            else:
                print(Fore.RED + "Invalid mobile number.")

        cursor.execute(
            "INSERT INTO user (name, email, mobile) VALUES (%s, %s, %s)",
            (name, email, mobile)
        )
        connection.commit()
        print(Fore.GREEN + "Record added successfully!")

    elif selected == 'UPDATE':
        while True:
            user_id = input(Fore.BLUE + "Enter ID to update: " + Style.RESET_ALL)
            if user_id.isdigit():
                cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
                record = cursor.fetchone()
                if record:
                    break
                else:
                    print(Fore.RED + "No record found with that ID.")
            else:
                print(Fore.RED + "Invalid ID format.")

        new_name = input(Fore.BLUE + "Enter new name (leave blank to keep same): " + Style.RESET_ALL)
        new_email = input(Fore.BLUE + "Enter new email (leave blank to keep same): " + Style.RESET_ALL)
        new_mobile = input(Fore.BLUE + "Enter new mobile (leave blank to keep same): " + Style.RESET_ALL)

        if not new_name:
            new_name = record['name']
        if not new_email:
            new_email = record['email']
        if not new_mobile:
            new_mobile = record['mobile']

        cursor.execute(
            "UPDATE user SET name=%s, email=%s, mobile=%s WHERE id=%s",
            (new_name, new_email, new_mobile, user_id)
        )
        connection.commit()
        print(Fore.GREEN + "Record updated successfully!")

    elif selected == 'DELETE':
        while True:
            user_id = input(Fore.BLUE + "Enter ID to delete: " + Style.RESET_ALL)
            if not user_id.isdigit():
                print(Fore.RED + "Invalid ID, enter a numeric value.")
                continue

            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
            record = cursor.fetchone()
            if record:
                confirm = input(Fore.YELLOW + f"Are you sure you want to delete '{record['name']}'? (y/n): " + Style.RESET_ALL)
                if confirm.lower() == 'y':
                    cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))
                    connection.commit()
                    print(Fore.GREEN + "Record deleted successfully!")
                break
            else:
                print(Fore.RED + "ID not found, please try again.")

    elif selected == 'VIEW':
        cursor.execute("SELECT * FROM user")
        rows = cursor.fetchall()

        if not rows:
            print(Fore.RED + "No records available.")
            continue

        index = 0
        total = len(rows)

        while index < total:
            try:
                num = int(input(Fore.CYAN + f"How many rows do you want to see? (Remaining {total - index}): " + Style.RESET_ALL))
            except ValueError:
                print(Fore.RED + "Please enter a number.")
                continue

            end_index = index + num
            for r in rows[index:end_index]:
                print(f"{Fore.YELLOW}ID: {r['id']} | Name: {r['name']} | Email: {r['email']} | Mobile: {r['mobile']}")
            index = end_index

            if index >= total:
                print(Fore.GREEN + "No more records left.")
                break

            next_action = input(Fore.MAGENTA + "Do you want to see more or go to main menu? (m for more / any key for menu): " + Style.RESET_ALL)
            if next_action.lower() != 'm':
                break
