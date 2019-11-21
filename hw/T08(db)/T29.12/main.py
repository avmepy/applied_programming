#!/usr/bin/env python3
# -*-encoding: utf-8-*-
# author: Valentyn Kofanov


import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup




class Library:

    def __init__(self, filename):
        self.filename = filename


    def create(self):

        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()
        curs.execute("CREATE TABLE library (author TEXT, name TEXT, year TEXT)")

        conn.commit()
        conn.close()


    def append(self, author, name, year):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        curs.execute("INSERT INTO library VALUES (?, ?, ?)", (author, name, year))

        conn.commit()
        conn.close()


    def find(self, author, name, year):
        conn = sqlite3.connect(self.filename)
        curs = conn.cursor()

        params = []
        if author:
            params.append(('author = ?', author))
        if name:
            params.append(('name = ?', name))
        if year:
            params.append(('year = ?', year))

        query = ' AND '.join(i[0] for i in params)

        if query != "":
            query = " WHERE " + query


        curs.execute(f"SELECT * FROM library {query}", (tuple(i[1] for i in params)))

        res = curs.fetchall()
        conn.commit()
        conn.close()
        return list(res)





class SearchApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.author_input = None
        self.name_input = None
        self.year_input = None
        self.button_add = None
        self.button_search = None
        self.db = Library("library.db")
        try:
            self.db.create()
        except:
            pass


    def build(self):

        al = AnchorLayout()

        bl_search = BoxLayout(spacing=5, orientation="vertical", size_hint=[.6, .5])
        gl_search = GridLayout(cols=2, padding=[30], spacing=3)

        self.author_input = TextInput()
        self.name_input = TextInput()
        self.year_input = TextInput()
        self.button_search = Button(text="search", on_press=self.search)
        self.button_add = Button(text="add", on_press=self.add)


        gl_search.add_widget(Label(text="Author:"))
        gl_search.add_widget(self.author_input)

        gl_search.add_widget(Label(text="Book name:"))
        gl_search.add_widget(self.name_input)

        gl_search.add_widget(Label(text="Year:"))
        gl_search.add_widget(self.year_input)


        bl_search.add_widget(gl_search)
        bl_search.add_widget(self.button_search)
        bl_search.add_widget(self.button_add)

        al.add_widget(bl_search)

        return al

    def search(self, instance):

        def close(instance):
            popup.dismiss()


        author = self.author_input.text
        # if not author:
        #     author = '*'
        name = self.name_input.text
        # if not author:
        #     name = '*'
        year = self.year_input.text
        # if not author:
        #     year = '*'


        text = '\n'.join(list(' '.join(i) for i in self.db.find(author, name, year)))

        content = AnchorLayout()
        bl = BoxLayout(orientation="vertical", spacing=5)

        bl.add_widget(Label(text=text))
        bl.add_widget(Button(text="close", on_press=close, size_hint=(1, .4)))

        content.add_widget(bl)



        popup = Popup(title='search result: ', content=content, size_hint=(None, None), size=(500, 800))
        popup.open()


    def add(self, instance):

        def close(instance):
            popup.dismiss()

        def submit(instance):
            self.db.append(author.text, name.text, year.text)

        content = AnchorLayout()

        bl_add = BoxLayout(spacing=5, orientation="vertical", size_hint=[.8, .7])

        author = TextInput()
        name = TextInput()
        year = TextInput()

        gl_add = GridLayout(cols=2, padding=[30], spacing=3)

        gl_add.add_widget(Label(text='author: '))
        gl_add.add_widget(author)
        gl_add.add_widget(Label(text='name: '))
        gl_add.add_widget(name)
        gl_add.add_widget(Label(text='year: '))
        gl_add.add_widget(year)

        bl_add.add_widget(gl_add)


        bl_add.add_widget(Button(text='submit', on_press=submit))
        bl_add.add_widget(Button(text='close', on_press=close))

        content.add_widget(bl_add)


        popup = Popup(title='add new book', content=content, size=(1000, 1000), size_hint=(None, None))
        popup.open()


if __name__ == '__main__':
    SearchApp().run()

