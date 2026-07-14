# Implementation details

## Data model

- Patient
  - Id (UUID)
  - Name (Text)
  - Phone (Text)

- Reservation
  - Id (UUID)
  - Patient (Foreign key -> Patient)
  - DateTime (DateTime)
  - Department (Text)
  - Doctor (Text)
  - Status (Enum: Scheduled / Visited / Canceled)

## Screens

- Patients
  - List existing patients (Name, Phone)
  - Add new patient via form (Name, Phone)

- Reservations
  - List reservations with Patient, DateTime, Department, Doctor, Status
  - Filter by status (Any / Scheduled / Visited / Canceled)

- Reservation detail / edit
  - Show full details of a reservation
  - Update fields and change Status using "Mark as Visited", etc.

## Reservation save flow (pseudo code)

1. User fills in reservation form (patient, datetime, department, doctor, status).
2. On Save:
   - If new reservation: create a new Reservation record.
   - If editing: load existing Reservation record and update fields.
3. Commit changes to the database.
4. Redirect back to the Reservations list screen.
