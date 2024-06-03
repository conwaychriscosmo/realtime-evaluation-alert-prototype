
import sqlite3
import datetime

DATABASE = 'users.db'

class Alert:
    def __init__(self, alert_id, alert_text, message_id, users):
        self.alert_id = alert_id
        self.alert_text = alert_text
        self.message_id = message_id
        self.users = users  # List of User objects associated with the alert

    @staticmethod
    def db_connection():
        conn = sqlite3.connect(DATABASE)
        return conn

    def create(self):
        conn = self.db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                alert_id INTEGER PRIMARY KEY,
                alert_text TEXT,
                message_id INTEGER,
                users TEXT  -- This will be a stringified list of user IDs
            )
        ''')
        # Convert the list of User objects to a list of user IDs
        user_ids = [user.user_id for user in self.users]
        cursor.execute('''
            INSERT INTO alerts (alert_text, message_id, users)
            VALUES (?, ?, ?)
        ''', (self.alert_text, self.message_id, str(user_ids)))
        conn.commit()
        conn.close()

    @classmethod
    def read(cls, alert_id):
        conn = cls.db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alerts WHERE alert_id=?', (alert_id,))
        alert_data = cursor.fetchone()
        conn.close()
        if alert_data:
            # Convert the stringified list of user IDs back to a list of User objects
            user_ids = eval(alert_data[3])
            users = [User(user_id, None) for user_id in user_ids]  # User type is not stored in DB
            return cls(alert_data[0], alert_data[1], alert_data[2], users)
        else:
            return None

    def update(self):
        conn = self.db_connection()
        cursor = conn.cursor()
        # Convert the list of User objects to a list of user IDs
        user_ids = [user.user_id for user in self.users]
        cursor.execute('''
            UPDATE alerts
            SET alert_text=?, message_id=?, users=?
            WHERE alert_id=?
        ''', (self.alert_text, self.message_id, str(user_ids), self.alert_id))
        conn.commit()
        conn.close()

    @staticmethod
    def destroy(alert_id):
        conn = Alert.db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM alerts WHERE alert_id=?', (alert_id,))
        conn.commit()
        conn.close()

# Example usage:
# users = [User('user123', 1), User('user456', 2)]
# alert = Alert(None, 'Urgent alert text', 78910, users)
# alert.create()
# fetched_alert = Alert.read(1)
# fetched_alert.alert_text = 'Updated alert text'
# fetched_alert.update()
# Alert.destroy(1)

class EmailAlert(Alert):
    def send_alert(self, message):
        print(f"Sending email alert: {message}")

class SmsAlert(Alert):
    def send_alert(self, message):
        print(f"Sending SMS alert: {message}")


class User:
    def __init__(self, user_id, user_type, name, email, phone_number, preferred_contact_method, is_active, language_preference, time_zone, alert_preferences):
        self.user_id = user_id
        self.user_type = user_type
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.preferred_contact_method = preferred_contact_method
        self.is_active = is_active
        self.last_active_time = datetime.datetime.now()
        self.language_preference = language_preference
        self.time_zone = time_zone
        self.alert_preferences = alert_preferences

    @staticmethod
    def db_connection():
        conn = sqlite3.connect(DATABASE)
        return conn

    def create(self):
        conn = self.db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                user_type INTEGER,
                name TEXT,
                email TEXT,
                phone_number TEXT,
                preferred_contact_method TEXT,
                is_active BOOLEAN,
                last_active_time TEXT,
                language_preference TEXT,
                time_zone TEXT,
                alert_preferences TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO users (user_id, user_type, name, email, phone_number, preferred_contact_method, is_active, last_active_time, language_preference, time_zone, alert_preferences)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.user_id, self.user_type, self.name, self.email, self.phone_number, self.preferred_contact_method, self.is_active, self.last_active_time, self.language_preference, self.time_zone, self.alert_preferences))
        conn.commit()
        conn.close()

    @classmethod
    def read(cls, user_id):
        conn = cls.db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return cls(*user_data)
        else:
            return None

    def update(self):
        conn = self.db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users
            SET user_type=?, name=?, email=?, phone_number=?, preferred_contact_method=?, is_active=?, last_active_time=?, language_preference=?, time_zone=?, alert_preferences=?
            WHERE user_id=?
        ''', (self.user_type, self.name, self.email, self.phone_number, self.preferred_contact_method, self.is_active, self.last_active_time, self.language_preference, self.time_zone, self.alert_preferences, self.user_id))
        conn.commit()
        conn.close()

    @staticmethod
    def destroy(user_id):
        conn = User.db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE user_id=?', (user_id,))
        conn.commit()
        conn.close()

# Example usage:
# user = User('user123', 1, 'John Doe', 'john.doe@example.com', '555-1234', 'email', True, 'English', 'America/New_York', '{"email": true, "sms": false}')
# user.create()
# fetched_user = User.read('user123')
# fetched_user.name = 'Jane Doe'
# fetched_user.update()
# User.destroy('user123')


class Message:
    def __init__(self, agent_id, customer_id, message_id, message_text, sentiment_score):
        self.agent_id = agent_id
        self.customer_id = customer_id
        self.message_id = message_id
        self.message_text = message_text
        self.sentiment_score = sentiment_score

    @staticmethod
    def db_connection():
        conn = sqlite3.connect(DATABASE)
        return conn

    def create(self):
        conn = self.db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY,
                agent_id TEXT,
                customer_id REAL,
                message_text TEXT,
                sentiment_score TEXT
            )
        ''')
        cursor.execute('''
            INSERT INTO messages (agent_id, customer_id, message_id, message_text, sentiment_score)
            VALUES (?, ?, ?, ?, ?)
        ''', (self.agent_id, self.customer_id, self.message_id, self.message_text, self.sentiment_score))
        conn.commit()
        conn.close()

    @classmethod
    def read(cls, message_id):
        conn = cls.db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM messages WHERE message_id=?', (message_id,))
        message_data = cursor.fetchone()
        conn.close()
        if message_data:
            return cls(*message_data)
        else:
            return None

    def update(self):
        conn = self.db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE messages
            SET agent_id=?, customer_id=?, message_text=?, sentiment_score=?
            WHERE message_id=?
        ''', (self.agent_id, self.customer_id, self.message_text, self.sentiment_score, self.message_id))
        conn.commit()
        conn.close()

    @staticmethod
    def destroy(message_id):
        conn = Message.db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM messages WHERE message_id=?', (message_id,))
        conn.commit()
        conn.close()

# Example usage:
# message = Message('agent123', 456789, 78910, 'Your issue has been resolved.', 'positive')
# message.create()
# fetched_message = Message.read(78910)
# fetched_message.message_text = 'Your issue has been updated.'
# fetched_message.update()
# Message.destroy(78910)

    def alert_users(self, alert_type):
        if alert_type == 'email':
            alert = EmailAlert()
        elif alert_type == 'sms':
            alert = SmsAlert()
        else:
            raise ValueError("Invalid alert type")
        alert.send_alert(self.message_text)
