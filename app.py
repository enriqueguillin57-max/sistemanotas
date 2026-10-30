from flask import Flask, render_template
from routes.estudiantes import estudiantes_bp
from routes.docentes import docentes_bp
from routes.asignaturas import asignaturas_bp
from routes.notas import notas_bp

app = Flask(__name__)
app.secret_key = "sistema_notas_secret_key"

# =========================================
# Registro de Blueprints (rutas)
# =========================================
app.register_blueprint(estudiantes_bp)
app.register_blueprint(docentes_bp)
app.register_blueprint(asignaturas_bp)
app.register_blueprint(notas_bp)


@app.route("/")
def inicio():
    return render_template("base.html")


if __name__ == "__main__":
    # debug=True para desarrollo
    app.run(debug=True, host="0.0.0.0", port=5000)
