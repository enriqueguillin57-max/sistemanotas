from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import ejecutar

bp_estudiantes = Blueprint("estudiantes", __name__, url_prefix="/estudiantes")


@bp_estudiantes.route("/")
def lista():
    estudiantes = ejecutar(
        """SELECT id_estudiante, cedula, nombre, apellido, correo,
                  fecha_nacimiento, estado, fecha_registro
           FROM estudiantes ORDER BY apellido, nombre""",
        fetch="all",
    )
    return render_template("estudiantes/lista.html", estudiantes=estudiantes)


@bp_estudiantes.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        datos = {
            "cedula": request.form["cedula"].strip(),
            "nombre": request.form["nombre"].strip(),
            "apellido": request.form["apellido"].strip(),
            "correo": request.form["correo"].strip(),
            "fecha_nacimiento": request.form.get("fecha_nacimiento") or None,
            "estado": request.form.get("estado", "Activo"),
        }
        try:
            ejecutar(
                """INSERT INTO estudiantes
                   (cedula, nombre, apellido, correo, fecha_nacimiento, estado)
                   VALUES (%(cedula)s, %(nombre)s, %(apellido)s, %(correo)s,
                           %(fecha_nacimiento)s, %(estado)s)""",
                datos,
                fetch="none",
            )
            flash("Estudiante registrado correctamente.", "success")
            return redirect(url_for("estudiantes.lista"))
        except Exception as e:
            flash(f"Error al guardar: {e}", "danger")

    return render_template("estudiantes/crear.html")


@bp_estudiantes.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    estudiante = ejecutar(
        "SELECT * FROM estudiantes WHERE id_estudiante = %s", (id,), fetch="one"
    )
    if not estudiante:
        flash("Estudiante no encontrado.", "warning")
        return redirect(url_for("estudiantes.lista"))

    if request.method == "POST":
        datos = {
            "id": id,
            "cedula": request.form["cedula"].strip(),
            "nombre": request.form["nombre"].strip(),
            "apellido": request.form["apellido"].strip(),
            "correo": request.form["correo"].strip(),
            "fecha_nacimiento": request.form.get("fecha_nacimiento") or None,
            "estado": request.form.get("estado", "Activo"),
        }
        try:
            ejecutar(
                """UPDATE estudiantes
                   SET cedula=%(cedula)s, nombre=%(nombre)s, apellido=%(apellido)s,
                       correo=%(correo)s, fecha_nacimiento=%(fecha_nacimiento)s,
                       estado=%(estado)s
                   WHERE id_estudiante=%(id)s""",
                datos,
                fetch="none",
            )
            flash("Estudiante actualizado.", "success")
            return redirect(url_for("estudiantes.lista"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    return render_template("estudiantes/editar.html", estudiante=estudiante)


@bp_estudiantes.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        ejecutar(
            "DELETE FROM estudiantes WHERE id_estudiante = %s", (id,), fetch="none"
        )
        flash("Estudiante eliminado.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("estudiantes.lista"))
