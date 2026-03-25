from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks VALUES (?)', (task_string,))
        the_connection.commit()   # ✅ commit immediately
        list_update()
        task_field.delete(0, 'end')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (the_value,))
            the_connection.commit()   # ✅ commit immediately
    except:
        messagebox.showinfo('Error', 'No task selected. Cannot Delete.')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        tasks.clear()
        list_update()
        the_cursor.execute('DELETE FROM tasks')
        the_connection.commit()   # ✅ commit immediately

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    messagebox.showinfo("Exit", "Application closed. Goodbye!")
    guiWindow.destroy()

def retrieve_database():
    tasks.clear()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("665x400+550+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#B5E5CF")

    # Database setup
    the_connection = sql.connect('listOftasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    tasks = []

    # Frame
    functions_frame = Frame(guiWindow, bg="#8EE5EE")
    functions_frame.pack(side="top", expand=True, fill="both")

    # Label
    tasks_label = Label(
        functions_frame,
        text="TO-DO LIST\nEnter the task Title:",
        font=("Arial", "14", "bold"),
        background="#8EE5EE",
        foreground="#FF6103"
    )
    tasks_label.place(x=20, y=30)

    # Entry field
    task_field = Entry(
        functions_frame,
        font=("Arial", "14"),
        width=42,
        foreground="black",
        background="white",
    )
    task_field.place(x=180, y=30)

    # Buttons
    add_button = Button(
        functions_frame,
        text="Add",
        width=15,
        bg="#D4AC0D",
        font=("Arial", "14", "bold"),
        command=add_task,
    )
    del_button = Button(
        functions_frame,
        text="Delete",
        width=15,
        bg="#D4AC0D",
        font=("Arial", "14", "bold"),
        command=delete_task,
    )
    del_all_button = Button(
        functions_frame,
        text="Delete All",
        width=15,
        bg="#D4AC0D",
        font=("Arial", "14", "bold"),
        command=delete_all_tasks,
    )
    exit_button = Button(
        functions_frame,
        text="Exit / Close",
        width=52,
        bg="#D4AC0D",
        font=("Arial", "14", "bold"),
        command=close,
    )

    add_button.place(x=18, y=80)
    del_button.place(x=240, y=80)
    del_all_button.place(x=460, y=80)
    exit_button.place(x=17, y=330)

    # Listbox
    task_listbox = Listbox(
        functions_frame,
        width=70,
        height=9,
        font=("Arial", 12),
        selectmode="SINGLE",
        background="white",
        foreground="black",
        selectbackground="#FF8C00",
        selectforeground="black"
    )
    task_listbox.place(x=17, y=140)

    # Load tasks from DB
    retrieve_database()
    list_update()

    guiWindow.mainloop()

    # Final commit and close DB
    the_connection.commit()
    the_cursor.close()
    the_connection.close()
