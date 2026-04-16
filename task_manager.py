import json
import os
from datetime import datetime
from plyer import notification

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    
def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(tasks, title, priority = "Media", due_date = ""):
    task = {"title": title, "done": False, "priority": priority, "due_date": due_date}
    tasks.append(task)
    save_tasks(tasks)
    return tasks

def toggle_task(tasks, index):
    tasks[index]["done"] = not tasks[index]["done"]
    save_tasks(tasks)
    return tasks

def delete_task(tasks, index):
    tasks.pop(index)
    save_tasks(tasks)
    return tasks

def filter_tasks (tasks, mode):
    if mode == "Pendientes":
        return [t for t in tasks if not t["done"]]
    elif mode == "Completadas":
        return [t for t in tasks if t["done"]]
    else:
        return tasks

def edit_task(tasks, index, new_title, new_priority=None, new_due_date=None):
    tasks[index]["title"] = new_title
    if new_priority is not None:
        tasks[index]["priority"] = new_priority
    if new_due_date is not None:
        tasks[index]["due_date"] = new_due_date
    save_tasks(tasks)
    return tasks

def clear_completed(tasks):
    tasks = [t for t in tasks if not t["done"]]
    save_tasks(tasks)
    return tasks

def search_tasks(tasks, query):
    q = query.lower()
    return [t for t in tasks if q in t["title"].lower()]

PRIORITY_ORDER = {"Alta": 0, "Media": 1, "Baja": 2}

def sort_tasks(tasks, mode):
    if mode == "Prioridad":
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.get("priority", "Media"), 1))
    elif mode == "Nombre":
        return sorted(tasks, key=lambda t: t["title"].lower())
    elif mode == "Fecha":
        def date_key(t):
            try:
                return datetime.strptime(t.get("due_date", ""), "%d/%m/%Y")
            except:
                return datetime.max
        return sorted(tasks, key=date_key)
    return tasks

def get_stats(tasks):
    total = len(tasks)
    done = len([t for t in tasks if t["done"]])
    pending = total - done
    by_priority = {"Alta": 0, "Media": 0, "Baja": 0}
    for t in tasks:
        p = t.get("priority", "Media")
        if p in by_priority:
            by_priority[p] += 1
    return {"total": total, "done": done, "pending": pending, "by_priority": by_priority}

def check_due_notifications(tasks):
    today = datetime.now().date()
    for task in tasks:
        if task.get("done"):
            continue
        due = task.get("due_date", "")
        if not due:
            continue
        try:
            due_date = datetime.strptime(due, "%d/%m/%Y").date()
            days_left = (due_date - today).days
            if days_left == 0:
                notification.notify(
                    title="⚠ Tarea para hoy",
                    message=task["title"],
                    timeout=5
                )
            elif days_left < 0:
                notification.notify(
                    title="❌ Tarea vencida",
                    message=f"{task['title']} (venció el {due})",
                    timeout=5
                )
        except:
            continue