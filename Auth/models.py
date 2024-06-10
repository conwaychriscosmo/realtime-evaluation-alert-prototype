import time
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.sqla_oauth2 import (
    OAuth2ClientMixin,
    OAuth2AuthorizationCodeMixin,
    OAuth2TokenMixin,
)
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates
from datetime import datetime

db = SQLAlchemy()
Base = declarative_base()

class OAuth2Client(db.Model, OAuth2ClientMixin):
    __tablename__ = 'oauth2_client'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

class TechnicalUser(OAuth2Client):
    """
    Represents a technical user (SDK consumer) in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): User's username.
        api_key (str): Secure API key for authentication.
        permissions (str): Comma-separated list of permissions (e.g., "read,write").
        last_activity (datetime): Timestamp of the user's last activity.
        active (bool): Indicates whether the user is active.
        rate_limit (int): Requests per minute allowed for the user.
        associated_projects (str): Comma-separated project IDs.
        alert_preferences (str): Preferred alert channels (e.g., "email,webhook").
        sdk_version (str): Version of the SDK used by the user.
    """

    __tablename__ = 'technical_users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    api_key = Column(String(64), unique=True, nullable=False)
    permissions = Column(String(100))
    last_activity = Column(DateTime, default=datetime.utcnow)
    active = Column(Boolean, default=True)
    rate_limit = Column(Integer, default=100)
    client_id = db.Column(db.Integer, db.ForeignKey("oauth2_client.id", ondelete="CASCADE"))
    client = db.relationship("oauth2_client")

    @validates('permissions')
    def validate_permissions(self, key, value):
        """
        Validates the format of permissions (comma-separated).

        Args:
            key (str): Attribute name ('permissions').
            value (str): Proposed permissions value.

        Returns:
            str: Validated permissions value.

        Raises:
            ValueError: If permissions format is invalid.
        """
        if not all(p.strip() for p in value.split(',')):
            raise ValueError("Invalid permissions format")
        return value

    def update_last_activity(self):
        """
        Updates the last activity timestamp to the current time.
        """
        self.last_activity = datetime.utcnow()

    def deactivate_user(self):
        """
        Deactivates the user account.
        """
        self.active = False

    def activate_user(self):
        """
        Activates the user account.
        """
        self.active = True

    def update_rate_limit(self, new_limit):
        """
        Updates the rate limit for the user.

        Args:
            new_limit (int): New rate limit value.
        """
        self.rate_limit = new_limit

    def update_alert_preferences(self, preferences):
        """
        Updates the user's alert preferences.

        Args:
            preferences (str): Comma-separated list of preferred alert channels.
        """
        self.alert_preferences = preferences

    def update_sdk_version(self, version):
        """
        Updates the SDK version used by the user.

        Args:
            version (str): New SDK version.
        """
        self.sdk_version = version

    def delete_user(self):
        """
        Placeholder method for user deletion logic.
        """
        pass



class OAuth2AuthorizationCode(db.Model, OAuth2AuthorizationCodeMixin):
    __tablename__ = 'oauth2_code'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')


class OAuth2Token(db.Model, OAuth2TokenMixin):
    __tablename__ = 'oauth2_token'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User')

    def is_refresh_token_active(self):
        if self.revoked:
            return False
        expires_at = self.issued_at + self.expires_in * 2
        return expires_at >= time.time()