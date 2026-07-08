from sqlalchemy.dialects.mysql import TINYINT  # Import TINYINT for MySQL specific type

from app import db  # Import the db instance from app.py


class Tweet(db.Model):  # <--- Changed class name to Tweet for clarity
    __tablename__ = "tweets"  # <--- Explicitly set table name to 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    positive = db.Column(TINYINT(1), nullable=False, default=0)
    negative = db.Column(TINYINT(1), nullable=False, default=0)

    def __repr__(self):
        return (
            f'<Tweet {self.id}: "{self.text[:30]}..."> '
            f"(Positive: {self.positive}, Negative: {self.negative})"
        )
