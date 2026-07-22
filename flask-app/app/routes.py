import os
from datetime import datetime
from functools import wraps
from uuid import uuid4

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from app import db
from app.i18n import INQUIRY_STATUS_TABS, RESERVATION_STATUS_TABS
from app.models import (
    Inquiry,
    InquiryStatus,
    Patient,
    Reservation,
    ReservationStatus,
)

main_bp = Blueprint("main", __name__)

ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user_email"):
            return redirect(url_for("main.login"))
        return view(*args, **kwargs)

    return wrapped


def _allowed_image(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
    )


def _save_reservation_image(reservation: Reservation) -> None:
    image = request.files.get("image")
    if not image or not image.filename:
        return

    if not _allowed_image(image.filename):
        flash("画像は PNG、JPG、GIF、WebP 形式のみ対応しています。", "error")
        return

    ext = image.filename.rsplit(".", 1)[1].lower()
    filename = f"{reservation.id}_{uuid4().hex[:8]}.{ext}"
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    if reservation.image_filename:
        old_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"], reservation.image_filename
        )
        if os.path.exists(old_path):
            os.remove(old_path)

    image.save(upload_path)
    reservation.image_filename = filename


@main_bp.route("/")
def root():
    if session.get("user_email"):
        return redirect(url_for("main.patients_list"))
    return redirect(url_for("main.login"))


@main_bp.route("/health")
def health():
    return {"status": "ok"}


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_email"):
        return redirect(url_for("main.patients_list"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if (
            email == current_app.config["ADMIN_EMAIL"]
            and password == current_app.config["ADMIN_PASSWORD"]
        ):
            session["user_email"] = email
            return redirect(url_for("main.patients_list"))

        flash("認証情報が正しくありません。", "error")

    return render_template("login.html")


@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.login"))


@main_bp.route("/patients")
@login_required
def patients_list():
    search = request.args.get("search", "").strip()
    query = Patient.query.order_by(Patient.name)

    if search:
        query = query.filter(Patient.name.ilike(f"%{search}%"))

    patients = query.all()
    return render_template("patients_list.html", patients=patients, search=search)


@main_bp.route("/patients/new", methods=["GET", "POST"])
@login_required
def patients_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        phone = request.form.get("phone", "").strip()

        if not name or not phone:
            flash("氏名と電話番号は必須です。", "error")
            return render_template("patients_form.html", name=name, phone=phone)

        db.session.add(Patient(name=name, phone=phone))
        db.session.commit()
        return redirect(url_for("main.patients_list"))

    return render_template("patients_form.html", name="", phone="")


@main_bp.route("/reservations")
@login_required
def reservations_list():
    status = request.args.get("status", "Any")
    search = request.args.get("search", "").strip()

    query = Reservation.query.join(Patient).order_by(Reservation.datetime.desc())

    if status in ReservationStatus.CHOICES:
        query = query.filter(Reservation.status == status)

    if search:
        query = query.filter(Patient.name.ilike(f"%{search}%"))

    reservations = query.all()

    return render_template(
        "reservations_list.html",
        reservations=reservations,
        current_status=status,
        search=search,
        status_tabs=RESERVATION_STATUS_TABS,
    )


@main_bp.route("/reservations/new", methods=["GET", "POST"])
@login_required
def reservations_new():
    patients = Patient.query.order_by(Patient.name).all()

    if request.method == "POST":
        return _save_reservation()

    return render_template(
        "reservations_form.html",
        patients=patients,
        status_choices=ReservationStatus.CHOICES,
        reservation=None,
    )


@main_bp.route("/reservations/<int:reservation_id>")
@login_required
def reservations_detail(reservation_id: int):
    reservation = Reservation.query.get_or_404(reservation_id)
    return render_template("reservations_detail.html", reservation=reservation)


@main_bp.route("/reservations/<int:reservation_id>/edit", methods=["GET", "POST"])
@login_required
def reservations_edit(reservation_id: int):
    reservation = Reservation.query.get_or_404(reservation_id)
    patients = Patient.query.order_by(Patient.name).all()

    if request.method == "POST":
        return _save_reservation(reservation)

    return render_template(
        "reservations_form.html",
        patients=patients,
        status_choices=ReservationStatus.CHOICES,
        reservation=reservation,
    )


@main_bp.route("/reservations/<int:reservation_id>/cancel", methods=["POST"])
@login_required
def reservations_cancel(reservation_id: int):
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.status = ReservationStatus.CANCELED
    db.session.commit()
    flash("予約をキャンセルしました。", "success")
    return redirect(url_for("main.reservations_detail", reservation_id=reservation_id))


@main_bp.route("/reservations/<int:reservation_id>/visit", methods=["POST"])
@login_required
def reservations_visit(reservation_id: int):
    reservation = Reservation.query.get_or_404(reservation_id)
    reservation.status = ReservationStatus.VISITED
    db.session.commit()
    flash("来院済みに更新しました。", "success")
    return redirect(url_for("main.reservations_detail", reservation_id=reservation_id))


@main_bp.route("/reservations/<int:reservation_id>/datetime", methods=["POST"])
@login_required
def reservations_update_datetime(reservation_id: int):
    reservation = Reservation.query.get_or_404(reservation_id)
    dt_str = request.form.get("datetime", "").strip()

    if not dt_str:
        flash("日時を入力してください。", "error")
        return redirect(url_for("main.reservations_detail", reservation_id=reservation_id))

    reservation.datetime = datetime.fromisoformat(dt_str)
    db.session.commit()
    flash("日時を更新しました。", "success")
    return redirect(url_for("main.reservations_detail", reservation_id=reservation_id))


def _save_reservation(reservation: Reservation | None = None):
    patient_id = request.form.get("patient_id")
    dt_str = request.form.get("datetime")
    department = request.form.get("department", "").strip()
    doctor = request.form.get("doctor", "").strip()
    status = request.form.get("status")

    if not patient_id or not dt_str or not department or not doctor or not status:
        flash("必須項目をすべて入力してください。", "error")
        return redirect(request.url)

    dt = datetime.fromisoformat(dt_str)

    if reservation is None:
        reservation = Reservation(
            patient_id=patient_id,
            datetime=dt,
            department=department,
            doctor=doctor,
            status=status,
        )
        db.session.add(reservation)
        db.session.flush()
    else:
        reservation.patient_id = patient_id
        reservation.datetime = dt
        reservation.department = department
        reservation.doctor = doctor
        reservation.status = status

    _save_reservation_image(reservation)
    db.session.commit()

    if reservation.id:
        return redirect(url_for("main.reservations_detail", reservation_id=reservation.id))
    return redirect(url_for("main.reservations_list"))


@main_bp.route("/inquiries")
@login_required
def inquiries_list():
    status = request.args.get("status", "Any")
    search = request.args.get("search", "").strip()

    query = Inquiry.query.order_by(Inquiry.datetime.desc())

    if status in InquiryStatus.CHOICES:
        query = query.filter(Inquiry.status == status)

    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Inquiry.subject.ilike(like),
                Inquiry.patient_name_or_contact.ilike(like),
            )
        )

    inquiries = query.all()
    return render_template(
        "inquiries_list.html",
        inquiries=inquiries,
        current_status=status,
        search=search,
        status_tabs=INQUIRY_STATUS_TABS,
    )


@main_bp.route("/inquiries/new", methods=["GET", "POST"])
@login_required
def inquiries_new():
    if request.method == "POST":
        return _save_inquiry()

    return render_template(
        "inquiries_form.html",
        status_choices=InquiryStatus.CHOICES,
        inquiry=None,
    )


@main_bp.route("/inquiries/<int:inquiry_id>/edit", methods=["GET", "POST"])
@login_required
def inquiries_edit(inquiry_id: int):
    inquiry = Inquiry.query.get_or_404(inquiry_id)

    if request.method == "POST":
        return _save_inquiry(inquiry)

    return render_template(
        "inquiries_form.html",
        status_choices=InquiryStatus.CHOICES,
        inquiry=inquiry,
    )


def _save_inquiry(inquiry: Inquiry | None = None):
    dt_str = request.form.get("datetime")
    subject = request.form.get("subject", "").strip()
    patient_name_or_contact = request.form.get("patient_name_or_contact", "").strip()
    status = request.form.get("status")
    notes = request.form.get("notes", "").strip()

    if not dt_str or not subject or not patient_name_or_contact or not status:
        flash("必須項目をすべて入力してください。", "error")
        return redirect(request.url)

    dt = datetime.fromisoformat(dt_str)

    if inquiry is None:
        inquiry = Inquiry(
            datetime=dt,
            subject=subject,
            patient_name_or_contact=patient_name_or_contact,
            status=status,
            notes=notes,
        )
        db.session.add(inquiry)
    else:
        inquiry.datetime = dt
        inquiry.subject = subject
        inquiry.patient_name_or_contact = patient_name_or_contact
        inquiry.status = status
        inquiry.notes = notes

    db.session.commit()
    return redirect(url_for("main.inquiries_list"))
