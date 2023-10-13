import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        # инициализируем главное окно приложения
        self.init_main()
        self.db = db
        self.viewData()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        self.add_img = self.add_img.subsample(5, 5)
        btn_add = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.openChildAdd)
        btn_add.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='./img/edit.png')
        self.update_img = self.update_img.subsample(5, 5)
        btn_update = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.openChildUpdate)
        btn_update.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        self.delete_img = self.delete_img.subsample(5, 5)
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.openChildDelete)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='./img/search.png')
        self.search_img = self.search_img.subsample(5, 5)
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.search_img, command=self.openChildSearch)
        btn_search.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'Name', 'Phone', 'Email', 'Salary'), height=45, show='headings')
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("Name", width=200, anchor=tk.CENTER)
        self.tree.column("Phone", width=150, anchor=tk.CENTER)
        self.tree.column("Email", width=150, anchor=tk.CENTER)
        self.tree.column("Salary", width=150, anchor=tk.CENTER)

        self.tree.heading("ID", text='ID')
        self.tree.heading("Name", text='ФИО')
        self.tree.heading("Phone", text='Телефон')
        self.tree.heading("Email", text='E-mail')
        self.tree.heading("Salary", text='Зарплата')

        self.tree.pack(side=tk.LEFT)

    def openChildAdd(self):
        Child()

    def openChildUpdate(self):
        try:
            entity = self.tree.set(self.tree.selection() [0])
            Child(entity)
        except:
            Warning('Выберите контакт')

    def openChildDelete(self):
        try:
            entity = self.tree.set(self.tree.selection() [0])
            self.deleteData(entity.get("ID"))
        except:
            Warning('Выберите контакт')

    def openChildSearch(self):
        Search()

    def addData(self, Name, Phone, Email, Salary):
        self.db.add(Name, Phone, Email, Salary)
        self.viewData()

    def updateData(self, ID, Name, Phone, Email, Salary):
        self.db.update(ID, Name, Phone, Email, Salary)
        self.viewData()

    def deleteData(self, ID):
        self.db.delete(ID)
        self.viewData()

    def searchData(self, Name):
        Name = ('%' + Name + '%')
        self.db.cursor.execute(
            '''SELECT * FROM contacts WHERE name LIKE ?''', [Name]
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', value=row) for row in self.db.cursor.fetchall()]

    def viewData(self):
        self.db.cursor.execute('SELECT * FROM contacts')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

class Child(tk.Toplevel):
    def __init__(self, entity = False):
        super().__init__(root)
        # делаем модальное окно
        self.transient(root)

        self.obEntity = entity
        if (hasattr(self.obEntity, 'get') and callable(getattr(self.obEntity, 'get'))):
            self.entityID = self.obEntity.get("ID")
        else:
            self.entityID = None

        self.view = app
        self.init_child()

    def init_child(self):

        if (self.entityID):
            self.title('Редактировать')
        else:
            self.title('Добавить')

        self.geometry('400x220')
        self.resizable(False,False)

        # активируем перехват событий в окне
        self.grab_set()
        # переводим фокус на окно
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=30)

        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=60)

        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=90)

        label_salary = tk.Label(self, text='Зарплата:')
        label_salary.place(x=50, y=120)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=30)
        if (self.entityID):
            self.entry_name.insert(0, self.obEntity.get("Name"))

        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=60)
        if (self.entityID):
            self.entry_phone.insert(0, self.obEntity.get("Phone"))

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=90)
        if (self.entityID):
            self.entry_email.insert(0, self.obEntity.get("Email"))

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=120)
        if (self.entityID):
            self.entry_salary.insert(0, self.obEntity.get("Salary"))

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        btn_ok_text = 'Добавить'
        if (self.entityID):
            btn_ok_text = 'Сохранить'

        self.btn_ok = ttk.Button(self, text=btn_ok_text)
        self.btn_ok.place(x=50, y=170)
        if (self.entityID):
            self.btn_ok.bind('<Button-1>', lambda event: self.eventUpdate())
        else:
            self.btn_ok.bind('<Button-1>', lambda event: self.eventAdd())

        self.wait_window()

    def eventAdd(self):
        self.view.addData(self.entry_name.get(), self.entry_phone.get(), self.entry_email.get(), self.entry_salary.get())
        self.destroy()

    def eventUpdate(self):
        self.view.updateData(self.entityID, self.entry_name.get(), self.entry_phone.get(), self.entry_email.get(), self.entry_salary.get())
        self.destroy()


class Search(tk.Toplevel):
    def __init__(self, entity = False):
        super().__init__(root)
        # делаем модальное окно
        self.transient(root)

        self.view = app
        self.init_child()

    def init_child(self):
        self.title('Поиск')

        self.geometry('300x100')
        self.resizable(False,False)

        # активируем перехват событий в окне
        self.grab_set()
        # переводим фокус на окно
        self.focus_set()

        label_search = tk.Label(self, text='Имя:')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        self.btn_cancel = ttk.Button(self, text='Закрыть')
        self.btn_cancel.place(x=200, y=50)
        self.btn_cancel.bind('<Button-1>', lambda event: self.eventClose())

        self.btn_search = ttk.Button(self, text='Найти')
        self.btn_search.place(x=50, y=50)
        self.btn_search.bind('<Button-1>', lambda event: self.eventSearch())

        self.protocol("WM_DELETE_WINDOW", self.eventClose)

    def eventSearch(self):
        self.view.searchData(self.entry_search.get())

    def eventClose(self):
        self.destroy()
        self.view.viewData()


class Warning(tk.Toplevel):
    def __init__(self, text):
        mb.showerror("Ошибка", text)


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('contacts.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY,
                name TEXT,
                phone TEXT,
                email TEXT,
                salary FLOAT
            )'''
        )
        self.conn.commit()

    def add(self, Name, Phone, Email, Salary):
        self.cursor.execute(
            '''INSERT INTO contacts(name,phone,email,salary) VALUES(?,?,?,?)''', (Name, Phone, Email, Salary)
        )
        self.conn.commit()

    def update(self, ID, Name, Phone, Email, Salary):
        self.cursor.execute(
            '''UPDATE contacts SET name=?, phone=? ,email=? ,salary=? WHERE id=?''', (Name, Phone, Email, Salary, ID)
        )
        self.conn.commit()

    def delete(self, ID):
        self.cursor.execute(
            '''DELETE FROM contacts WHERE id=?''', [ID]
        )
        self.conn.commit()


if __name__ == '__main__':
    # создаем объект приложения
    root = tk.Tk()
    # создаем объект базы данных
    db = DB()
    app = Main(root)
    app.pack()
    # задаем заголовок окна
    root.title('Справочник сотрудников')
    # задаем начальные размеры окна
    root.geometry('700x450')
    root.resizable(False, False)
    # данный параметр устанавливается чтобы окно закрывалось корректно
    root.protocol('WM_DELETE_WINDOW', app.quit)
    # основной цикл
    root.mainloop()