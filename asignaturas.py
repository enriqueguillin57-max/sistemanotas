from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import ejecutar

bp_asignaturas = Blueprint("asignaturas", __name__, url_prefix="/asignaturas")


def _docentes():
    return ejecutar(
        """SELECT id_docente, nombre, apellido FROM docentes
           WHERE estado='Activo' ORDER BY apellido""",
        fetch="all",
    )


@bp_asignaturas.route("/")
def lista():
    asignaturas = ejecutar(
        """SELECT a.id_asignatura, a.nombre, a.descripcion, a.nivel,
                  a.id_docente, CONCAT(d.nombre,' ',d.apellido) AS docente
           FROM asignaturas a
           JOIN docentes d ON d.id_docente = a.id_docente
           ORDER BY a.nombre""",
        fetch="all",
    )
    return render_template("asignaturas/lista.html", asignaturas=asignaturas)


@bp_asignaturas.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        datos = {
            "nombre": request.form["nombre"].strip(),
            "descripcion": request.form.get("descripcion", "").strip(),
            "nivel": request.form.get("nivel", "").strip(),
            "id_docente": request.form["id_docente"],
        }
        try:
            ejecutar(
                """INSERT INTO asignaturas (nombre, descripcion, nivel, id_docente)
                   VALUES (%(nombre)s, %(descripcion)s, %(nivel)s, %(id_docente)s)""",
                datos,
                fetch="none",
            )
            flash("Asignatura registrada.", "success")
            return redirect(url_for("asignaturas.lista"))
        except Exception as e:
            flash(f"Error al guardar: {e}", "danger")

    return render_template("asignaturas/crear.html", docentes=_docentes())


@bp_asignaturas.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    asignatura = ejecutar(
        "SELECT * FROM asignaturas WHERE id_asignatura = %s", (id,), fetch="one"
    )
    if not asignatura:
        flash("Asignatura no encontrada.", "warning")
        return redirect(url_for("asignaturas.lista"))

    if request.method == "POST":
        datos = {
            "id": id,
            "nombre": request.form["nombre"].strip(),
            "descripcion": request.form.get("descripcion", "").strip(),
            "nivel": request.form.get("nivel", "").strip(),
            "id_docente": request.form["id_docente"],
        }
        try:
            ejecutar(
                """UPDATE asignaturas
                   SET nombre=%(nombre)s, descripcion=%(descripcion)s,
                       nivel=%(nivel)s, id_docente=%(id_docente)s
                   WHERE id_asignatura=%(id)s""",
                datos,
                fetch="none",
            )
            flash("Asignatura actualizada.", "success")
            return redirect(url_for("asignaturas.lista"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    return render_template(
        "asignaturas/editar.html", asignatura=asignatura, docentes=_docentes()
    )


@bp_asignaturas.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        ejecutar(
            "DELETE FROM asignaturas WHERE id_asignatura = %s", (id,), fetch="none"
        )
        flash("Asignatura eliminada.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("asignaturas.lista"))
