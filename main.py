import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",          
    password="Winter@2009", 
    database="banking_app"
)
cursor = conn.cursor()

"""----------Tables------------
- create accounts and transactions tables 
-------------------------------------"""



def tables():

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            balance DECIMAL(10, 2)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            account_id INT,
            type VARCHAR(20),
            amount DECIMAL(10,2),
            FOREIGN KEY (account_id) REFERENCES accounts(id)
        )
    ''')

    conn.commit()


"""----------Create Account Function----------
- create an account with the user's name and initial deposit amount
- validate that the initial deposit is not negative
--------------------------------------------------------------"""



def create_account():
    user_name = input("Enter your name: ")
    initial_deposit = float(input("Enter initial deposit amount: "))

    if initial_deposit < 0:
        print("Initial deposit cannot be negative.")
        return  
    
    sql = "INSERT INTO accounts (name, balance) VALUES (%s, %s)"
    val = (user_name, initial_deposit)
    cursor.execute(sql, val)
    conn.commit()


    account_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)", (account_id, "CREATE", initial_deposit)
    )
    conn.commit()

    print("Account has been created: "+ str(account_id))


"""----------Deposit Function----------
- allow users to deposit money into their account
- validate that the deposit amount is not negative or zero
----------------------------------------"""

def deposit():
    account_id = int(input("Enter account ID: "))
    amount = float(input("Enter the amount to deposit: "))

    if amount <= 0:
        print("Deposit cannot be zero or negative.")
        return
    
    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    result = cursor.fetchone()


    if result is None:
        print("Account was not found")
        return
    
    cursor.execute(
        "UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, account_id))

    cursor.execute(
        "INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)", (account_id, "DEPOSIT", amount)
    )

    conn.commit()

    print("Money has been deposited!")


"""----------Withdraw Function----------
- allow users to withdraw money from their account
- validate that the withdrawal amount is not negative or zero
- validate that the account has sufficient funds for the withdrawal
------------------------------------------"""

def withdraw():
    account_id = int(input("Enter account ID: "))
    amount = float(input("Enter the amount to withdraw: "))

    if amount <= 0:
        print("Withdrawal cannot be zero or negative.")
        return
    


    cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    result = cursor.fetchone()

    if result is None:
        print("Account wasn't found")
        return



    
    current_balance = result[0]

    if current_balance < amount:
        print("Insufficient amount of money in the account")
        return
    
    cursor.execute(
        "UPDATE accounts SET balance = balance - %s WHERE id = %s", (amount, account_id))

    cursor.execute(
        "INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)", (account_id, "WITHDRAW", amount)
    )

    conn.commit()

    print("Money has been withdrawn!")


"""----------Check Transaction History Function----------
- allow users to view their transaction history, including deposits and withdrawals
- validate that the account exists before retrieving transaction history
----------------------------------------------------------"""



def check_transactions():
    account_id = int(input("Enter account ID: "))


    cursor.execute("SELECT type, amount FROM transactions WHERE account_id = %s", (account_id,))

    transactions = cursor.fetchall()

    if len(transactions) == 0:
        print("Transactions haven't been found for this account.")
        return

    for transaction in transactions:
        print(f"Type: {transaction[0]},  Amount: {transaction[1]}")


"""----------Check Balance Function----------
- allow users to check their account balance
- validate that the account exists before retrieving balance
--------------------------------------------"""


def check_account_balance():
    account_id = int(input("Enter account ID: "))

    cursor.execute("SELECT name, balance from accounts WHERE id = %s", (account_id,))
    result = cursor.fetchone()

    if result is None:
        print("Account wasn't found")
        return
    else:
        print("Account Name:" + str(result[0]))
        print("Account Balance:" + str(result[1]))


"""----------List Existing Account/Delete Account Function----------
- allow users to view all existing accounts and delete an account if they choose to
- validate that the account exists before deleting an account
-------------------------------------------------------------"""


def list_existing_accounts():
    cursor.execute("SELECT id, name FROM accounts")

    accounts = cursor.fetchall()

    if len(accounts) == 0:
        print("No accounts have been found.")
        return
    
    for account in accounts:
        print("Id: " + str(account[0]) + ", Name: " + str(account[1]))

    delete_account = input("Would you like to delete an account? (y/n): ")

    if delete_account == "y":

        account_id = int(input("Enter your account ID:"))

        cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))

        result = cursor.fetchone()

        if result is None:
            print("Account wasn't found")
            return
        cursor.execute("DELETE FROM transactions where account_id = %s", (account_id,))
        cursor.execute("DELETE FROM accounts where id = %s", (account_id,))
        conn.commit()

        print("Account has been deleted!")



                         
"""-----------Main Menue Function/ CLI UI------------"""

def main_menu():
    print("Welcome to the Banking App!")
    

    while True:
        print("1. Create an Account \n2. Deposit into Account \n3. Withdraw from Account \n4. Check transaction history \n5. View account Balance \n6. View all account/Delete an account ")
 


        user_choice = int(input("Enter your choice: "))

        if user_choice == 1:
            create_account()
        elif user_choice == 2:
            deposit()
        elif user_choice == 3:
            withdraw()
        elif user_choice == 4:
            check_transactions()
        elif user_choice == 5:
            check_account_balance()
        elif user_choice == 6:
            list_existing_accounts()
        
        user = input("Would you like to keep managaing your account? (y/n):")

        if user == 'n':
            print("Thank you for using the Banking App!")
            break

# Calls

tables()
main_menu()

        
