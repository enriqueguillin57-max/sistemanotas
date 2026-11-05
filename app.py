from flask import Flask, redirect, url_for
from routes.estudiantes import bp_estudiantes
from routes.docentes import bp_docentes
from routes.asignaturas import bp_asignaturas
from routes.notas import bp_notas

app = Flask(__name__)
app.secret_key = "cambia_esta_clave_secreta"

# Registrar blueprints
app.register_blueprint(bp_estudiantes)
app.register_blueprint(bp_docentes)
app.register_blueprint(bp_asignaturas)
app.register_blueprint(bp_notas)


@app.route("/")
def inicio():
    return redirect(url_for("estudiantes.lista"))


if __name__ == "__main__":
    app.run(debug=True)
