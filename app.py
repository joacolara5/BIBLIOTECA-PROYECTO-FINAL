# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from sqlalchemy.exc import NoResultFound
from base import Base, engine, SessionLocal
from model import Usuario, Libro, Categoria
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret")

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Configuración de sesión y login
db = SessionLocal()
login_manager = LoginManager(app)
login_manager.login_view = "auth"

@login_manager.user_loader
def load_user(user_id):
    return db.query(Usuario).get(int(user_id))


@app.context_processor
def inject_user():
    return dict(username=(current_user.username if current_user.is_authenticated else ""))


# --- Rutas de autenticación ---
@app.route("/", methods=["GET", "POST"])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        action = request.form.get("action")
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if action == "register":
            if db.query(Usuario).filter_by(username=username).first():
                flash("El usuario ya existe", "danger")
            else:
                u = Usuario(username=username)
                u.set_password(password)
                db.add(u); db.commit()
                flash("Usuario creado. Inicia sesión.", "success")
                return redirect(url_for("auth"))

        elif action == "login":
            u = db.query(Usuario).filter_by(username=username).first()
            if u and u.check_password(password):
                login_user(u)
                flash("Sesión iniciada", "success")
                return redirect(url_for("index"))
            else:
                flash("Credenciales inválidas", "danger")

    return render_template("auth.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión", "info")
    return redirect(url_for("auth"))


# --- Páginas principales ---
@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/libros")
@login_required
def libros_page():
    books = db.query(Libro).all()
    # pasar lista de dicts
    return render_template("libros.html", books=[{
        "title": b.titulo,
        "author": b.autor,
        "description": b.descripcion,
        "img_url": b.imagen_url
    } for b in books])


@app.route("/masinfo")
@login_required
def masinfo_page():
    total_books = db.query(Libro).count()
    total_cats = db.query(Categoria).count()
    total_users = db.query(Usuario).count()
    stats = {
        "total_books": total_books,
        "total_categories": total_cats,
        "total_users": total_users
    }
    return render_template("masinfo.html", stats=stats)


@app.route("/instalaciones")
@login_required
def instalaciones_page():
    return render_template("instalaciones.html")


@app.route("/contacto")
@login_required
def contacto_page():
    return render_template("contacto.html")


# --- API REST (opcional) ---
@app.route("/api/libros", methods=["GET"])
@login_required
def api_libros():
    books = db.query(Libro).all()
    return jsonify([{
        "id": b.id,
        "titulo": b.titulo,
        "autor": b.autor,
        "descripcion": b.descripcion,
        "imagen_url": b.imagen_url
    } for b in books])


# Manejo de errores
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
