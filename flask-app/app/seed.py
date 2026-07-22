from datetime import datetime

from app import db
from app.models import (
    Inquiry,
    InquiryStatus,
    Patient,
    Reservation,
    ReservationStatus,
)


def seed_sample_data() -> None:
    if Patient.query.first():
        return

    patients = [
        Patient(name="Sophia Martinez", phone="+1-415-555-0198"),
        Patient(name="Liam O'Connor", phone="+44 20 7946 0958"),
        Patient(name="Nina Patel", phone="+91 22 1234 5678"),
        Patient(name="Emma Wilson", phone="+1-212-555-0147"),
        Patient(name="James Chen", phone="+86 10 1234 5678"),
        Patient(name="Olivia Brown", phone="+61 2 9876 5432"),
        Patient(name="Noah Garcia", phone="+34 91 123 4567"),
        Patient(name="Ava Thompson", phone="+1-310-555-0183"),
        Patient(name="Ethan Davis", phone="+49 30 12345678"),
    ]
    db.session.add_all(patients)
    db.session.flush()

    patient_by_name = {p.name: p for p in patients}

    reservations = [
        Reservation(
            patient=patient_by_name["Liam O'Connor"],
            datetime=datetime(2026, 7, 20, 18, 30),
            department="Cardiology",
            doctor="Dr. Emily Stanton",
            status=ReservationStatus.VISITED,
        ),
        Reservation(
            patient=patient_by_name["Nina Patel"],
            datetime=datetime(2026, 7, 18, 23, 0),
            department="Neurology",
            doctor="Dr. Marcus Lee",
            status=ReservationStatus.CANCELED,
        ),
        Reservation(
            patient=patient_by_name["Sophia Martinez"],
            datetime=datetime(2026, 7, 22, 10, 0),
            department="General Medicine",
            doctor="Dr. Sarah Kim",
            status=ReservationStatus.SCHEDULED,
        ),
        Reservation(
            patient=patient_by_name["Emma Wilson"],
            datetime=datetime(2026, 7, 21, 14, 15),
            department="Dermatology",
            doctor="Dr. James Porter",
            status=ReservationStatus.SCHEDULED,
        ),
        Reservation(
            patient=patient_by_name["James Chen"],
            datetime=datetime(2026, 7, 19, 9, 45),
            department="Orthopedics",
            doctor="Dr. Emily Stanton",
            status=ReservationStatus.VISITED,
        ),
        Reservation(
            patient=patient_by_name["Olivia Brown"],
            datetime=datetime(2026, 7, 17, 16, 30),
            department="Pediatrics",
            doctor="Dr. Lisa Nguyen",
            status=ReservationStatus.SCHEDULED,
        ),
        Reservation(
            patient=patient_by_name["Noah Garcia"],
            datetime=datetime(2026, 7, 16, 11, 0),
            department="Cardiology",
            doctor="Dr. Marcus Lee",
            status=ReservationStatus.CANCELED,
        ),
    ]
    db.session.add_all(reservations)

    inquiries = [
        Inquiry(
            datetime=datetime(2026, 7, 14, 18, 30),
            subject="Question about medication dosage",
            patient_name_or_contact="John Doe, +1234567890",
            status=InquiryStatus.RESOLVED,
            notes="Patient asked about adjusting evening dose. Advised to follow prescription.",
        ),
        Inquiry(
            datetime=datetime(2026, 7, 12, 20, 20),
            subject="Inquiry on lab test results",
            patient_name_or_contact="Michael Brown, +1987654321",
            status=InquiryStatus.NEW,
            notes="Waiting for lab to send results.",
        ),
        Inquiry(
            datetime=datetime(2026, 7, 15, 9, 0),
            subject="Appointment rescheduling request",
            patient_name_or_contact="Sarah Lee, +1555123456",
            status=InquiryStatus.IN_PROGRESS,
            notes="Staff checking doctor availability for next week.",
        ),
        Inquiry(
            datetime=datetime(2026, 7, 11, 13, 45),
            subject="Insurance coverage question",
            patient_name_or_contact="David Miller, +1444555666",
            status=InquiryStatus.RESOLVED,
            notes="Confirmed coverage for upcoming procedure.",
        ),
        Inquiry(
            datetime=datetime(2026, 7, 10, 8, 30),
            subject="Follow-up after surgery",
            patient_name_or_contact="Anna Kowalski, +48700123456",
            status=InquiryStatus.IN_PROGRESS,
            notes="Scheduled callback with nurse.",
        ),
        Inquiry(
            datetime=datetime(2026, 7, 9, 17, 10),
            subject="Prescription refill request",
            patient_name_or_contact="Robert Taylor, +12025550199",
            status=InquiryStatus.NEW,
            notes="",
        ),
    ]
    db.session.add_all(inquiries)
    db.session.commit()
