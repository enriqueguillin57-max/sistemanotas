from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import ejecutar_consulta

estudiantes_bp = Blueprint("estudiantes", __name__, url_prefix="/estudiantes")


# ---------- READ (lista) ----------
@estudiantes_bp.route("/")
def index():
    estudiantes = ejecutar_consulta(
        "SELECT * FROM estudiantes ORDER BY id_estudiante DESC", fetchall=True
    )
    return render_template("estudiantes/index.html", estudiantes=estudiantes)


@estudiantes_bp.route("/lista")
def lista():
    estudiantes = ejecutar_consulta(
        "SELECT * FROM estudiantes ORDER BY apellido, nombre", fetchall=True
    )
    return render_template("estudiantes/lista.html", estudiantes=estudiantes)


# ---------- CREATE ----------
@estudiantes_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        cedula = request.form["cedula"].strip()
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        correo = request.form["correo"].strip()
        fecha_nacimiento = request.form.get("fecha_nacimiento") or None
        estado = request.form.get("estado", "Activo")

        if not cedula or not nombre or not apellido or not correo:
            flash("Todos los campos obligatorios deben estar llenos.", "danger")
            return redirect(url_for("estudiantes.crear"))

        ejecutar_consulta(
            """INSERT INTO estudiantes
               (cedula, nombre, apellido, correo, fecha_nacimiento, estado)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (cedula, nombre, apellido, correo, fecha_nacimiento, estado),
            commit=True,
        )
        flash("Estudiante registrado correctamente.", "success")
        return redirect(url_for("estudiantes.lista"))

    return render_template("estudiantes/crear.html")


@estudiantes_bp.route("/formulario")
def formulario():
    return render_template("estudiantes/formulario.html")


# ---------- UPDATE ----------
@estudiantes_bp.route("/editar/<int:id_estudiante>", methods=["GET", "POST"])
def editar(id_estudiante):
    estudiante = ejecutar_consulta(
        "SELECT * FROM estudiantes WHERE id_estudiante = %s",
        (id_estudiante,),
        fetchone=True,
    )
    if not estudiante:
        flash("Estudiante no encontrado.", "warning")
        return redirect(url_for("estudiantes.lista"))

    if request.method == "POST":
        cedula = request.form["cedula"].strip()
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        correo = request.form["correo"].strip()
        fecha_nacimiento = request.form.get("fecha_nacimiento") or None
        estado = request.form.get("estado", "Activo")

        ejecutar_consulta(
            """UPDATE estudiantes
                  SET cedula=%s, nombre=%s, apellido=%s, correo=%s,
                      fecha_nacimiento=%s, estado=%s
                WHERE id_estudiante=%s""",
            (cedula, nombre, apellido, correo, fecha_nacimiento, estado, id_estudiante),
            commit=True,
        )
        flash("Estudiante actualizado correctamente.", "success")
        return redirect(url_for("estudiantes.lista"))

    return render_template("estudiantes/editar.html", estudiante=estudiante)


# ---------- DELETE ----------
@estudiantes_bp.route("/eliminar/<int:id_estudiante>", methods=["POST", "GET"])
def eliminar(id_estudiante):
    ejecutar_consulta(
        "DELETE FROM estudiantes WHERE id_estudiante = %s",
        (id_estudiante,),
        commit=True,
    )
    flash("Estudiante eliminado correctamente.", "success")
    return redirect(url_for("estudiantes.lista"))
