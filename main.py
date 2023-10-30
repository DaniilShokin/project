import tkinter as tk
from tkinter import ttk
import sqlite3


# класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # инициализация виджетов главного окна
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_add = tk.Button(toolbar, text='Добавить', bg='#d7d7d7',
                            bd=0, image=self.add_img,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # создание кнопки изменения данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                    image=self.update_img, command=self.open_update_child)
        btn_edit_dialog.pack(side=tk.LEFT)

        # создание кнопки удаления записи
        self.delete_img = tk.PhotoImage(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        # кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                               image=self.search_img, command=self.open_search)
        btn_search.pack(side=tk.LEFT)

        # кнопка обновления
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0,
                                image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Добавляем Treeview
        self.tree = ttk.Treeview(root,
                                 columns=('id', 'name', 'phone', 'email'),
                                 height=45,
                                 show='headings')

        # добавляем параметры колонкам
        self.tree.column('id', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        # подписи колонок
        self.tree.heading('id', text='id')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')

        # упаковка
        self.tree.pack(side=tk.LEFT)

    # метод добавления даных
    def records(self, name, phone, email):
        self.db.insert_data(name, phone, email)
        self.view_records()

    #отображение данных в treeview
    def view_records(self):
        # выбираем информацию из БД
        self.db.cur.execute('SELECT * FROM users')
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в виджет таблицы всю информацию из БД
        [self.tree.insert('', 'end', values=i)for i in self.db.cur.fetchall()]

    # удаление записей
    def delete_records(self):
        # цикл по выделенным записям
        for selection_item in self.tree.selection():
            # удаление из БД
            self.db.cur.execute('''DELETE FROM users WHERE id=?''',
                              (self.tree.set(selection_item, '#1'),))
        # сохранение изменений в БД
        self.db.conn.commit()
        # обновление виджета таблицы
        self.view_records()

    # поиск записи по ФИО
    def search_records(self, name):
        name = ('%' + name + '%',)
        self.db.cur.execute(
            '''SELECT * FROM users WHERE name LIKE ?''', name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row)
         for row in self.db.cur.fetchall()]

    # обновление (изменение) данных
    def update_record(self, name, phone, email):
        self.db.cur.execute('''UPDATE users SET name=?, phone=?, email=? WHERE ID=?''',
                          (name, phone, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # метод вызывающий дочернее окно
    def open_child(self):
        Child()


    # метод отвечающий за вызов окна для поиска
    def open_search(self):
        Search()

    # метод отвечающий за вызов окна для изменения данных
    def open_update_child(self):
        Update()

# класс дочернего окна
# Toplevel - окно верхнего уровня
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app



    # инициализация виджетов главного окна
    def init_child(self):
        # заголовок окна
        self.title('Добавление контакта')
        # размер окна
        self.geometry('400x200')
        # ограничение изменения размеров окна
        self.resizable(False, False)
        # перехватываем события
        self.grab_set()
        # перехватываем фокус
        self.focus_set()

        # подписи
        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=50)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=80)
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=110)

        # добавляем строку ввода для ФИО
        self.entry_name = tk.Entry(self, text='ФИО:')
        self.entry_name.place(x=200, y=50)
        # добавляем строку ввода для телефона
        self.entry_phone = tk.Entry(self, text='Телефон:')
        self.entry_phone.place(x=200, y=80)
        # добавляем строку ввода для email
        self.entry_email = tk.Entry(self, text='E-mail:')
        self.entry_email.place(x=200, y=110)

        # кнопка закрытия дочернего окна
        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=200, y=150)

        # срабатывание по ЛКМ
        # при нажатии кнопки вызывается метод records, которому передаюся значения из строк ввода
        btn_add = tk.Button(self, text='Добавить')
        btn_add.bind('<Button-1>', lambda ev: self.view.records(self.entry_name.get(),
                                                                self.entry_phone.get(),
                                                                self.entry_email.get()))
        btn_add.place(x=265, y=150)


# класс окна для обновления, наследуемый от класса дочернего окна
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.view = app
        self.db = db
        self.default_data()

    def init_update(self):
        self.title('Изменение контакта')
        self.btn_add = ttk.Button(self, text='Изменить')
        self.btn_add.place(x=100, y=150)
        self.btn_add.bind('<Button-1>', lambda ev: self.view.update_record(self.entry_name.get(),
                                                                          self.entry_phone.get(),
                                                                          self.entry_email.get()))

        # закрываем окно редактирования
        btn_upd.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('SELECT * FROM users WHERE id = ?', (id, ))
        # получаем доступ к первой записи из выборки
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])


# класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = tk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = tk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>',
                        lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>',
                        lambda event: self.destroy(), add='+')


# класс БД
class Db:
    def __init__(self):
        # создаем соединение с БД
        self.conn = sqlite3.connect('contacts.db')
        # создание объекта класса cursor, используемый для взаимодействия с БД
        self.cur = self.conn.cursor()
        # выполнение запроса к БД
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT)''')
        self.conn.commit()

    # метод добавления в БД
    def insert_data(self, name, phone, email):
        self.cur.execute('''INSERT INTO users (name, phone, email) VALUES (?, ?, ?)''', (name, phone, email))
        self.conn.commit()


# действия при запуске окна
if __name__ == '__main__':
    root = tk.Tk()
    # экземпляр класса DB
    db = Db()
    app = Main(root)
    app.pack()
    # заголовок окна
    root.title('Телефонная книга')
    # ограничение изменения размеров окна
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()