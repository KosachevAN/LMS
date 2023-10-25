import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    #поиск записи
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.c.execute('''SELECT * FROM db WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.c.fetchall()]

    def open_search_dialog(self):
        Search()

    def delete_record(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM db WHERE ID=?''',
            (self.tree.set(selection_item, '#1'),))
            self.db.conn.commit()
            self.view_records()

    #обновление данных
    def update_record(self, name, tel, email, salary):
        self.db.c.execute('''UPDATE db SET name=?, tel=?, email=?, salary=? WHERE ID=?''',
            (name, tel, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    def view_records(self):
        #выбор из БД
        self.db.c.execute('''SELECT * FROM db''')
        #удаляем из виджета
        [self.tree.delete(i) for i in self.tree.get_children()]
        #добавляем в виджет данные БД
        [self.tree.insert('', 'end', value=row) for row in self.db.c.fetchall()]

    def records(self, name, tel, email, salary):
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    def open_dialog(self):
        Child()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        #вывод таблицы
        #ttk.Style().configure("Treeview", background="blue", foreground="black", fieldbackground="red")
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email', 'salary'), height=45, show='headings')
        #колонки
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)

        #заголовки
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        #упаковка
        self.tree.pack(side=tk.LEFT)

        #создание кнопки изменения записи
        self.update_img = tk.PhotoImage(file='./img/red.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        #создание кнопки удаления записи
        self.delete_img = tk.PhotoImage(file='./img/del.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        #создание кнопки поиска записи
        self.search_img = tk.PhotoImage(file='./img/fnd.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        #создание кнопки обновления записи
        self.refresh_img = tk.PhotoImage(file='./img/upd.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x300')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        #подписи
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_tel = tk.Label(self, text='Телефон')
        label_tel.place(x=50,y=80)
        label_email = tk.Label(self, text='E-mail')
        label_email.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=130)

        #ВВОД ПОЛЕЙ и их координат:
        #имя
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        #телефон
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)
        #емейл
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        #зарплата
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)


        #КНОПКИ:
        #закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)
        #добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        #срабатывание по ЛКМ
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(
            self.entry_name.get(),
            self.entry_tel.get(),
            self.entry_email.get(),
            self.entry_salary.get()
            ))
        
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(
            self.entry_name.get(),
            self.entry_tel.get(),
            self.entry_email.get(),
            self.entry_salary.get()
            ))
        #закрывам окно редактирования
        #add='+' позволяет вешать на 1 кнопку более 1 события
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''', (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)
        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        # Соединение с базой данных
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS db
            (id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            tel TEXT NOT NULL,  
            email TEXT,         
            salary TEXT         
            );''')
        self.conn.commit()

    def insert_data(self, name, tel, email, salary):
        self.c.execute("""INSERT INTO db(name, tel, email, salary)
                    VALUES (?, ?, ?, ?) """, (name, tel, email, salary))
        self.conn.commit()


if __name__=='__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('800x600')
    root.resizable(False, False)
    root.mainloop()