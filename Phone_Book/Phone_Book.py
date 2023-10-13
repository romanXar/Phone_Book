import tkinter as tk
from tkinter import ttk
import sqlite3




class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def open_search_dialog(self):
        Search()


    # поиск записей   
    def search_records(self,name):
        name =('%'+name+'%',)
        self.db.c.execute("""SELECT * FROM db WHERE name LIKE ?""",name)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values = row) 
         for row in self.db.c.fetchall()]




  
    # удаление записей    
    def delete_records(self):
        # цикл по выделенным записям
        for selection_item in self.tree.selection():
            # удаление из БД
            self.db.c.execute("""DELETE FROM db WHERE id = ?""",(self.tree.set(selection_item,'#1'),))
        # сохранение изменений в БД
        self.db.conn.commit()
        # обновление виджета таблицы
        self.view_records()



    # обновление записей      
    def update_record(self,name,tel,email):
        self.db.c.execute("""
        UPDATE db SET name = ?,tel = ?,email = ?
        WHERE ID = ?""",(name,tel,email,self.tree.set(
            self.tree.selection()[0],'#1')))
        self.db.conn.commit()
        self.view_records()

    def open_update_dialog(self):
        Update()

    def records(self,name,tel,email):
        self.db.insert_data(name,tel,email)
        self.view_records()

    def init_main(self):
        # создаем панель инструментов
        toolbar = tk.Frame(bg='#07d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
 
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email'), height=45, show='headings')
        
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300,anchor=tk.CENTER)
        self.tree.column("tel", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        
        self.tree.heading("ID", text='ID')
        self.tree.heading("name", text='ФИО')
        self.tree.heading("tel", text='Телефон')
        self.tree.heading("email", text='E-mail')

        self.tree.pack(side=tk.LEFT)

        # создаем кнопки изменения данных

        # кнопка добавления данных
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image = self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        # кнопка изменения данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar,bg = '#d7d8e0',bd = 0,image =self.update_img,command = self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        # кнопка удаления данных
        self.delete_img = tk.PhotoImage(file = './img/delete.png')
        btn_delete = tk.Button(toolbar,bg = '#d7d8e0',bd=0,image = self.delete_img,command = self.delete_records)
        btn_delete.pack(side = tk.LEFT)
        
        # кнопка поиска данных
        self.search_img = tk.PhotoImage(file = './img/search.png')
        btn_search = tk.Button(toolbar,bg = '#d7d8e0',bd=0,image = self.search_img,command = self.open_search_dialog)
        btn_search.pack(side = tk.LEFT)
           
    def init_child(self):
        # заголовок окна
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

    def open_dialog(self):
        Child()
        # вывод данных в виджет таблицы
    def view_records(self):
        # выбираем информацию из БД
        self.db.c.execute("""SELECT * FROM db""")
        # удаляем все из виджета таблицы
        [self.tree.delete(i) for i in self.tree.get_children()]
        # добавляем в вывод таблицы всю информацию из БД
        [self.tree.insert('','end',values = row)
         for row in self.db.c.fetchall()]



class Child(tk.Toplevel,Main):
    def __init__ (self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        # заголовок окна
        self.title('добавить')
        # размер окна
        self.geometry('400x220')
        # ограничение изменени размера окна
        self.resizable(False,False)
        # перехват всех событий происходящих в окне
        self.grab_set()
        # захват фокуса
        self.focus_set()
        
        
        
        #Подписи
        label_name = tk.Label(self, text='ФИО')     
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)     
        label_sum = tk.Label(self, text = 'E-mail')
        label_sum.place(x=50, y=110)

        # добавляет строку ввода для наименования
        self.entry_name = ttk.Entry(self)
        # меняет координаты объекта
        self.entry_name.place(x=200, y=50)

        # добавляет строку ввода для email
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200,y=80)
        
        # добавляет строку ввода для телефона
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)
        
        # кнопка закрытия дочернего окна
        self.btn_cancel = ttk.Button(self, text='Закрыть',command=self.destroy)
        self.btn_cancel.place(x=300,y=170)
        
        # кнопка добавления
        self.btn_ok = ttk.Button(self,text='Добавить')       
        self.btn_ok.place(x=220, y=170)
        # срабатывание по ЛКМ
        # при нажатии кнопки вызывается метод records, которому передаются значения из строк ввода
        self.btn_ok.bind('<Button-1>',lambda event: self.view.records(self.entry_name.get(),
                                                                      self.entry_tel.get(),
                                                                      self.entry_email.get()))

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self,text = 'Редактировать')
        btn_edit.place(x = 205,y = 170)
        btn_edit.bind('<Button-1>',lambda event: self.view.update_record(self.entry_name.get(),
                    self.entry_email.get(),
                    self.entry_tel.get()))
        # закрывает окно редактирования
        # add= '+' позволет на одну кнопку вешать более одного события
        btn_edit.bind('<Button-1>',lambda event: self.destroy(),add = '+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute("""SELECT * FROM db WHERE id = ?""",(self.view.tree.set(self.view.tree.selection()[0],'#1')))
      
        # получает доступ к первой записи из выборки
        row = self.db.c.fetchone()           
        self.entry_name.insert(0,row[1])
        self.entry_email.insert(0,row[2])
        self.entry_tel.insert(0,row[3])

#Класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)
      

        label_search = tk.Label(self,text = 'Поиск')
        label_search.place(x = 50,y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105,y=20,width=150)

        btn_cansel = ttk.Button(self,text='Закрыть',command = self.destroy)
        btn_cansel.place(x = 185,y=50)

        btn_search = ttk.Button(self,text = 'Поиск')
        btn_search.place(x = 105,y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(),add = '+')







class DB():
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
      
        self.c = self.conn.cursor()

        self.c.execute("""
        CREATE TABLE IF NOT EXISTS db(
        id INTEGER PRIMARY KEY,
        name TEXT,
        tel TEXT,
        email TEXT
        );
        """)
        self.conn.commit()

    def insert_data(self,name,tel,email):
        self.c.execute("""
        INSERT INTO db (name,tel,email)
        VALUES (?,?,?)
        """,(name,tel,email))
        self.conn.commit()

if __name__== '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    # заголовок окна
    root.title('Телефонная книга')
    # размер окна
    root.geometry('665x458')
    # ограничение изменения размеров окна
    root.resizable(False, False)

    root.mainloop()