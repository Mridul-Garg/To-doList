import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

def add():
    t_string= tfield.get()
    if len(t_string)==0:
        messagebox.showerror("Error","Entry is Empty: Please enter a task into the entry field")
    else:
        task.append(t_string)
        cursor.execute('insert into task values (?)', (t_string,))
        list_update()
        tfield.delete(0,'end')  

def list_update():
    clear_list()
    for i in task:
        t_listbox.insert('end',i)

def delete():
    try:
        val=t_listbox.get(t_listbox.curselection())
        if val in task:
            task.remove(val)
        list_update()
        cursor.execute('delete from task where title =?',(val,))
    except:
        messagebox.showerror("Error","No task selected: Please select a task to delete")

def deleteall():
    message=messagebox.askyesno("Delete All","Are you sure you want to delete all tasks?")
    if message==True:
        while len(task)!=0:
            task.pop()
        cursor.execute('delete from task')
        list_update()

def clear_list():
    t_listbox.delete(0,'end')

def close():
    print(task)
    guiWindow.destroy()

def database():
    while len(task)!=0:
        task.pop()
    for row in cursor.execute('select title from task'):
        task.append(row[0])

if __name__=="__main__":
    guiWindow=tk.Tk()
    guiWindow.title("To-Do list - Mridul Garg")
    guiWindow.geometry("500x500+500+250")
    guiWindow.resizable(0,0)
    guiWindow.config(bg="#BCD2EE")

    connect=sql.connect('listtasks.db')
    cursor=connect.cursor()
    cursor.execute('create table if not exists task (title text)')
    task=[]
    header=tk.Frame(guiWindow,bg="#CAE1FF")
    function=tk.Frame(guiWindow,bg="#CAE1FF")
    listbox=tk.Frame(guiWindow,bg="#CAE1FF")
    header.pack(fill="both")
    function.pack(side="left",expand=True,fill="both")
    listbox.pack(side="right",expand=True,fill="both")

    headerlabel=ttk.Label(
        header,
        text="To-Do List",
        font=("Times New Roman","30"),
        background="#CAE1FF",
        foreground="#8B1C62"
    )
    headerlabel.pack(padx=40,pady=40)
    tasklabel=ttk.Label(
        function,
        text="Enter Task:",
        font=("Segoe UI","12","bold"),
        background="#CAE1FF",
        foreground="#000000"
    )
    tasklabel.place(x=30,y=40)

    tfield=ttk.Entry(
        function,
        font=("Segoe UI","12"),
        width=18,
        background="#BCD2EE",
        foreground="#EE3B3B"
    )
    tfield.place(x=30,y=80)

    addbutton=ttk.Button(
        function,
        text="Add Task",
        width=24,
        command=add
    )
    delbutton=ttk.Button(
        function,
        text="Delete Task",
        width=24,
        command=delete
    )
    deleteallbutton=ttk.Button(
        function,
        text="Delete All Tasks",
        width=24,
        command=deleteall
    )
    exitbutton=ttk.Button(
        function,
        text="Exit",
        width=24,
        command=close
    )
    addbutton.place(x = 30, y = 120)  
    delbutton.place(x = 30, y = 160)  
    deleteallbutton.place(x = 30, y = 200)  
    exitbutton.place(x = 30, y = 240)

    t_listbox=tk.Listbox(
        listbox,
        width=26,
        height=13,
        selectmode='SINGLE',
        background = "#FFFFFF",  
        foreground = "#000000",
        selectbackground="#36648B",
        selectforeground="#F5F5F5"
    )
    t_listbox.place(x=10,y=20)

    database()
    list_update()
    guiWindow.mainloop()
    connect.commit()
    cursor.close()  
