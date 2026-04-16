import customtkinter as ctk
from datetime import datetime
from task_manager import load_tasks, add_task, toggle_task, delete_task, filter_tasks, edit_task, clear_completed, search_tasks, sort_tasks, check_due_notifications

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MisTareas")
        self.geometry("720x680")
        self.minsize(600, 500)
        self.resizable(True, True)

        self.tasks = load_tasks()
        self.filter_mode = "Todas"
        check_due_notifications(self.tasks)

        self._build_ui()
        self.bind("<Configure>", self._on_resize)
        self.refresh_list()

    def _on_resize(self, event):
        if event.widget is self:
            max_w = 960
            pad = max(20, (self.winfo_width() - max_w) // 2)
            self.content.configure(padx=pad)

    def _build_ui(self):
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=20)

        # ── Cabecera ─────────────────────────────────────────────
        top_bar = ctk.CTkFrame(self.content, fg_color="transparent")
        top_bar.pack(pady=(20, 12), fill="x")

        left_header = ctk.CTkFrame(top_bar, fg_color="transparent")
        left_header.pack(side="left")

        title_row = ctk.CTkFrame(left_header, fg_color="transparent")
        title_row.pack(anchor="w")
        ctk.CTkLabel(title_row, text="📝", font=ctk.CTkFont(size=26)).pack(side="left")
        ctk.CTkLabel(title_row, text="MisTareas", font=ctk.CTkFont(size=26, weight="bold")).pack(side="left", padx=(4, 0))

        self.pending_label = ctk.CTkLabel(
            left_header, text="0 tareas pendientes",
            font=ctk.CTkFont(size=13), text_color="#4A9EFF"
        )
        self.pending_label.pack(anchor="w")

        right_header = ctk.CTkFrame(top_bar, fg_color="transparent")
        right_header.pack(side="right")

        ctk.CTkButton(
            right_header, text="📊  Estadísticas",
            width=130, height=36,
            fg_color="transparent",
            border_width=1, border_color=("#555555", "#aaaaaa"),
            text_color=("#111111", "#f0f0f0"),
            command=self.show_stats
        ).pack(side="left", padx=(0, 8))

        self.theme_mode = "light"
        self.theme_btn = ctk.CTkButton(
            right_header, text="🌙", width=36, height=36,
            fg_color="transparent",
            border_width=1, border_color=("#555555", "#aaaaaa"),
            text_color=("#111111", "#f0f0f0"),
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="left")

        # ── Tarjeta de entrada ────────────────────────────────────
        input_card = ctk.CTkFrame(self.content, corner_radius=12)
        input_card.pack(pady=(0, 12), fill="x")

        row1 = ctk.CTkFrame(input_card, fg_color="transparent")
        row1.pack(padx=16, pady=(14, 6), fill="x")

        self.entry = ctk.CTkEntry(
            row1, placeholder_text="Escribe una nueva tarea...",
            height=42, border_width=0, fg_color="transparent"
        )
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda e: self.add_task())

        ctk.CTkButton(row1, text="+ Añadir", width=110, height=42, command=self.add_task).pack(side="right")

        row2 = ctk.CTkFrame(input_card, fg_color="transparent")
        row2.pack(padx=16, pady=(0, 14), fill="x")

        self.priority_var = ctk.StringVar(value="Media")
        ctk.CTkOptionMenu(
            row2,
            values=["Alta", "Media", "Baja"],
            variable=self.priority_var,
            width=130, height=36
        ).pack(side="left", padx=(0, 10))

        self.date_entry = ctk.CTkEntry(row2, placeholder_text="DD/MM/AAAA", width=140, height=36)
        self.date_entry.pack(side="left")

        # ── Filtros + Ordenación ──────────────────────────────────
        filter_row = ctk.CTkFrame(self.content, fg_color="transparent")
        filter_row.pack(pady=(0, 8), fill="x")

        self.filter_var = ctk.StringVar(value="Todas")
        ctk.CTkSegmentedButton(
            filter_row,
            values=["Todas", "Pendientes", "Completadas"],
            variable=self.filter_var,
            command=lambda _: self.refresh_list()
        ).pack(side="left", fill="x", expand=True)

        self.sort_var = ctk.StringVar(value="Por defecto")
        ctk.CTkOptionMenu(
            filter_row,
            values=["Por defecto", "Prioridad", "Nombre", "Fecha"],
            variable=self.sort_var,
            command=lambda _: self.refresh_list(),
            width=130
        ).pack(side="right")

        # ── Buscador + Limpiar completadas ────────────────────────
        search_row = ctk.CTkFrame(self.content, fg_color="transparent")
        search_row.pack(pady=(0, 12), fill="x")

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.refresh_list())
        ctk.CTkEntry(
            search_row, textvariable=self.search_var,
            placeholder_text="🔍 Buscar tareas...", height=36
        ).pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            search_row, text="🗑  Limpiar completadas",
            fg_color="transparent", border_width=1,
            border_color=("#555555", "#aaaaaa"),
            text_color=("#111111", "#f0f0f0"),
            hover_color="#550000", height=36,
            command=self.clear_completed
        ).pack(side="right")

        # ── Lista de tareas ───────────────────────────────────────
        self.list_frame = ctk.CTkScrollableFrame(self.content, corner_radius=12, label_text="")
        self.list_frame.pack(pady=(0, 20), fill="both", expand=True)

    def add_task(self):
        title = self.entry.get().strip()
        if not title:
            return
        
        priority = self.priority_var.get()
        due_date = self.date_entry.get().strip()
        self.tasks = add_task(self.tasks, title, priority, due_date)
        self.entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.refresh_list()

    def refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        mode = self.filter_var.get()
        query = self.search_var.get().strip()
        visible = filter_tasks(self.tasks, mode)
        if query:
            visible = search_tasks(visible, query)
        visible = sort_tasks(visible, self.sort_var.get())

        if not visible:
            ctk.CTkLabel(self.list_frame, text="No hay tareas. ¡Añade una nueva!",
                         text_color="gray").pack(pady=20)
            pending = len([t for t in self.tasks if not t["done"]])
            self.pending_label.configure(
                text=f"{pending} tarea{'s' if pending != 1 else ''} pendiente{'s' if pending != 1 else ''}"
            )
            return
        
        for task in visible:
            real_index = self.tasks.index(task)
            self._build_task_row(task, real_index)

        pending = len([t for t in self.tasks if not t["done"]])
        self.pending_label.configure(
            text=f"{pending} tarea{'s' if pending != 1 else ''} pendiente{'s' if pending != 1 else ''}"
        )

    def _build_task_row(self, task, index):
        row = ctk.CTkFrame(self.list_frame)
        row.pack(fill="x", pady=4, padx = 4)

        # Color según prioridad
        priority = task.get("priority", "Media")
        colors = {"Alta": "#FF4444", "Media": "#FFA500", "Baja": "#44AA44"}
        color = colors.get(priority, "#888888")

        ctk.CTkLabel(row, text="●", text_color=color, width=16).pack(side="left", padx=(8,0))

        check_var = ctk.BooleanVar(value=task["done"])
        text_color = ("gray", "gray") if task["done"] else ("#1a1a1a", "#f0f0f0")
        font_style = ctk.CTkFont(size=14, overstrike=task["done"])

        ctk.CTkCheckBox(
            row, text = task["title"], 
            variable=check_var,
            font=font_style,
            text_color=text_color,
            command=lambda i=index: self.toggle(i)
        ).pack(side="left", fill="x", expand=True, pady=10, padx=12)

        due = task.get("due_date", "")
        if due:
            try:
                due_dt = datetime.strptime(due, "%d/%m/%Y")
                vencida = due_dt < datetime.now() and not task["done"]
                date_color = "#FF4444" if vencida else "gray"
                label = f"⚠ {due}" if vencida else f"📅 {due}"
            except:
                date_color = "gray"
                label = due
            ctk.CTkLabel(row, text=label, text_color=date_color,
                         font=ctk.CTkFont(size=11)).pack(side="right", padx=(0, 8))

        ctk.CTkButton(
            row, text="✏", width=36, height=28,
            fg_color="transparent", hover_color="#003366",
            command=lambda i=index: self.edit_task(i)
        ).pack(side="right", padx=(0, 4))

        ctk.CTkButton(
            row, text="🗑", width=36, height=28,
            fg_color="transparent", hover_color="#550000",
            command=lambda i=index: self.delete(i)
        ).pack(side="right", padx=8)

    def toggle(self, index):
        self.tasks = toggle_task(self.tasks, index)
        self.refresh_list()

    def delete(self, index):
        self.tasks = delete_task(self.tasks, index)
        self.refresh_list()

    def edit_task(self, index):
        dialog = ctk.CTkInputDialog(text="Nuevo nombre:", title="Editar tarea")
        new_title = dialog.get_input()
        if new_title and new_title.strip():
            self.tasks = edit_task(self.tasks, index, new_title.strip())
            self.refresh_list()

    def clear_completed(self):
        self.tasks = clear_completed(self.tasks)
        self.refresh_list()

    def toggle_theme(self):
        if self.theme_mode == "light":
            ctk.set_appearance_mode("dark")
            self.theme_mode = "dark"
            self.theme_btn.configure(text="☀")
        else:
            ctk.set_appearance_mode("light")
            self.theme_mode = "light"
            self.theme_btn.configure(text="🌙")

    def show_stats(self):
        from task_manager import get_stats
        stats = get_stats(self.tasks)
        win = ctk.CTkToplevel(self)
        win.title("Estadísticas")
        win.geometry("300x220")
        win.grab_set()

        ctk.CTkLabel(win, text="📊 Resumen", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=16)
        ctk.CTkLabel(win, text=f"Total de tareas: {stats['total']}").pack()
        ctk.CTkLabel(win, text=f"Completadas: {stats['done']}").pack()
        ctk.CTkLabel(win, text=f"Pendientes: {stats['pending']}").pack()
        ctk.CTkLabel(win, text=f"Alta prioridad: {stats['by_priority']['Alta']}").pack()
        ctk.CTkLabel(win, text=f"Media prioridad: {stats['by_priority']['Media']}").pack()
        ctk.CTkLabel(win, text=f"Baja prioridad: {stats['by_priority']['Baja']}").pack()