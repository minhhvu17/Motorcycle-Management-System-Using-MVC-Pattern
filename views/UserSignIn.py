import mysql.connector
import smtplib, ssl
import random
from email.message import EmailMessage
from hashlib import sha256

# inexjtosdktycubl

class UserSignIn:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="minhhvu11",
            database="motorbikemanagement"
        )


    def authenticate(self, username, password):
        cur = self.conn.cursor()

        # Execute the SQL query check username and password
        cur.execute("SELECT * FROM user_data WHERE username = %s AND password = %s", (username, password))

        # Get the result
        result = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        self.conn.close()

        if result:
            return True
        else:
            return False

    
class UserRestorePassword:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="minhhvu11",
            database="motorbikemanagement"
        )
        self.sender_email = 'ml2groupproject@gmail.com'
        self.sender_password = 'yybzjvmsyynkjbfl'

    def check_email(self, username, email):
        cur = self.conn.cursor()

        # Execute the SQL query check username and password
        cur.execute("SELECT * FROM user_data WHERE username = %s AND email = %s", (username, email))

        # Get the result
        result = cur.fetchone()

        # Close the cursor and connection
        cur.close()
        self.conn.close()

        if result:
            return True
        else:
            return False

    def send_email(self, user_email):
        # Set the subject and body of the email
        subject = 'RESET CODE FOR YOUR ACCOUNT'
        code = random.randint(100000, 999999)
        body = """
        This is your code: {}
        """

        body = body.format(code)

        em = EmailMessage()
        em['From'] = self.sender_email
        em['To'] = user_email
        em['Subject'] = subject
        em.set_content(body)

        # Add SSL (layer of security)
        context = ssl.create_default_context()

        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.sender_email, self.sender_password)
            smtp.sendmail(self.sender_email, user_email, em.as_string())
        
        # hash code and save to database
        h = sha256()
        h.update(str(code).encode())
        hash = h.hexdigest()
        code = hash

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="minhhvu11",
            database="motorbikemanagement"
        )
        cur = self.conn.cursor()
        try:
            cur.execute('DROP TABLE if exists code_sent')
        except:
            pass
        cur.execute('CREATE TABLE code_sent (code VARCHAR(64))')
        cur.execute('INSERT INTO code_sent (code) VALUES (%s)', (code,))
        self.conn.commit()
        cur.close()
        self.conn.close()

    def check_code(self, code1):
        if code1 == '':
            return False
        h = sha256()
        h.update(code1.encode())
        hash = h.hexdigest()
        code1 = hash
        cur = self.conn.cursor()
        # check if code is in database

        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="minhhvu11",
            database="motorbikemanagement"
        )
        cur = self.conn.cursor()
        cur.execute('use motorbikemanagement')

        try:
            cur.execute('SELECT * FROM code_sent WHERE code = %s', (code1,))
        except:
            return False
        
        result = cur.fetchone()
        cur.close()
        self.conn.close()

        if result:
            return True
        else:
            return False
    
    def change_password(self, username, password):
        cur = self.conn.cursor()

        #hash the new password
        h = sha256()
        h.update(password.encode())
        hash = h.hexdigest()
        password = hash

        # Execute the SQL query to update password of user with username = username
        query = 'UPDATE user_data SET password = %s WHERE username = %s'
        cur.execute(query, (password, username))

        # Commit the changes
        self.conn.commit()

        # Close the cursor and connection
        cur.close()
        self.conn.close()
