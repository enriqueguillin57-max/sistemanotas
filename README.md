# 🎓 Sistema de Notas

Aplicación web CRUD para gestión académica de **estudiantes, docentes, asignaturas y notas**, construida con **Python + Flask** y **MySQL (XAMPP)**.

---

## 📌 Descripción

El sistema administra por completo las entidades de una institución educativa: registrar, listar, editar y eliminar estudiantes y docentes; crear asignaturas vinculadas a un docente; y asignar notas por estudiante y asignatura. El promedio de cada nota lo calcula MySQL automáticamente mediante una columna generada.

---

## ✨ Características

- CRUD completo en los 4 módulos: **estudiantes, docentes, asignaturas y notas**.
- Interfaz con barra superior (logo + usuario), menú de navegación con emojis y mensajes flash.
- Promedio calculado por la base de datos: `ROUND((nota1 + nota2 + examen) / 3, 2)`.
- Validación de notas en rango **0 a 10** en tres niveles: formulario HTML, Python y `CHECK` en MySQL.
- Consultas parametrizadas (prevención de inyección SQL).
- Integridad referencial con claves foráneas `ON DELETE CASCADE` / `RESTRICT`.
- Restricción `UNIQUE`: un estudiante no puede tener dos notas en la misma asignatura.

---

## 🛠️ Tecnologías

| Componente | Versión |
|---|---|
| Python | 3.10+ |
| Flask | 3.0.3 |
| MySQL | 8.0.16+ (XAMPP) |
| mysql-connector-python | 9.1.0 |
| Frontend | HTML5 + CSS3 (Jinja2) |

> ⚠️ Se requiere **MySQL 8.0.16 o superior**: versiones anteriores ignoran los `CHECK` y no aplican correctamente las columnas generadas `STORED`.

---

## 📂 Estructura del proyecto

```
sistema_notas/
├── app.py                  # Punto de entrada y registro de blueprints
├── db.py                   # Conexión y ejecución de consultas
├── requirements.txt        # Dependencias
├── sistema_notas.sql       # Script de base de datos
├── README.md
│
├── routes/
│   ├── __init__.py
│   ├── estudiantes.py
│   ├── docentes.py
│   ├── asignaturas.py
│   └── notas.py
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── base.html
    ├── estudiantes/   (index, lista, formulario, crear, editar)
    ├── docentes/      (index, lista, formulario, crear, editar)
    ├── asignaturas/   (index, crear, editar)
    └── notas/         (index, crear, editar)
```

---

## ⚙️ Instalación y ejecución

### 1. Requisitos previos

- **XAMPP** con Apache y MySQL.
- **Python 3.10 o superior**.

### 2. Crear la base de datos

1. Abre el **Panel de Control de XAMPP** y arranca **Apache** y **MySQL**.
2. Entra a phpMyAdmin: `[localhost](http://localhost/phpmyadmin)`
3. Pestaña **SQL** → pega `sistema_notas.sql` → **Ejecutar**.

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

### 5. Abrir en el navegador

```
[127.0.0.1](http://127.0.0.1:5000)
```

---

## 🔌 Configuración de conexión

En `db.py` (valores por defecto de XAMPP):

```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",          # vacío por defecto en XAMPP
    "database": "sistema_notas",
    "charset": "utf8mb4",
    "use_pure": True,
}
```

Si tu MySQL tiene contraseña, cámbiala en `password`.

---

## 🧭 Rutas disponibles

| Módulo | Ruta | Acción |
|---|---|---|
| Inicio | `/` | Página de bienvenida |
| **Estudiantes** 🧑‍🎓 | `/estudiantes/` · `/estudiantes/lista` · `/estudiantes/formulario` | Listar |
| | `/estudiantes/crear` | Crear |
| | `/estudiantes/editar/<id>` | Editar |
| | `/estudiantes/eliminar/<id>` | Eliminar |
| **Docentes** 👨‍🏫 | `/docentes/` · `/docentes/lista` · `/docentes/formulario` | Listar |
| | `/docentes/crear` | Crear |
| | `/docentes/editar/<id>` | Editar |
| | `/docentes/eliminar/<id>` | Eliminar |
| **Asignaturas** 📚 | `/asignaturas/` | Listar |
| | `/asignaturas/crear` | Crear |
| | `/asignaturas/editar/<id>` | Editar |
| | `/asignaturas/eliminar/<id>` | Eliminar |
| **Notas** 📝 | `/notas/` | Listar |
| | `/notas/crear` | Crear |
| | `/notas/editar/<id>` | Editar |
| | `/notas/eliminar/<id>` | Eliminar |

---

## 🗄️ Modelo de datos

### `estudiantes`

| Campo | Tipo | Restricción |
|---|---|---|
| id_estudiante | INT | PK, autoincremental |
| cedula | VARCHAR(20) | UNIQUE, obligatorio |
| nombre / apellido | VARCHAR(100) | obligatorios |
| correo | VARCHAR(120) | UNIQUE, obligatorio |
| fecha_nacimiento | DATE | opcional |
| estado | ENUM | `Activo` / `Inactivo` |
| fecha_registro | TIMESTAMP | automático |

### `docentes`

| Campo | Tipo | Restricción |
|---|---|---|
| id_docente | INT | PK, autoincremental |
| cedula | VARCHAR(20) | UNIQUE, obligatorio |
| nombre / apellido | VARCHAR(100) | obligatorios |
| correo | VARCHAR(120) | UNIQUE, obligatorio |
| especialidad | VARCHAR(100) | opcional |
| estado | ENUM | `Activo` / `Inactivo` |

### `asignaturas`

| Campo | Tipo | Restricción |
|---|---|---|
| id_asignatura | INT | PK, autoincremental |
| nombre | VARCHAR(100) | obligatorio |
| descripcion | VARCHAR(255) | opcional |
| nivel | VARCHAR(50) | opcional |
| id_docente | INT | FK → `docentes` (`ON DELETE RESTRICT`) |

### `notas`

| Campo | Tipo | Restricción |
|---|---|---|
| id_nota | INT | PK, autoincremental |
| id_estudiante | INT | FK → `estudiantes` (`ON DELETE CASCADE`) |
| id_asignatura | INT | FK → `asignaturas` (`ON DELETE CASCADE`) |
| nota1 / nota2 / examen | DECIMAL(4,2) | `CHECK` entre 0 y 10 |
| **promedio** | DECIMAL(4,2) | **columna generada** (no se escribe) |
| observacion | VARCHAR(255) | opcional |
| fecha_actualizacion | TIMESTAMP | se actualiza sola al editar |

**Regla clave:** el campo `promedio` lo calcula MySQL automáticamente. **Nunca** lo incluyas en un `INSERT` o `UPDATE`; si lo haces, la consulta falla.

---

## 🧩 Notas de uso

- **Borrar un docente** con asignaturas asignadas falla (`ON DELETE RESTRICT`). Primero reasigna o elimina sus asignaturas.
- **Borrar un estudiante o asignatura** elimina en cascada sus notas asociadas.
- Un estudiante **no puede repetir nota** en la misma asignatura (restricción `UNIQUE`).
- Al editar una nota solo cambian las calificaciones y la observación; el estudiante y la asignatura quedan fijos.

---

## 🧪 Solución de problemas

| Problema | Causa | Solución |
|---|---|---|
| `Error al conectar a MySQL` | MySQL apagado o credenciales incorrectas | Enciende MySQL en XAMPP y revisa `DB_CONFIG` |
| `Unknown database 'sistema_notas'` | La base no existe | Ejecuta `sistema_notas.sql` en phpMyAdmin |
| `Check constraint 'chk_nota1' is violated` | Nota fuera de 0–10 | Ingresa valores válidos (el formulario ya los limita) |
| No se puede eliminar un docente | Tiene asignaturas asociadas | Reasigna o elimina sus asignaturas primero |
| `Cannot insert into generated column 'promedio'` | Se escribió el promedio en el SQL | No incluyas `promedio` en el `INSERT`/`UPDATE` |

---

## 👤 Autor

Proyecto académico — **Sistema de Notas**  
Desarrollado con Python, Flask y MySQL (XAMPP).

---

## 📄 Licencia

Uso libre con fines educativos.