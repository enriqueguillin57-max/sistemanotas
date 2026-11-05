# 🎓 Sistema de Notas — Flask + MySQL

Aplicación web CRUD para la gestión de estudiantes, docentes, asignaturas y notas,
desarrollada con **Python (Flask)** y **MySQL** sobre **XAMPP**.

## 📋 Descripción

El sistema permite administrar cuatro entidades relacionadas:

- 🎓 **Estudiantes** — datos personales y estado académico.
- 👨‍🏫 **Docentes** — datos personales y especialidad.
- 📚 **Asignaturas** — cada asignatura pertenece a un docente.
- 📝 **Notas** — nota1, nota2 y examen por estudiante/asignatura, con
  **promedio calculado automáticamente** por MySQL (columna generada).

Cada módulo implementa las operaciones **Crear, Leer, Actualizar y Eliminar**.

## 🛠️ Tecnologías

| Componente | Versión |
|---|---|
| Python | 3.10+ |
| Flask | 3.0.3 |
| MySQL | 8.0.16+ (XAMPP) |
| PyMySQL | 1.1.1 |
| DBUtils | 3.1.0 |

## 📁 Estructura del proyecto

    sistema_notas/
    ├── app.py
    ├── db.py
    ├── requirements.txt
    ├── base_datos.sql
    ├── static/
    │   ├── css/estilo.css
    │   └── img/logo.png
    ├── templates/
    │   ├── base.html
    │   ├── estudiantes/
    │   ├── docentes/
    │   ├── asignaturas/
    │   └── notas/
    └── routes/
        ├── __init__.py
        ├── estudiantes.py
        ├── docentes.py
        ├── asignaturas.py
        └── notas.py

## 🗺️ Rutas disponibles

| Método | Ruta | Acción |
|---|---|---|
| GET | `/estudiantes/` | Listar estudiantes |
| GET/POST | `/estudiantes/crear` | Crear estudiante |
| GET/POST | `/estudiantes/editar/<id>` | Editar estudiante |
| POST | `/estudiantes/eliminar/<id>` | Eliminar estudiante |
| GET | `/docentes/` | Listar docentes |
| GET/POST | `/docentes/crear` | Crear docente |
| GET/POST | `/docentes/editar/<id>` | Editar docente |
| POST | `/docentes/eliminar/<id>` | Eliminar docente |
| GET | `/asignaturas/` | Listar asignaturas |
| GET/POST | `/asignaturas/crear` | Crear asignatura |
| GET/POST | `/asignaturas/editar/<id>` | Editar asignatura |
| POST | `/asignaturas/eliminar/<id>` | Eliminar asignatura |
| GET | `/notas/` | Listar notas |
| GET/POST | `/notas/crear` | Crear nota |
| GET/POST | `/notas/editar/<id>` | Editar nota |
| POST | `/notas/eliminar/<id>` | Eliminar nota |

## ⚙️ Instalación

1. **Clonar el repositorio**

       git clone [github.com](https://github.com/tu-usuario/sistema-notas.git)
       cd sistema-notas

2. **Crear el entorno virtual e instalar dependencias**

       python -m venv venv
       venv\Scripts\activate        # Windows
       source venv/bin/activate     # Linux / macOS
       pip install -r requirements.txt

3. **Levantar MySQL con XAMPP**

   Abre el **Panel de Control de XAMPP** y arranca **Apache** y **MySQL**.

4. **Crear la base de datos**

   - Abre `[localhost](http://localhost/phpmyadmin)`
   - Pestaña **SQL** → pega el contenido de `base_datos.sql` → **Continuar**

   O desde la terminal:

       mysql -u root -p < base_datos.sql

5. **Configurar la conexión**

   En `db.py` ajusta `DB_CONFIG` si tu MySQL usa otra contraseña:

       "user": "root",
       "password": "",

6. **Ejecutar la aplicación**

       python app.py

   Abre `[127.0.0.1](http://127.0.0.1:5000)`

## 🗄️ Base de datos

- `estudiantes` — cédula y correo únicos.
- `docentes` — cédula y correo únicos.
- `asignaturas` — FK a `docentes`, único `(nombre, id_docente)`.
- `notas` — FKs a `estudiantes` y `asignaturas`, único `(id_estudiante, id_asignatura)`,
  `promedio` como columna `GENERATED ALWAYS AS (...) STORED`,
  y `CHECK` de 0 a 10 en las tres notas.

## ✨ Características

- Interfaz con logo, nombre de usuario y menú con emojis.
- Mensajes flash de éxito / error / advertencia.
- Confirmación antes de eliminar.
- Promedio calculado por MySQL (nunca se escribe desde Flask).
- Pool de conexiones con DBUtils.

## 👤 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
