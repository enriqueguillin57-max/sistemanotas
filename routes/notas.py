from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import ejecutar_consulta

notas_bp = Blueprint("notas", __name__, url_prefix="/notas")


def _validar_notas(nota1, nota2, examen):
    try:
        valores = [float(nota1), float(nota2), float(examen)]
    except ValueError:
        return "Las notas deben ser numéricas."

    if any(valor < 0 or valor > 10 for valor in valores):
        return "Las notas deben estar entre 0 y 10."

    return None


@notas_bp.route("/")
def index():
    notas = ejecutar_consulta(
        """SELECT n.*,
                  CONCAT(e.nombre, ' ', e.apellido) AS estudiante,
                  a.nombre AS asignatura
             FROM notas n
             JOIN estudiantes e ON e.id_estudiante = n.id_estudiante
             JOIN asignaturas a ON a.id_asignatura = n.id_asignatura
            ORDER BY n.id_nota DESC""",
        fetchall=True,
    )
    return render_template("notas/index.html", notas=notas)


@notas_bp.route("/crear", methods=["GET", "POST"])
def crear():
    estudiantes = ejecutar_consulta(
        "SELECT id_estudiante, nombre, apellido FROM estudiantes ORDER BY apellido",
        fetchall=True,
    )
    asignaturas = ejecutar_consulta(
        "SELECT id_asignatura, nombre FROM asignaturas ORDER BY nombre", fetchall=True
    )

    if request.method == "POST":
        id_estudiante = request.form["id_estudiante"]
        id_asignatura = request.form["id_asignatura"]
        nota1 = request.form["nota1"]
        nota2 = request.form["nota2"]
        examen = request.form["examen"]
        observacion = request.form.get("observacion", "").strip()

        error = _validar_notas(nota1, nota2, examen)
        if error:
            flash(error, "danger")
            return redirect(url_for("notas.crear"))

        ejecutar_consulta(
            """INSERT INTO notas
               (id_estudiante, id_asignatura, nota1, nota2, examen, observacion)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (id_estudiante, id_asignatura, nota1, nota2, examen, observacion),
            commit=True,
        )
        flash("Nota registrada correctamente.", "success")
        return redirect(url_for("notas.index"))

    return render_template(
        "notas/crear.html", estudiantes=estudiantes, asignaturas=asignaturas
    )


@notas_bp.route("/editar/<int:id_nota>", methods=["GET", "POST"])
def editar(id_nota):
    nota = ejecutar_consulta(
        "SELECT * FROM notas WHERE id_nota = %s", (id_nota,), fetchone=True
    )
    estudiantes = ejecutar_consulta(
        "SELECT id_estudiante, nombre, apellido FROM estudiantes ORDER BY apellido",
        fetchall=True,
    )
    asignaturas = ejecutar_consulta(
        "SELECT id_asignatura, nombre FROM asignaturas ORDER BY nombre", fetchall=True
    )

    if not nota:
        flash("Nota no encontrada.", "warning")
        return redirect(url_for("notas.index"))

    if request.method == "POST":
        nota1 = request.form["nota1"]
        nota2 = request.form["nota2"]
        examen = request.form["examen"]
        observacion = request.form.get("observacion", "").strip()

        error = _validar_notas(nota1, nota2, examen)
        if error:
            flash(error, "danger")
            return redirect(url_for("notas.editar", id_nota=id_nota))

        # El promedio lo calcula MySQL automáticamente (columna generada)
        ejecutar_consulta(
            """UPDATE notas
                  SET nota1=%s, nota2=%s, examen=%s, observacion=%s
                WHERE id_nota=%s""",
            (nota1, nota2, examen, observacion, id_nota),
            commit=True,
        )
        flash("Nota actualizada correctamente.", "success")
        return redirect(url_for("notas.index"))

    return render_template(
        "notas/editar.html",
        nota=nota,
        estudiantes=estudiantes,
        asignaturas=asignaturas,
    )


@notas_bp.route("/eliminar/<int:id_nota>", methods=["POST", "GET"])
def eliminar(id_nota):
    ejecutar_consulta("DELETE FROM notas WHERE id_nota = %s", (id_nota,), commit=True)
    flash("Nota eliminada correctamente.", "success")
    return redirect(url_for("notas.index"))
