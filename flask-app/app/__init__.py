import os
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

from config import get_config

db = SQLAlchemy()


def create_app():
    config = get_config()
    base_dir = config.BASE_DIR

    app = Flask(
        __name__,
        template_folder=str(base_dir / "templates"),
        static_folder=str(base_dir / "static"),
    )

    app.config.from_object(config)
    app.config["SQLALCHEMY_DATABASE_URI"] = config._database_uri()

    upload_dir = Path(app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)

    if app.config.get("ENV") == "production":
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    db.init_app(app)

    from app import models  # noqa: F401
    from app.seed import seed_sample_data

    with app.app_context():
        db.create_all()
        _ensure_schema()
        seed_sample_data()

    from app.i18n import INQUIRY_STATUS_JA, RESERVATION_STATUS_JA

    @app.template_filter("fmt_datetime")
    def fmt_datetime(value):
        if value is None:
            return ""
        from app.i18n import MONTHS_JA
        return f"{value.year}年{MONTHS_JA[value.month]}{value.day}日 {value.strftime('%H:%M')}"

    @app.template_filter("reservation_status")
    def reservation_status(value):
        return RESERVATION_STATUS_JA.get(value, value)

    @app.template_filter("inquiry_status")
    def inquiry_status(value):
        return INQUIRY_STATUS_JA.get(value, value)

    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app


def _ensure_schema():
    from sqlalchemy import inspect, text

    inspector = inspect(db.engine)
    if "reservations" not in inspector.get_table_names():
        return

    columns = {col["name"] for col in inspector.get_columns("reservations")}
    if "image_filename" not in columns:
        with db.engine.begin() as conn:
            conn.execute(
                text("ALTER TABLE reservations ADD COLUMN image_filename VARCHAR(255)")
            )
