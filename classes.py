from datetime import datetime
from exts import db

class Alert(db.Model):
    __tablename__ = 'alerts'
    alert_id = db.Column(db.Integer, primary_key=True)
    alert_text = db.Column(db.Text, nullable=False)
    message_id = db.Column(db.Integer, nullable=False)
    users = db.Column(db.Text)  # This will be a stringified list of user IDs

    def __init__(self, alert_text, message_id, users):
        self.alert_text = alert_text
        self.message_id = message_id
        self.users = str([user.user_id for user in users])

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def read(cls, alert_id):
        return cls.query.filter_by(alert_id=alert_id).first()

    def update(self):
        db.session.commit()

    @classmethod
    def destroy(cls, alert_id):
        alert = cls.read(alert_id)
        if alert:
            db.session.delete(alert)
            db.session.commit()

class EmailAlert(Alert):
    def send_alert(self, message):
        print(f"Sending email alert: {message}")

class SmsAlert(Alert):
    def send_alert(self, message):
        print(f"Sending SMS alert: {message}")

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.String(80), primary_key=True)
    user_type = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    preferred_contact_method = db.Column(db.String(10), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    last_active_time = db.Column(db.DateTime, default=datetime.utcnow)
    language_preference = db.Column(db.String(50), nullable=False)
    time_zone = db.Column(db.String(50), nullable=False)
    alert_preferences = db.Column(db.Text, nullable=True)

    def __init__(self, user_id, user_type, name, email, phone_number, preferred_contact_method, is_active, language_preference, time_zone, alert_preferences):
        self.user_id = user_id
        self.user_type = user_type
        self.name = name
        self.email = email
        self.phone_number = phone_number
        self.preferred_contact_method = preferred_contact_method
        self.is_active = is_active
        self.language_preference = language_preference
        self.time_zone = time_zone
        self.alert_preferences = alert_preferences

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def read(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    def update(self):
        db.session.commit()

    @classmethod
    def destroy(cls, user_id):
        user = cls.read(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()

class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.String(80), nullable=False)
    customer_id = db.Column(db.Float, nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    sentiment_score = db.Column(db.String(50), nullable=False)

    def __init__(self, agent_id, customer_id, message_id, message_text, sentiment_score):
        self.agent_id = agent_id
        self.customer_id = customer_id
        self.message_id = message_id
        self.message_text = message_text
        self.sentiment_score = sentiment_score

    def create(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def read(cls, message_id):
        return cls.query.filter_by(message_id=message_id).first()

    def update(self):
        db.session.commit()

    @classmethod
    def destroy(cls, message_id):
        message = cls.read(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()

    def alert_users(self, alert_type):
        if alert_type == 'email':
            alert = EmailAlert()
        elif alert_type == 'sms':
            alert = SmsAlert()
        else:
            raise ValueError("Invalid alert type")
        alert.send_alert(self.message_text)
