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

- Inquiry
  - Id (UUID)
  - DateTime (DateTime)
  - Subject (Text)
  - PatientNameOrContact (Text)
  - Status (Enum: New / In Progress / Resolved)
  - Notes (Long Text)

## Screens

- Patients
  - List existing patients (Name, Phone)
  - Add new patient via form (Name, Phone)

- Reservations
  - List reservations with Patient, DateTime, Department, Doctor, Status
  - Filter by status (Any / Canceled / Scheduled / Visited)
  - Open popup form to create and edit reservations

- Reservation edit (popup)
  - Show full details of a reservation (DateTime, Department, Doctor, Patient, Status)
  - Update fields and change Status (Scheduled / Visited / Canceled)

- Inquiries
  - List inquiries with DateTime, Subject, PatientNameOrContact, Status
  - Filter by status (Any / New / In Progress / Resolved)
  - Open popup form to create and edit inquiries

- Inquiry edit (popup)
  - Create and edit inquiries (DateTime, Subject, PatientNameOrContact, Status, Notes)

## Reservation save flow (pseudo code)

1. User fills in reservation form (patient, datetime, department, doctor, status).
2. On Save:
   - If new reservation: create a new Reservation record.
   - If editing: load existing Reservation record and update fields.
3. Commit changes to the database.
4. Redirect back to the Reservations list screen.
