# 📝 MisTareas — To-Do List

Aplicación de escritorio para gestión de tareas personales, construida con Python y CustomTkinter.

---

## Características

### Gestión de tareas
- **Añadir tareas** escribiendo un título y pulsando *Añadir* o `Enter`.
- **Marcar como completada** mediante el checkbox de cada tarea.
- **Editar** el título de una tarea con el botón ✏.
- **Eliminar** tareas individuales con el botón 🗑.
- **Limpiar completadas** elimina de un golpe todas las tareas marcadas.

### Prioridad y fecha de vencimiento
- Cada tarea puede tener prioridad **Alta**, **Media** o **Baja**, indicada con un punto de color (rojo / naranja / verde).
- Se puede asignar una **fecha límite** en formato `DD/MM/AAAA`.
  - Las tareas vencidas y pendientes se marcan con ⚠ en rojo.
  - Las tareas con fecha futura muestran 📅 en gris.

### Filtros y búsqueda
- Filtra la lista por **Todas**, **Pendientes** o **Completadas**.
- Ordena las tareas por **Prioridad**, **Nombre**, **Fecha** o en el orden de creación (*Por defecto*).
- Campo de búsqueda en tiempo real para localizar tareas por título.

### Estadísticas
- Botón **📊 Estadísticas** que abre un resumen con:
  - Total de tareas, completadas y pendientes.
  - Número de tareas por nivel de prioridad.

### Apariencia
- Botón para alternar entre **modo oscuro** y **modo claro**.
- El título de la ventana muestra en todo momento el número de tareas pendientes.

### Notificaciones de Windows
- Al iniciar la aplicación comprueba automáticamente las fechas límite y lanza notificaciones del sistema para:
  - Tareas que vencen **hoy**.
  - Tareas que ya han **vencido**.

### Persistencia
- Las tareas se guardan automáticamente en `tasks.json` en el mismo directorio, por lo que se conservan entre sesiones.

---

## Requisitos

- Python 3.10 o superior
- Dependencias (instalables con `pip`):

```bash
pip install customtkinter plyer
```

---

## Ejecución en desarrollo

```bash
python main.py
```

## Generar ejecutable (.exe)

```bash
pyinstaller --onefile --windowed --name "MisTareas" main.py
```

El ejecutable resultante se encontrará en la carpeta `dist\`. Cada vez que se modifique el código es necesario volver a compilarlo para que los cambios se reflejen en el `.exe`.

---

## Estructura del proyecto

```
PythonProject/
├── main.py            # Punto de entrada
├── app.py             # Interfaz gráfica (CustomTkinter)
├── task_manager.py    # Lógica de negocio y persistencia
├── tasks.json         # Datos de tareas (generado automáticamente)
└── README.md
```
