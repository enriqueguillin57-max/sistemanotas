from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import ejecutar_consulta

asignaturas_bp = Blueprint("asignaturas", __name__, url_prefix="/asignaturas")


@asignaturas_bp.route("/")
def index():
    asignaturas = ejecutar_consulta(
        """SELECT a.*, CONCAT(d.nombre, ' ', d.apellido) AS docente
             FROM asignaturas a
             JOIN docentes d ON d.id_docente = a.id_docente
            ORDER BY a.id_asignatura DESC""",
        fetchall=True,
    )
    return render_template("asignaturas/index.html", asignaturas=asignaturas)


@asignaturas_bp.route("/crear", methods=["GET", "POST"])
def crear():
    docentes = ejecutar_consulta(
        "SELECT id_docente, nombre, apellido FROM docentes ORDER BY apellido", fetchall=True
    )
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form.get("descripcion", "").strip()
        nivel = request.form.get("nivel", "").strip()
        id_docente = request.form["id_docente"]

        if not nombre or not id_docente:
            flash("Nombre y docente son obligatorios.", "danger")
            return redirect(url_for("asignaturas.crear"))

        ejecutar_consulta(
            """INSERT INTO asignaturas (nombre, descripcion, nivel, id_docente)
               VALUES (%s, %s, %s, %s)""",
            (nombre, descripcion, nivel, id_docente),
            commit=True,
        )
        flash("Asignatura registrada correctamente.", "success")
        return redirect(url_for("asignaturas.index"))

    return render_template("asignaturas/crear.html", docentes=docentes)


@asignaturas_bp.route("/editar/<int:id_asignatura>", methods=["GET", "POST"])
def editar(id_asignatura):
    asignatura = ejecutar_consulta(
        "SELECT * FROM asignaturas WHERE id_asignatura = %s",
        (id_asignatura,),
        fetchone=True,
    )
    docentes = ejecutar_consulta(
        "SELECT id_docente, nombre, apellido FROM docentes ORDER BY apellido", fetchall=True
    )
    if not asignatura:
        flash("Asignatura no encontrada.", "warning")
        return redirect(url_for("asignaturas.index"))

    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        descripcion = request.form.get("descripcion", "").strip()
        nivel = request.form.get("nivel", "").strip()
        id_docente = request.form["id_docente"]

        ejecutar_consulta(
            """UPDATE asignaturas
                  SET nombre=%s, descripcion=%s, nivel=%s, id_docente=%s
                WHERE id_asignatura=%s""",
            (nombre, descripcion, nivel, id_docente, id_asignatura),
            commit=True,
        )
        flash("Asignatura actualizada correctamente.", "success")
        return redirect(url_for("asignaturas.index"))

    return render_template(
        "asignaturas/editar.html", asignatura=asignatura, docentes=docentes
    )


@asignaturas_bp.route("/eliminar/<int:id_asignatura>", methods=["POST", "GET"])
def eliminar(id_asignatura):
    ejecutar_consulta(
        "DELETE FROM asignaturas WHERE id_asignatura = %s",
        (id_asignatura,),
        commit=True,
    )
    flash("Asignatura eliminada correctamente.", "success")
    return redirect(url_for("asignaturas.index"))
