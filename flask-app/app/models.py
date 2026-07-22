from datetime import datetime

from app import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    reservations = db.relationship("Reservation", backref="patient", lazy=True)


class ReservationStatus:
    SCHEDULED = "Scheduled"
    VISITED = "Visited"
    CANCELED = "Canceled"

    CHOICES = [SCHEDULED, VISITED, CANCELED]


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    department = db.Column(db.String(100), nullable=False)
    doctor = db.Column(db.String(100), nullable=False)
    status = db.Column(
        db.String(20), nullable=False, default=ReservationStatus.SCHEDULED
    )
    image_filename = db.Column(db.String(255), nullable=True)


class InquiryStatus:
    NEW = "New"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"

    CHOICES = [NEW, IN_PROGRESS, RESOLVED]


class Inquiry(db.Model):
    __tablename__ = "inquiries"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    subject = db.Column(db.String(200), nullable=False)
    patient_name_or_contact = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=InquiryStatus.NEW)
    notes = db.Column(db.Text, nullable=True)
