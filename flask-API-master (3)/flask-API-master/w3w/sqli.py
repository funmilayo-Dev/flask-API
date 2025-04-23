#This is a CRUD test with EMMANuel
import sqlite3
from tabulate import tabulate

#connecting to the database
con = sqlite3.connect('clients.db')

#create an instance of the cursor based on the connected database
cur = con.cursor()

# create a user table
'''cur.execute("""CREATE TABLE usersList
            (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                surname TEXT NULL,
                company TEXT NULL,
                occupation TEXT NOT NULL,
                email TEXT NOT NULL
            );""")
con.commit()'''

def check_table_exist(table_name:str):
    """returns True if table name sent as arg exists"""
    #SQL statement checks counts of number of table_names in the the sql master
    cur.execute(""" SELECT count(name) FROM sqlite_master
                    WHERE type='table'
                    AND name= ?;
                    """, (table_name,)
                ) 
    count_of_tables = cur.fetchone()[0]
    con.commit()

    if count_of_tables == 1:
        return True
    else:        
        print(f"Table {table_name} does not exist")
        return False
    
def create_user_table():
    """Creates a table"""
    if check_table_exist("users"):
        print("Table exists!")
    
    else:
        cur.execute("""CREATE TABLE users
                    (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        firstname TEXT NOT NULL,
                        surname TEXT NOT NULL,
                        company TEXT NOT NULL,
                        occupation TEXT NOT NULL,
                        email TEXT NOT NULL
                    )                """)
        con.commit()

def menu_options():
    """End user menu options"""
    while True:
        print("""
        1. Insert a user data
        2. View one user data
        3. View all users data
        4. Delete one user data
        5. Update one user data
        6. Modify columns in users table
        6. Exit
            """)
        menu_choice = input("Please choose an option:\n")
        menu_options = ["1", "2", "3", "4", "5", "6"]

        while menu_choice not in menu_options:
            menu_choice = input("Error! You must choose a valid number between 1 and 6:\n")

        if menu_choice == "1":
            insert_user_record()
        elif menu_choice == "2":
            get_one_user_data()
        elif menu_choice == "3":
            get_all_users()
        elif menu_choice == "4":
            delete_one_user_data()
        elif menu_choice == "5":
            update_user_data()
        elif menu_choice == "6":
            modify_columns()
        else:
            print("Goodbye!")
            con.close()
            exit()

        continue_choice = input("Would you like to exit? (Y/N):\n").upper()
        if continue_choice == "Y":
            break
    print("Good bye!")
    con.close()
    exit()

def insert_user_record():
    """collects data entered by user and sends to insert_user_data func"""
    user_id = next_user_id() + 1
    firstname = input("Please enter your name: ")
    surname = input("Please enter your surname: ")
    company = input("Enter your organisation's name: ")
    occupation = input("Enter your occupation: ")
    email = input("Enter your email: ")

    #send values as args to insert_user_data()
    insert_user_data(firstname,surname,company,occupation,email)
    return

def insert_user_data(firstname:str, surname:str, company:str, occupation:str, email:str):
    """accepts user data as args and inserts into users table"""
    cur = con.cursor()
    cur.execute("""INSERT INTO users VALUES (?,?,?,?,?,?)""", 
                (None, firstname, surname, company, occupation, email)
    )
    con.commit()
    return

def next_user_id():
    """checks the database for the highest id number and increments by 1"""
    res = cur.execute("SELECT MAX(user_id) FROM users")
    highest_id = res.fetchone()[0]

    if highest_id is None:
        highest_id = 2400000

    print(highest_id)
    return highest_id


def get_all_users():
    """to print all records in a table"""
    cur = con.cursor()
    """print("{:<2} {:<15} {:<15} {:<10} {:<30} {:<50}"
          .format(("ID","Firstname","Surname","Organisation","Occupation","Email"))
    )"""
    #print(f"{'ID':<2} {'First name':<12} {'Surname':<12} {'Organisation':<12} {'Occupation':<12} {'Email':<10}")
    for row in cur.execute("SELECT rowid, * FROM users"):
        '''print("{:<2} {:<15} {:<15} {:<10} {:<30} {:<50}"
        .format(row[1],row[2],row[3])
        )'''
        #print(f"{row[0]:<2} {row[1]:<12} {row[2]:<12} {row[3]:<12} {row[4]:<12} {row[5]:<10}")

    """to display table data in tabular format"""
    table = []
    headers = ["First Name", "Surname", "Company", "Occupation", "Email"]
    for row in cur.execute("SELECT * FROM users ORDER by firstname"):
        #to convert individ tuple to list
        individ = list(row)
        #add individ tuple to complete tuple
        table.append(individ)

    print(tabulate(table,headers, tablefmt = "grid"))
    
def get_one_user_data():
    """display all table data"""
    cur = con.cursor()
    customer_id = input("Enter the customer's id")
    print(f"{'ID':<2} {'First Name':<15} {'Surname':<15} {'Organisation':<15} {'Occupation':<15} {'Email':<10}")
    for row in cur.execute("SELECT rowid, * FROM users WHERE rowid=?", customer_id):
        print(f"{row[0]:<2} {row[1]:<12} {row[2]:<12} {row[3]:<12} {row[4]:<12} {row[5]:<10}")
    return

def modify_columns():
    """to add a new column in the table"""
    cur = con.cursor()

def delete_one_user_data():
    """deletes one data from the table or database"""
    cur = con.cursor()
    get_one_user_data() #displays records before deletion
    user_id = input("Enter a customer to delete:\n")
    cur.execute("DELETE from users WHERE rowid=?", user_id)
    con.commit()
    get_one_user_data() #displays updated record after deleting
    return

def update_user_data():
    """to update user's data in the DB table"""
    get_one_user_data() # to display all data before update
    user_id = input("Enter the user id for update: ")
    user_firstname = input("Enter the new First name: ")
    user_surname = input("Enter the new Surname: ")
    user_company = input("Enter the company: ")
    user_occupation = input("Enter the new occupation: ")
    user_email = input("Enter new email: ")
    cur.execute("""UPDATE clientlist
    SET firstname = ?, surname = ?, organisation = ?, occupation = ?, email = ?
    WHERE rowid = ?""",(user_id,user_firstname,user_surname,user_company,user_occupation,user_email))
    get_one_user_data() # view updated records
    return


#check_table_exist("users")
#get_one_data()
#get_users_data()
#get_one_user_data()
#create_user_table()
#menu_options()
        