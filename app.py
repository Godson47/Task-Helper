#Task_Helper for daily task,User can Add,delete or Modify task
#Basic Functionality with working UI
#using python
#Full Basic working code
#Push to Github


import tkinter as tk
from tkinter import ttk, messagebox
import database

class TaskHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Tracker")
        self.root.geometry("950x650")
        self.root.minsize(800, 550)
        self.selected_task_id = None

        database.initialize_database()

        self.title_var = tk.StringVar()
        self.due_date_var = tk.StringVar()

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Title.TLabel", font=("Arial", 24, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 11))
        style.configure("Treeview", rowheight=35, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Add.TButton", font=("Arial", 10, "bold"), padding=8)

        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Task Tracker", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            main_frame,
            text="Manage your daily tasks easily",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(0, 20))

        form_frame = ttk.LabelFrame(main_frame, text="Task Details", padding=15)
        form_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(form_frame, text="Task Title:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.title_entry = ttk.Entry(
            form_frame, textvariable=self.title_var, width=50
        )
        self.title_entry.grid(
            row=0, column=1, sticky="ew", padx=5, pady=5
        )

        ttk.Label(form_frame, text="Due Date:").grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.due_date_entry = ttk.Entry(
            form_frame, textvariable=self.due_date_var, width=20
        )
        self.due_date_entry.grid(
            row=0, column=3, sticky="ew", padx=5, pady=5
        )

        ttk.Label(form_frame, text="Description:").grid(
            row=1, column=0, sticky="nw", padx=5, pady=5
        )
        self.description_text = tk.Text(
            form_frame, height=4, width=60, font=("Arial", 10)
        )
        self.description_text.grid(
            row=1, column=1, columnspan=3, sticky="ew", padx=5, pady=5
        )
        form_frame.columnconfigure(1, weight=1)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 15))

        ttk.Button(
            button_frame, text="Add Task",
            command=self.add_task, style="Add.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Update Task",
            command=self.update_task
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Delete Task",
            command=self.delete_task
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Mark as completed or pending",
            command=self.toggle_status
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame, text="Clear",
            command=self.clear_form
        ).pack(side="right", padx=5)

        list_frame = ttk.LabelFrame(main_frame, text="My Tasks", padding=10)
        list_frame.pack(fill="both", expand=True)

        columns = ("id", "title", "description", "due_date", "status")
        self.task_tree = ttk.Treeview(
            list_frame, columns=columns, show="headings"
        )

        headings = {
            "id": "ID",
            "title": "Task",
            "description": "Description",
            "due_date": "Due Date",
            "status": "Status"
        }

        for column, heading in headings.items():
            self.task_tree.heading(column, text=heading)

        self.task_tree.column("id", width=50, anchor="center")
        self.task_tree.column("title", width=200)
        self.task_tree.column("description", width=350)
        self.task_tree.column("due_date", width=120, anchor="center")
        self.task_tree.column("status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.task_tree.yview
        )
        self.task_tree.configure(yscrollcommand=scrollbar.set)

        self.task_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.task_tree.bind("<<TreeviewSelect>>", self.select_task)

        self.status_label = ttk.Label(
            main_frame, text="Ready", relief="sunken", anchor="w"
        )
        self.status_label.pack(fill="x", pady=(10, 0))

        self.load_tasks()

    def add_task(self):
        title = self.title_var.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        due_date = self.due_date_var.get().strip()

        if not title:
            messagebox.showwarning("Missing Information", "No task title")
            return

        database.add_task(title, description, due_date)
        messagebox.showinfo("Success", "Task added successfully!")
        self.clear_form()
        self.load_tasks()

    def update_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning(
                "No Task Selected", "Please select a task to be updated."
            )
            return

        title = self.title_var.get().strip()
        description = self.description_text.get("1.0", tk.END).strip()
        due_date = self.due_date_var.get().strip()

        if not title:
            messagebox.showwarning(
                "Missing Information", "Task title cannot be empty."
            )
            return

        database.update_task(
            self.selected_task_id, title, description, due_date
        )
        messagebox.showinfo("Success", "Task updated successfully!")
        self.clear_form()
        self.load_tasks()

    def delete_task(self):
        if self.selected_task_id is None:
            messagebox.showwarning(
                "No Task Selected", "Please select a task to delete."
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete", "Are you sure you want to delete this task?"
        ):
            return

        database.delete_task(self.selected_task_id)
        messagebox.showinfo("Deleted", "Task deleted successfully!")
        self.clear_form()
        self.load_tasks()

    def toggle_status(self):
        if self.selected_task_id is None:
            messagebox.showwarning(
                "No Task Selected", "Please select a task first."
            )
            return

        database.toggle_task_status(self.selected_task_id)
        self.load_tasks()
        self.status_label.config(text="Task status updated.")

    def load_tasks(self):
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)

        tasks = database.get_tasks()

        for task in tasks:
            self.task_tree.insert("", tk.END, values=task)

        self.status_label.config(text=f"{len(tasks)} task(s)")

    def select_task(self, event=None):
        selected = self.task_tree.selection()
        if not selected:
            return

        values = self.task_tree.item(selected[0])["values"]
        if not values:
            return

        self.selected_task_id = values[0]
        self.title_var.set(values[1])
        self.due_date_var.set(values[3])

        self.description_text.delete("1.0", tk.END)
        self.description_text.insert("1.0", values[2])

        self.status_label.config(
            text=f"Selected task #{self.selected_task_id}"
        )

    def clear_form(self):
        self.selected_task_id = None
        self.title_var.set("")
        self.due_date_var.set("")
        self.description_text.delete("1.0", tk.END)

        for item in self.task_tree.selection():
            self.task_tree.selection_remove(item)

        self.status_label.config(text="Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskHelper(root)
    root.mainloop()
