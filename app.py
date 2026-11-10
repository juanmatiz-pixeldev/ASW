from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import random
import re
from functools import wraps
import os
from sqlalchemy import create_engine, String, Integer, DateTime, Boolean, select, func, inspect, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-this-secret")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "false").lower() == "true",
)

TOTAL_CUPOS = 100
CAMPAIGN_YEAR = 2026
CAMPAIGN_MONTH = 11
CAMPAIGN_START_DAY = 1
CAMPAIGN_END_DAY = 30
LEVELS = ["A1", "A2", "B1", "B2", "B2+", "Exceptional Level"]
PACKAGE_LEVELS = {1: ["A1"], 3: ["A1", "A2", "B1"], 6: LEVELS}
STATUSES = ["Ya se encuentra matriculado", "Pagó - esperando material", "Pendiente de pago"]
SEDES = ["Cali Norte", "Cali San Fernando", "Cali Limonar"]
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///data.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Person(Base):
    __tablename__ = "people"
    id = mapped_column(String(80), primary_key=True)
    identification: Mapped[str | None] = mapped_column(String(12), nullable=True, unique=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    package: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(80), nullable=False)
    sede: Mapped[str] = mapped_column(String(40), nullable=False, default="Cali Norte")
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(40), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    sede: Mapped[str | None] = mapped_column(String(40), nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

Base.metadata.create_all(engine)

def random_promo_code(used=None):
    used = used or set()
    while True:
        # Formato promocional: ASW + 6 dígitos.
        code = "ASW" + "".join(random.choice("0123456789") for _ in range(6))
        if code not in used:
            return code

def valid_promo_code(value):
    return bool(re.fullmatch(r"ASW\d{6}", str(value or "").strip().upper()))

def random_colombian_id(used=None):
    used = used or set()
    while True:
        # Identificación ficticia de 8 a 10 dígitos, con primer dígito entre 1 y 9.
        length = random.choice([8, 9, 10])
        value = str(random.randint(1, 9)) + "".join(random.choice("0123456789") for _ in range(length - 1))
        if value not in used:
            return value

def migrate_database():
    # Compatibilidad con bases anteriores: agrega identificación y convierte los
    # antiguos IDs de cédula en códigos promocionales de 6 dígitos.
    inspector = inspect(engine)
    columns = {c["name"] for c in inspector.get_columns("people")} if inspector.has_table("people") else set()
    with engine.begin() as conn:
        if "identification" not in columns:
            conn.execute(text("ALTER TABLE people ADD COLUMN identification VARCHAR(12)"))
    with SessionLocal() as db:
        people = db.scalars(select(Person)).all()
        used_codes = {p.id for p in people if p.id and len(p.id) == 6 and p.id.isdigit()}
        used_ids = {p.identification for p in people if p.identification}
        changed = False
        for person in people:
            if not person.identification or not str(person.identification).isdigit():
                person.identification = random_colombian_id(used_ids)
                used_ids.add(person.identification)
                changed = True
            if not valid_promo_code(person.id):
                old_id = person.id
                person.id = random_promo_code(used_codes)
                used_codes.add(person.id)
                changed = True
        if changed:
            db.commit()

migrate_database()

NAMES = [
    "Luisa Fernanda Ríos", "Carlos Andrés Mora", "Diana Marcela Suárez", "Jorge Esteban Patiño",
    "Ana Milena Castro", "Raúl Hernández Vega", "Paola Andrea Giraldo", "Sebastián López Torres",
    "Marcela Quintero Ruiz", "Fabio Alberto Nieto", "Claudia Patricia Romero", "Hernando Salcedo Ávila",
    "Natalia Gómez Pedraza", "Álvaro Martínez Cano", "Sandra Milena Vargas", "Andrés Felipe Cárdenas",
    "Valentina Rodríguez Peña", "Juan David Moreno", "Camila Andrea Torres", "Mateo Sánchez Ruiz",
    "Daniela Pardo Gómez", "Santiago Ramírez", "Laura Sofía Méndez", "Nicolás Herrera",
    "Mariana Castillo", "David Esteban Rojas", "Sara Martínez", "Miguel Ángel Vargas",
    "Juliana Restrepo", "Alejandro Díaz", "Gabriela Molina", "Felipe González",
    "Manuela Castro", "Cristian Parra", "Isabella Ortiz", "Kevin Martínez",
    "Laura Valeria León", "Samuel Jiménez", "Sofía Cabrera", "Tomás Arias",
    "María José Navarro", "Juan Sebastián Duarte", "Daniela Salazar", "Esteban Guerrero",
    "Valeria Campos", "Julián Acosta", "Carolina Beltrán", "Diego Fernando Ruiz",
    "Natalia Andrea Silva", "Óscar Medina", "Angie Ramírez", "Brayan Torres",
    "Paula Andrea Lozano", "Emmanuel Castaño", "Viviana Rincón", "José Manuel Peña",
    "Tatiana Franco", "Mauricio Valencia", "Lina Marcela Cruz", "Ricardo Fuentes",
    "Adriana Gómez", "Wilson Bermúdez", "Mónica Velasco", "Germán Ospina",
    "Katherine Salcedo", "Jonathan Reyes", "Alejandra Nieto", "Jhonatan Morales",
    "Melissa Vargas", "Harold Quintero", "Yuliana Cifuentes", "Sebastián Cardona",
    "Andrea Patricia Mejía", "Luis Miguel Arias", "Fernanda Cárdenas", "Camilo Andrés Peña",
    "Sara Valentina Rojas", "Manuel Alejandro Díaz", "Lorena Sánchez", "Cristóbal Molina",
    "Daniela Valencia", "Andrés Mauricio Rojas", "Natalia Pineda", "Felipe Andrés Muñoz",
    "María Camila Rentería", "David Santiago López", "Valentina Restrepo",
    "Juan Pablo Cárdenas", "Isabella Martínez", "Samuel Ortega", "Laura Jiménez",
    "Nicolás Benítez", "Camila Fernández", "Mateo Giraldo", "Sara Ocampo",
    "Tomás Velasco", "Mariana Ríos", "Emilio Cabrera",
]

def initial_data():
    rng = random.Random(20260901)
    names = NAMES.copy()
    rng.shuffle(names)
    records = []
    used_codes = set()
    used_ids = set()
    # 95 registros ficticios para una demostración visual: quedan exactamente 5 cupos.
    statuses = ["Pagó - esperando material"] * 25 + ["Ya se encuentra matriculado"] * 70
    rng.shuffle(statuses)
    for i, name in enumerate(names[:95]):
        package = rng.choice([1, 3, 6])
        day = rng.randint(CAMPAIGN_START_DAY, CAMPAIGN_END_DAY)
        hour = rng.randint(7, 19)
        minute = rng.randint(0, 59)
        sede = rng.choice(SEDES)
        promo = random_promo_code(used_codes)
        used_codes.add(promo)
        identification = random_colombian_id(used_ids)
        used_ids.add(identification)
        records.append(Person(
            id=promo, identification=identification, name="[DEMO] " + name, package=package,
            status=statuses[i], sede=sede,
            date=datetime(CAMPAIGN_YEAR, CAMPAIGN_MONTH, day, hour, minute)
        ))
    return records

def seed_database():
    # Los 95 registros ficticios están marcados [DEMO]. Se insertan una sola vez,
    # únicamente si la tabla está vacía y SEED_DEMO_DATA=true. Desactivar después.
    if os.environ.get("SEED_DEMO_DATA", "false").lower() != "true":
        return
    with SessionLocal() as db:
        if db.scalar(select(func.count()).select_from(Person)) == 0:
            db.add_all(initial_data())
            db.commit()

def validate_date(value):
    try:
        dt = datetime.strptime(value, "%Y-%m-%dT%H:%M")
        return dt.year == CAMPAIGN_YEAR and dt.month == CAMPAIGN_MONTH and CAMPAIGN_START_DAY <= dt.day <= CAMPAIGN_END_DAY
    except (TypeError, ValueError):
        return False

def normalize_entry(data):
    package = int(data.get("package", 1))
    if package not in PACKAGE_LEVELS:
        raise ValueError("Package must be 1, 3, or 6 levels.")
    status = data.get("status", STATUSES[0])
    if status not in STATUSES:
        raise ValueError("Invalid status.")
    return package, status

def serialize(person):
    return {
        "id": person.id, "identification": person.identification, "name": person.name, "package": person.package,
        "levels": PACKAGE_LEVELS[person.package], "status": person.status, "sede": person.sede,
        "date": person.date.strftime("%d/%m/%Y %H:%M")
    }

def login_required(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        if not session.get("authenticated"):
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "msg": "Login required."}), 401
            return redirect(url_for("login", next=request.path))
        return fn(*args, **kwargs)
    return wrapped

def seed_users():
    # No existen contraseñas predeterminadas: deben configurarse como variables
    # privadas del servicio de hosting antes de poner la web en Internet.
    required = ["ADMIN_PASSWORD", "NORTE_PASSWORD", "SAN_FERNANDO_PASSWORD", "LIMONAR_PASSWORD"]
    missing = [key for key in required if not os.environ.get(key)]
    if missing:
        raise RuntimeError("Faltan variables privadas de acceso: " + ", ".join(missing))
    credentials = {
        "admin": (os.environ["ADMIN_PASSWORD"], None, True),
        "NORTE": (os.environ["NORTE_PASSWORD"], "Cali Norte", False),
        "SAN_FERNANDO": (os.environ["SAN_FERNANDO_PASSWORD"], "Cali San Fernando", False),
        "LIMONAR": (os.environ["LIMONAR_PASSWORD"], "Cali Limonar", False),
    }
    with SessionLocal() as db:
        for username, (password, sede, is_admin) in credentials.items():
            user = db.get(User, username)
            if not user:
                db.add(User(username=username, password_hash=generate_password_hash(password), sede=sede, is_admin=is_admin))
        db.commit()

def current_user():
    username = session.get("username")
    if not username:
        return None
    with SessionLocal() as db:
        return db.get(User, username)

def visible_query(db, user):
    stmt = select(Person).order_by(Person.date.desc())
    if not user.is_admin:
        stmt = stmt.where(Person.sede == user.sede)
    return stmt

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        with SessionLocal() as db:
            user = db.get(User, username)
            if user and check_password_hash(user.password_hash, password):
                session.clear()
                session["authenticated"] = True
                session["username"] = user.username
                session["is_admin"] = user.is_admin
                session["sede"] = user.sede
                return redirect(request.args.get("next") or url_for("index"))
        return render_template("login.html", error="Incorrect username or password."), 401
    return render_template("login.html", error=None)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    user = current_user()
    return render_template("index.html", total=TOTAL_CUPOS, levels=LEVELS, statuses=STATUSES, sedes=SEDES, username=user.username, is_admin=user.is_admin, user_sede=user.sede)

@app.route("/api/people", methods=["GET"])
@login_required
def get_people():
    user = current_user()
    with SessionLocal() as db:
        people = db.scalars(visible_query(db, user)).all()
        global_people = db.scalars(select(Person)).all()
        paid_waiting = sum(1 for p in people if p.status == "Pagó - esperando material")
        matriculated = sum(1 for p in people if p.status == "Ya se encuentra matriculado")
        return jsonify({
            "people": [serialize(p) for p in people], "total": TOTAL_CUPOS,
            "registered": len(global_people), "available": max(0, TOTAL_CUPOS - len(global_people)),
            "visible_registered": len(people), "matriculated": matriculated, "paid_waiting": paid_waiting,
            "sede": user.sede, "is_admin": user.is_admin
        })

@app.route("/api/register", methods=["POST"])
@login_required
def register():
    data = request.get_json() or {}
    user = current_user()
    name = (data.get("name") or "").strip()
    promo_code = (data.get("promo_code") or "").strip().upper()
    identification = "".join(ch for ch in str(data.get("identification") or "") if ch.isdigit())
    date_value = data.get("date") or datetime.now().strftime("%Y-%m-%dT%H:%M")
    if not name or not promo_code or not identification:
        return jsonify({"ok": False, "msg": "Full name, promotional code, and identification are required."}), 400
    if not valid_promo_code(promo_code):
        return jsonify({"ok": False, "msg": "Promotional code must follow the format ASW + 6 digits. Example: ASW753025."}), 400
    if not (6 <= len(identification) <= 10) or identification[0] == "0":
        return jsonify({"ok": False, "msg": "Identification must contain 6 to 10 digits and start with a digit from 1 to 9."}), 400
    if not validate_date(date_value):
        return jsonify({"ok": False, "msg": "Date must be between November 1 and November 30, 2026."}), 400
    try:
        package, status = normalize_entry(data)
    except (ValueError, TypeError) as exc:
        return jsonify({"ok": False, "msg": str(exc)}), 400
    sede = (data.get("sede") or "").strip() if user.is_admin else user.sede
    if sede not in SEDES:
        return jsonify({"ok": False, "msg": "Invalid branch."}), 400
    dt = datetime.strptime(date_value, "%Y-%m-%dT%H:%M")
    with SessionLocal() as db:
        try:
            if db.scalar(select(Person).where(Person.identification == identification)):
                return jsonify({"ok": False, "msg": "This identification is already registered."}), 409
            count = db.scalar(select(func.count()).select_from(Person))
            if count >= TOTAL_CUPOS:
                return jsonify({"ok": False, "msg": "No seats are available."}), 400
            if db.scalar(select(Person).where(Person.id == promo_code)):
                return jsonify({"ok": False, "msg": "This promotional code is already registered. Please use another code."}), 409
            entry = Person(id=promo_code, identification=identification, name=name, package=package, status=status, sede=sede, date=dt)
            db.add(entry)
            db.commit()
            disp = TOTAL_CUPOS - (count + 1)
            return jsonify({"ok": True, "entry": serialize(entry), "disponibles": disp, "msg": f"✅ {name} registered at {sede}. Promotional code: {promo_code}. {disp} seats remaining."})
        except IntegrityError:
            db.rollback()
            return jsonify({"ok": False, "msg": "The identification or promotional code is already registered."}), 409

@app.route("/api/update/<path:person_id>", methods=["PUT"])
@login_required
def update_person(person_id):
    data = request.get_json() or {}
    user = current_user()
    with SessionLocal() as db:
        person = db.get(Person, person_id)
        if not person:
            return jsonify({"ok": False, "msg": "Enrollment not found."}), 404
        if not user.is_admin and person.sede != user.sede:
            return jsonify({"ok": False, "msg": "You do not have permission to edit an enrollment from another branch."}), 403
        name = (data.get("name") or person.name).strip()
        promo_code = (data.get("promo_code") or person.id).strip().upper()
        identification = "".join(ch for ch in str(data.get("identification") or person.identification or "") if ch.isdigit())
        if not name or not promo_code or not identification:
            return jsonify({"ok": False, "msg": "Full name and identification are required."}), 400
        if not valid_promo_code(promo_code):
            return jsonify({"ok": False, "msg": "Promotional code must follow the format ASW + 6 digits. Example: ASW753025."}), 400
        if not (6 <= len(identification) <= 10) or identification[0] == "0":
            return jsonify({"ok": False, "msg": "Identification must contain 6 to 10 digits and start with a digit from 1 to 9."}), 400
        other = db.scalar(select(Person).where(Person.identification == identification, Person.id != person.id))
        if other:
            return jsonify({"ok": False, "msg": "This identification already belongs to another record."}), 409
        date_value = data.get("date")
        if date_value:
            if not validate_date(date_value):
                return jsonify({"ok": False, "msg": "Date must be between November 1 and November 30, 2026."}), 400
            person.date = datetime.strptime(date_value, "%Y-%m-%dT%H:%M")
        try:
            package, status = normalize_entry(data)
        except (ValueError, TypeError) as exc:
            return jsonify({"ok": False, "msg": str(exc)}), 400
        if user.is_admin:
            sede = (data.get("sede") or person.sede).strip()
            if sede not in SEDES:
                return jsonify({"ok": False, "msg": "Invalid branch."}), 400
            person.sede = sede
        other_code = db.scalar(select(Person).where(Person.id == promo_code, Person.id != person.id))
        if other_code:
            return jsonify({"ok": False, "msg": "Este código promocional ya está registrado."}), 409
        person.id = promo_code
        person.identification = identification
        person.name = name
        person.package = package
        person.status = status
        db.commit()
        return jsonify({"ok": True, "person": serialize(person), "msg": "Enrollment updated successfully."})

@app.route("/api/delete/<path:person_id>", methods=["DELETE"])
@login_required
def delete_person(person_id):
    user = current_user()
    with SessionLocal() as db:
        person = db.get(Person, person_id)
        if not person:
            return jsonify({"ok": False, "msg": "Enrollment not found."}), 404
        if not user.is_admin and person.sede != user.sede:
            return jsonify({"ok": False, "msg": "You do not have permission to delete an enrollment from another branch."}), 403
        name = person.name
        db.delete(person)
        db.commit()
        count = db.scalar(select(func.count()).select_from(Person))
        return jsonify({"ok": True, "msg": f"🗑️ {name} removed from the enrollment list.", "disponibles": TOTAL_CUPOS - count})

@app.route("/api/change-password", methods=["POST"])
@login_required
def change_password():
    data = request.get_json() or {}
    old_password = data.get("old_password") or ""
    new_password = data.get("new_password") or ""
    if len(new_password) < 8:
        return jsonify({"ok": False, "msg": "The new password must be at least 8 characters long."}), 400
    username = session.get("username")
    with SessionLocal() as db:
        user = db.get(User, username)
        if not user or not check_password_hash(user.password_hash, old_password):
            return jsonify({"ok": False, "msg": "The current password is incorrect."}), 400
        user.password_hash = generate_password_hash(new_password)
        db.commit()
    return jsonify({"ok": True, "msg": "Password updated successfully."})

@app.route("/api/admin/set-password", methods=["POST"])
@login_required
def admin_set_password():
    user = current_user()
    if not user.is_admin:
        return jsonify({"ok": False, "msg": "Only the administrator can configure user passwords."}), 403
    data = request.get_json() or {}
    username = (data.get("username") or "").strip()
    new_password = data.get("new_password") or ""
    if username not in {"admin", "NORTE", "SAN_FERNANDO", "LIMONAR"}:
        return jsonify({"ok": False, "msg": "Invalid user."}), 400
    if len(new_password) < 8:
        return jsonify({"ok": False, "msg": "Password must be at least 8 characters long."}), 400
    with SessionLocal() as db:
        target = db.get(User, username)
        if not target:
            return jsonify({"ok": False, "msg": "User not found."}), 404
        target.password_hash = generate_password_hash(new_password)
        db.commit()
    return jsonify({"ok": True, "msg": f"Password for {username} updated."})

@app.get("/healthz")
def healthz():
    try:
        with SessionLocal() as db:
            db.execute(select(func.count()).select_from(Person))
        return jsonify({"status": "ok"})
    except Exception:
        return jsonify({"status": "error"}), 503

seed_database()
seed_users()

if __name__ == "__main__":
    print("Enrollment System — November 2026 Campaign")
    print("Local: http://127.0.0.1:5000")
    app.run(host="0.0.0.0", debug=False, port=int(os.environ.get("PORT", 5000)))
