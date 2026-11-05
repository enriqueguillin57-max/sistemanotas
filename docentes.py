from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import ejecutar

bp_docentes = Blueprint("docentes", __name__, url_prefix="/docentes")


@bp_docentes.route("/")
def lista():
    docentes = ejecutar(
        """SELECT id_docente, cedula, nombre, apellido, correo,
                  especialidad, estado
           FROM docentes ORDER BY apellido, nombre""",
        fetch="all",
    )
    return render_template("docentes/lista.html", docentes=docentes)


@bp_docentes.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        datos = {
            "cedula": request.form["cedula"].strip(),
            "nombre": request.form["nombre"].strip(),
            "apellido": request.form["apellido"].strip(),
            "correo": request.form["correo"].strip(),
            "especialidad": request.form.get("especialidad", "").strip(),
            "estado": request.form.get("estado", "Activo"),
        }
        try:
            ejecutar(
                """INSERT INTO docentes
                   (cedula, nombre, apellido, correo, especialidad, estado)
                   VALUES (%(cedula)s, %(nombre)s, %(apellido)s, %(correo)s,
                           %(especialidad)s, %(estado)s)""",
                datos,
                fetch="none",
            )
            flash("Docente registrado correctamente.", "success")
            return redirect(url_for("docentes.lista"))
        except Exception as e:
            flash(f"Error al guardar: {e}", "danger")

    return render_template("docentes/crear.html")


@bp_docentes.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    docente = ejecutar(
        "SELECT * FROM docentes WHERE id_docente = %s", (id,), fetch="one"
    )
    if not docente:
        flash("Docente no encontrado.", "warning")
        return redirect(url_for("docentes.lista"))

    if request.method == "POST":
        datos = {
            "id": id,
            "cedula": request.form["cedula"].strip(),
            "nombre": request.form["nombre"].strip(),
            "apellido": request.form["apellido"].strip(),
            "correo": request.form["correo"].strip(),
            "especialidad": request.form.get("especialidad", "").strip(),
            "estado": request.form.get("estado", "Activo"),
        }
        try:
            ejecutar(
                """UPDATE docentes
                   SET cedula=%(cedula)s, nombre=%(nombre)s, apellido=%(apellido)s,
                       correo=%(correo)s, especialidad=%(especialidad)s,
                       estado=%(estado)s
                   WHERE id_docente=%(id)s""",
                datos,
                fetch="none",
            )
            flash("Docente actualizado.", "success")
            return redirect(url_for("docentes.lista"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    return render_template("docentes/editar.html", docente=docente)


@bp_docentes.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        ejecutar("DELETE FROM docentes WHERE id_docente = %s", (id,), fetch="none")
        flash("Docente eliminado.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar (puede tener asignaturas): {e}", "danger")
    return redirect(url_for("docentes.lista"))
