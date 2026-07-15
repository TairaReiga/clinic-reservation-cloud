# clinic-reservation-cloud
Small clinic reservation & inquiry management cloud system

## Overview
Small clinic reservation & inquiry management cloud system built on OutSystems Personal Edition.
Aimed at small clinics to centralize patient reservations and inquiries in a single cloud app.

## Live App URL
Clinic Management app (OutSystems):
https://personal-p2heapy9-dev.outsystems.app/ClinicManagementSystem/Login

Use the sample users to log in:
- Log in as Matthew Shelton (Admin)
- Log in as Jesse Hernandez (Clinic Staff)

## Features
- Patient management:
  - Patient list (Patients screen)
  - Create new patients via a simple form (Name, Phone)

- Reservation management:
  - Reservation list with DateTime, Patient, Department, Doctor, Status
  - Status filtering (Any / Canceled / Scheduled / Visited)
  - New Reservation form to create and edit reservations (patient, date/time, department, doctor, status)

- Inquiry management:
  - Inquiry list with DateTime, Subject, PatientNameOrContact, Status
  - Status filtering (Any / New / In Progress / Resolved)
  - New Inquiry form to create and edit inquiries (date/time, subject, patient/contact, status, notes)
