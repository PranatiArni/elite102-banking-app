import unittest
import mysql.connector

class TestBankingApp(unittest.TestCase):

    def setUp(self):
        self.conn = mysql.connector.connect(

            host="localhost",
            user="root",          
            password="Winter@2009", 
            database="banking_app"


        )

        self.cursor = self.conn.cursor()


        self.cursor.execute("DELETE FROM transactions")
        self.cursor.execute("DELETE FROM accounts")
        self.conn.commit()

    def tearDown(self):
        self.cursor.close()
        self.conn.close()



    def test_create_account(self):
        self.cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", ('Pranati Arni', 2345))
                                
        self.conn.commit()

        account_id = self.cursor.lastrowid


        self.cursor.execute("SELECT name, balance FROM accounts WHERE id = %s", (account_id,))
        result = self.cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Pranati Arni")
        self.assertEqual(float(result[1]), 2345.00)

    def test_deposit(self):
        self.cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", ('Pranati Arni', 1234))
        self.conn.commit()

        account_id = self.cursor.lastrowid

        self.cursor.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (40, account_id))
        self.conn.commit()

        self.cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        result = self.cursor.fetchone()
    
        self.assertEqual(float(result[0]), 1274.00)


    def test_withdraw(self):
        self.cursor.execute("INSERT INTO accounts (name, balance) VALUES (%s, %s)", ('Pranati Arni', 1234))
        self.conn.commit()

        account_id = self.cursor.lastrowid

        self.cursor.execute("UPDATE accounts SET balance = balance - %s WHERE id = %s", (40, account_id))
        self.conn.commit()

        self.cursor.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        result = self.cursor.fetchone()
    
        self.assertEqual(float(result[0]), 1194.00)

    
if __name__ == '__main__':
    unittest.main()









