from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import ejecutar

bp_notas = Blueprint("notas", __name__, url_prefix="/notas")


def _combos():
    estudiantes = ejecutar(
        """SELECT id_estudiante, nombre, apellido FROM estudiantes
           WHERE estado='Activo' ORDER BY apellido""",
        fetch="all",
    )
    asignaturas = ejecutar(
        "SELECT id_asignatura, nombre FROM asignaturas ORDER BY nombre", fetch="all"
    )
    return estudiantes, asignaturas


@bp_notas.route("/")
def lista():
    notas = ejecutar(
        """SELECT n.id_nota, n.nota1, n.nota2, n.examen, n.promedio,
                  n.observacion, n.fecha_actualizacion,
                  CONCAT(e.nombre,' ',e.apellido) AS estudiante,
                  a.nombre AS asignatura
           FROM notas n
           JOIN estudiantes e ON e.id_estudiante = n.id_estudiante
           JOIN asignaturas a ON a.id_asignatura = n.id_asignatura
           ORDER BY e.apellido, a.nombre""",
        fetch="all",
    )
    return render_template("notas/lista.html", notas=notas)


@bp_notas.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        datos = {
            "id_estudiante": request.form["id_estudiante"],
            "id_asignatura": request.form["id_asignatura"],
            "nota1": request.form["nota1"],
            "nota2": request.form["nota2"],
            "examen": request.form["examen"],
            "observacion": request.form.get("observacion", "").strip(),
        }
        try:
            ejecutar(
                """INSERT INTO notas
                   (id_estudiante, id_asignatura, nota1, nota2, examen, observacion)
                   VALUES (%(id_estudiante)s, %(id_asignatura)s, %(nota1)s,
                           %(nota2)s, %(examen)s, %(observacion)s)""",
                datos,
                fetch="none",
            )
            flash("Nota registrada.", "success")
            return redirect(url_for("notas.lista"))
        except Exception as e:
            flash(f"Error al guardar: {e}", "danger")

    estudiantes, asignaturas = _combos()
    return render_template(
        "notas/crear.html", estudiantes=estudiantes, asignaturas=asignaturas
    )


@bp_notas.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    nota = ejecutar("SELECT * FROM notas WHERE id_nota = %s", (id,), fetch="one")
    if not nota:
        flash("Nota no encontrada.", "warning")
        return redirect(url_for("notas.lista"))

    if request.method == "POST":
        datos = {
            "id": id,
            "nota1": request.form["nota1"],
            "nota2": request.form["nota2"],
            "examen": request.form["examen"],
            "observacion": request.form.get("observacion", "").strip(),
        }
        try:
            ejecutar(
                """UPDATE notas
                   SET nota1=%(nota1)s, nota2=%(nota2)s, examen=%(examen)s,
                       observacion=%(observacion)s
                   WHERE id_nota=%(id)s""",
                datos,
                fetch="none",
            )
            flash("Nota actualizada.", "success")
            return redirect(url_for("notas.lista"))
        except Exception as e:
            flash(f"Error al actualizar: {e}", "danger")

    estudiantes, asignaturas = _combos()
    return render_template(
        "notas/editar.html",
        nota=nota,
        estudiantes=estudiantes,
        asignaturas=asignaturas,
    )


@bp_notas.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    try:
        ejecutar("DELETE FROM notas WHERE id_nota = %s", (id,), fetch="none")
        flash("Nota eliminada.", "success")
    except Exception as e:
        flash(f"No se pudo eliminar: {e}", "danger")
    return redirect(url_for("notas.lista"))
