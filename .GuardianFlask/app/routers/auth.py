from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message

from app.models import db, Usuario
from app.helpers import (
    hash_password, verify_password,
    generate_reset_token, verify_reset_token
)

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ──────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        email      = request.form.get("email", "").strip()
        password   = request.form.get("password", "")
        remember   = request.form.get("remember") == "on"

        usuario = Usuario.query.filter_by(Email=email).first()

        if not usuario or not verify_password(usuario.Contraseña, password):
            flash("Correo o contraseña incorrectos.", "error")
            return render_template("auth/login.html")

        login_user(usuario, remember=remember)
        next_page = request.args.get("next")
        return redirect(next_page or url_for("dashboard.index"))

    return render_template("auth/login.html")


# ──────────────────────────────────────────────
# REGISTRO
# ──────────────────────────────────────────────
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":
        nombre    = request.form.get("nombre", "").strip()
        email     = request.form.get("email", "").strip()
        telefono  = request.form.get("telefono", "").strip()
        password  = request.form.get("password", "")
        confirm   = request.form.get("confirm_password", "")

        # Validaciones
        if not nombre or not email or not password:
            flash("Todos los campos obligatorios deben completarse.", "error")
            return render_template("auth/register.html")

        if password != confirm:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("auth/register.html")

        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            return render_template("auth/register.html")

        if Usuario.query.filter_by(Email=email).first():
            flash("Ya existe una cuenta con ese correo electrónico.", "error")
            return render_template("auth/register.html")

        # Crear usuario
        nuevo = Usuario(
            Nombre     = nombre,
            Email      = email,
            Telefono   = telefono or None,
            Contraseña = hash_password(password),
            Rol        = "Civil"
        )
        db.session.add(nuevo)
        db.session.commit()

        flash("¡Cuenta creada exitosamente! Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


# ──────────────────────────────────────────────
# LOGOUT
# ──────────────────────────────────────────────
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("auth.login"))


# ──────────────────────────────────────────────
# RECUPERAR CONTRASEÑA - Paso 1: Ingresar correo
# ──────────────────────────────────────────────
@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        from app import mail  # importación diferida para evitar circular imports

        email   = request.form.get("email", "").strip()
        usuario = Usuario.query.filter_by(Email=email).first()

        # Siempre mostrar el mismo mensaje (seguridad: no revelar si el email existe)
        flash("Si ese correo está registrado, recibirás un código de recuperación.", "info")

        if usuario:
            token = generate_reset_token(email)
            # Guardamos el token en sesión para verificar en el paso 2
            session["reset_token"] = token
            session["reset_email"] = email

            enlace = url_for("auth.reset_verify_token",
                             token=token, _external=True)

            msg = Message(
                subject = "Guardian Zero – Recuperación de contraseña",
                recipients = [email],
                html = f"""
                <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;
                            border:1px solid #e0e0e0;border-radius:12px;overflow:hidden;">
                  <div style="background:#1a6b73;padding:24px;text-align:center;">
                    <h1 style="color:#fff;margin:0;font-size:22px;">Guardian Zero</h1>
                  </div>
                  <div style="padding:32px;">
                    <h2 style="color:#1a3a4a;margin-top:0;">Recuperación de contraseña</h2>
                    <p style="color:#555;">Hola <strong>{usuario.Nombre}</strong>,</p>
                    <p style="color:#555;">
                      Recibimos una solicitud para restablecer tu contraseña.
                      Haz clic en el botón a continuación. El enlace expira en
                      <strong>30 minutos</strong>.
                    </p>
                    <div style="text-align:center;margin:32px 0;">
                      <a href="{enlace}"
                         style="background:#1a9ea8;color:#fff;text-decoration:none;
                                padding:14px 32px;border-radius:8px;font-size:16px;
                                font-weight:bold;">
                        Restablecer contraseña
                      </a>
                    </div>
                    <p style="color:#888;font-size:13px;">
                      Si no solicitaste esto, ignora este correo.
                    </p>
                  </div>
                </div>
                """
            )
            try:
                mail.send(msg)
            except Exception as e:
                # Log del error pero no lo mostramos al usuario
                print(f"[MAIL ERROR] {e}")

        return redirect(url_for("auth.forgot_password"))

    return render_template("auth/forgot_password.html")


# ──────────────────────────────────────────────
# RECUPERAR CONTRASEÑA - Paso 2: Verificar token
# (El usuario llega desde el enlace del correo)
# ──────────────────────────────────────────────
@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_verify_token(token):
    email = verify_reset_token(token)
    if not email:
        flash("El enlace ha expirado o es inválido. Solicita uno nuevo.", "error")
        return redirect(url_for("auth.forgot_password"))

    # Guardamos en sesión para el paso 3
    session["verified_reset_email"] = email
    return redirect(url_for("auth.reset_password"))


# ──────────────────────────────────────────────
# RECUPERAR CONTRASEÑA - Paso 3: Nueva contraseña
# ──────────────────────────────────────────────
@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    email = session.get("verified_reset_email")
    if not email:
        flash("Sesión de recuperación inválida. Inicia el proceso de nuevo.", "error")
        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")

        if not password or len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error")
            return render_template("auth/reset_password.html")

        if password != confirm:
            flash("Las contraseñas no coinciden.", "error")
            return render_template("auth/reset_password.html")

        usuario = Usuario.query.filter_by(Email=email).first()
        if not usuario:
            flash("Usuario no encontrado.", "error")
            return redirect(url_for("auth.login"))

        usuario.Contraseña = hash_password(password)
        db.session.commit()

        session.pop("verified_reset_email", None)
        session.pop("reset_token", None)
        session.pop("reset_email", None)

        flash("¡Contraseña actualizada exitosamente! Ya puedes iniciar sesión.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/reset_password.html")