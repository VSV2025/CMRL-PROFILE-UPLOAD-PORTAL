from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Submission(db.Model):

    __tablename__ = "submissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_name = db.Column(
        db.String(255),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        nullable=False
    )

    contact_no = db.Column(
        db.String(20),
        nullable=False
    )

    pdf_path = db.Column(
        db.String(500),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )