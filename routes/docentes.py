from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import ejecutar_consulta

docentes_bp = Blueprint("docentes", __name__, url_prefix="/docentes")


# ---------- READ ----------
@docentes_bp.route("/")
def index():
    docentes = ejecutar_consulta(
        "SELECT * FROM docentes ORDER BY id_docente DESC", fetchall=True
    )
    return render_template("docentes/index.html", docentes=docentes)


@docentes_bp.route("/lista")
def lista():
    docentes = ejecutar_consulta(
        "SELECT * FROM docentes ORDER BY apellido, nombre", fetchall=True
    )
    return render_template("docentes/lista.html", docentes=docentes)


# ---------- CREATE ----------
@docentes_bp.route("/crear", methods=["GET", "POST"])
def crear():
    if request.method == "POST":
        cedula = request.form["cedula"].strip()
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        correo = request.form["correo"].strip()
        especialidad = request.form.get("especialidad", "").strip()
        estado = request.form.get("estado", "Activo")

        if not cedula or not nombre or not apellido or not correo:
            flash("Todos los campos obligatorios deben estar llenos.", "danger")
            return redirect(url_for("docentes.crear"))

        ejecutar_consulta(
            """INSERT INTO docentes
               (cedula, nombre, apellido, correo, especialidad, estado)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (cedula, nombre, apellido, correo, especialidad, estado),
            commit=True,
        )
        flash("Docente registrado correctamente.", "success")
        return redirect(url_for("docentes.lista"))

    return render_template("docentes/crear.html")


@docentes_bp.route("/formulario")
def formulario():
    return render_template("docentes/formulario.html")


# ---------- UPDATE ----------
@docentes_bp.route("/editar/<int:id_docente>", methods=["GET", "POST"])
def editar(id_docente):
    docente = ejecutar_consulta(
        "SELECT * FROM docentes WHERE id_docente = %s", (id_docente,), fetchone=True
    )
    if not docente:
        flash("Docente no encontrado.", "warning")
        return redirect(url_for("docentes.lista"))

    if request.method == "POST":
        cedula = request.form["cedula"].strip()
        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        correo = request.form["correo"].strip()
        especialidad = request.form.get("especialidad", "").strip()
        estado = request.form.get("estado", "Activo")

        ejecutar_consulta(
            """UPDATE docentes
                  SET cedula=%s, nombre=%s, apellido=%s, correo=%s,
                      especialidad=%s, estado=%s
                WHERE id_docente=%s""",
            (cedula, nombre, apellido, correo, especialidad, estado, id_docente),
            commit=True,
        )
        flash("Docente actualizado correctamente.", "success")
        return redirect(url_for("docentes.lista"))

    return render_template("docentes/editar.html", docente=docente)


# ---------- DELETE ----------
@docentes_bp.route("/eliminar/<int:id_docente>", methods=["POST", "GET"])
def eliminar(id_docente):
    ejecutar_consulta(
        "DELETE FROM docentes WHERE id_docente = %s", (id_docente,), commit=True
    )
    flash("Docente eliminado correctamente.", "success")
    return redirect(url_for("docentes.lista"))
