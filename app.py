from tkinter import *                # import everything from tkinter
from tkinter.ttk import *            # for beautful widgets
from tkinter import messagebox as mb # import messagebox
import sqlite3                       # import database module


class MyApp:
    """Initialises the Login window"""
    def __init__(self, parent):
        """Constructor"""
        self.root = parent
        self.root.iconbitmap('icon.ico')
        self.root.title("Please Log In to Proceed")
        self.frame = Frame(parent)
        self.frame.pack()
        Label(self.frame,text='Username').grid(row=0)
        self.username = Entry(self.frame)
        self.username.grid(row=0,column=1)
        Label(self.frame,text='Password').grid(row=1)
        self.password = Entry(self.frame,show="*")
        self.password.grid(row=1,column=1)
        b = Button(self.frame,text='Login',command = self.openframe)
        b.grid(row=2)

        
    def clear(self):
        self.username.delete(0,END)
        self.password.delete(0,END)
 
    def hide(self):
        """Hides the current frame"""
        self.root.withdraw()
 
    def openframe(self):
        data = self.username.get(),self.password.get()
        if '' in data: # if blank record then stop
            mb.showinfo('Blank Fields','Fill all the fields please')
        else:
            try:
                con = sqlite3.connect('users.db') # connect to the database
                c = con.cursor()
                c.execute('''SELECT * FROM users''')
                rows = c.fetchall()
                for row in rows:
                    user,password = row[0],row[1]
                    if user == data[0] and password == data[1]:
                        self.hide()
                        frame = MainFrame(self)
                else:
                    self.clear()
            except sqlite3.DatabaseError as e:
                mb.showerror('Error occurred','Something went wrong oops')
            

    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()


class MainFrame(Toplevel):
    """Launches the main application window"""
 
    def __init__(self, original):
        """Constructor"""
        self.master = original
        Toplevel.__init__(self, relief=RIDGE, bd=2)
        self.geometry("400x300+500+90")
        #self.resizable(0,0)
        self.iconbitmap('icon.ico')
        self.title("Infinity Event Management System")
        self.master.iconname('events')
        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.filemenu = Menu(self.menu,tearoff=False)
        self.filemenu.add_command(label='Search',command=self.opensearch)
        self.filemenu.add_command(label='Create User',command=self.openframe)
        self.filemenu.add_command(label='Logout',command=self.logout)
        self.menu.add_cascade(label = 'File',underline=0,menu=self.filemenu)
        self.aboutmenu = Menu(self.menu,self.menu,tearoff=False)
        self.aboutmenu.add_command(label='About',command=self.openabout)
        self.menu.add_cascade(label = 'Help',underline=0,menu=self.aboutmenu)
        Label(self,text='Name').grid(row=0,sticky=W)
        Label(self,text='Surname').grid(row=1,sticky=W)
        Label(self,text='Phone Num').grid(row=2,sticky=W)
        Label(self,text='Email').grid(row=3,sticky=W)
        Label(self,text='Details').grid(row=4,sticky=W)
        Label(self,text='Date').grid(row=5,sticky=W)
        self.e1 = Entry(self,width=45)
        self.e1.grid(row=0,column=1)
        self.e2 = Entry(self,width=45)
        self.e2.grid(row=1,column=1)
        self.e3 = Entry(self,width=45)
        self.e3.grid(row=2,column=1)
        self.e4 = Entry(self,width=45)
        self.e4.grid(row=3,column=1)
        self.e5 = Entry(self,width=45)
        self.e5.grid(row=4,column=1)
        self.e6 = Entry(self,width=45)
        self.e6.grid(row=5,column=1)
        Button(self,text='Save',command=self.save_to_database).grid(row=6)


    def logout(self):
        if mb.askquestion('Logout','Do you want to logout?',icon ='warning') == 'yes':
            self.destroy()
        else:
            pass

    def grabinfo(self):
        '''Collects information from the entry field'''
        name = self.e1.get()
        sname= self.e2.get()
        tel = self.e3.get()
        email = self.e4.get()
        detail = self.e5.get()
        date = self.e6.get()
        data = name,sname,tel,email,detail,date
        return data
        

    def clear(self):
        self.e1.delete(0,END)
        self.e2.delete(0,END)
        self.e3.delete(0,END)
        self.e4.delete(0,END)
        self.e5.delete(0,END)
        self.e6.delete(0,END)

    def save_to_database(self):
        '''Creates the database and stores the values'''

        if '' in self.grabinfo():
            mb.showinfo('Incomplete Details','Fill all the fields')
        else:
            try:
                con = sqlite3.connect('events.db')
                #con2 = sqlite3.connect('users.db')
                cur = con.cursor()
                #cur2 = con2.cursor()
                cur.execute('''CREATE TABLE IF NOT EXISTS events(name TEXT NOT NULL,
                                           surname TEXT NOT NULL,
                                           phone number PRIMARY KEY NOT NULL,
                                           email TEXT,
                                           address TEXT NOT NULL,
                                           date DATE NOT NULL)''')
                #cur2.execute('''CREATE TABLE IF NOT EXISTS users(name TEXT NOT NULL,
                                          # password TEXT NOT NULL)''')
                cur.execute('''INSERT INTO events VALUES(?,?,?,?,?,?)''',self.grabinfo())
                con.commit()
                #con2.commit()
                mb.showinfo('Records Saved','The record has been saved successfully')
            except sqlite3.DatabaseError as e:
                mb.showinfo('Database Error','There was a problem with the database %s'%e)
        self.clear() # calling the clear method
       

    def hide(self):
        """"""
        self.withdraw()

 
    def openframe(self):
        """Opens the users frame"""
        self.hide()
        subFrame = UserFrame(self)

    def openabout(self):
        '''Opens the about frame'''
        self.hide()
        subframe = AboutFrame(self)

    def opensearch(self):
        '''Opens the search frame'''
        self.hide()
        frame = SearchFrame(self)

    def show(self):
        """"""
        self.root.update()
        self.root.deiconify()
 
  
    def onClose(self):
        """"""
        self.destroy()
        self.original_frame.show()
        
########################################################################
class UserFrame(Toplevel):
    """Launches the users frame"""
 
    def __init__(self, original):
        """Constructor"""
        self.master = original
        Toplevel.__init__(self)
        self.geometry("300x200+500+90")
        self.iconbitmap('icon.ico')
        self.resizable(0,0)
        self.title('Register New Users')
        Label(self,text='Username*').grid(row=0,sticky=W)
        self.username = Entry(self)
        self.username.grid(row=0,column=1)
        Label(self,text='Password*').grid(row=1,sticky=W)
        self.password = Entry(self,show='*')
        self.password.grid(row=1,column=1)
        Label(self,text='Re-Enter Password*').grid(row=2,sticky=W)
        self.password1 = Entry(self,show='*')
        self.password1.grid(row=2,column=1)
        b = Button(self,text='Save',command=self.grabinfo) # to add a method to add to database
        #b.bind('<Enter>',self.log_in)       # binding with the enter button to the event
        b.grid(row=3,column=0,sticky=W)
        b2 = Button(self,text='Back',command=self.openframe)
        b2.grid(row=3,column=1,sticky=W)

    def clearentries(self):
        self.username.delete(0,END)
        self.password.delete(0,END)
        self.password1.delete(0,END)

    def grabinfo(self):
        entries = self.username.get(),self.password.get(),self.password1.get()
        
        if '' in entries:
            # if a field is empty
            mb.showinfo('Incomplete Details','Make sure all fields are field!')
        else:
            # enter the values into a database
            if entries[1] == entries[2]:
                data = entries[0],entries[1]
                try:
                    con1 = sqlite3.connect('users.db')
                    cur1 = con1.cursor()
                    cur1.execute('''CREATE TABLE IF NOT EXISTS users(name TEXT NOT NULL,
                                                                     password TEXT NOT NULL)''')
                    cur1.execute('''INSERT INTO users VALUES(?,?)''',(data))
                    # show that records saved correctly
                    mb.showinfo('Success','Records saved successfully!')
                    con1.commit()
                    con1.close()
                except sqlite3.DatabaseError as e:
                    mb.showerror('Error','Error occurred %s!' % e)
            else:
                # passwords dont match
                mb.showinfo('Passwords Error','Passwords dont match!')
        self.clearentries()
            
    def hide(self):
        """"""
        self.withdraw()
 
  
    def openframe(self):
        """"""
        self.hide()
        subFrame = MainFrame(self)

########################################################################
class AboutFrame(Toplevel):
    """Launches the users frame"""

    def __init__(self, original):
        """Constructor"""
        self.master = original
        Toplevel.__init__(self)
        self.geometry("400x300+500+90")
        self.iconbitmap('icon.ico')
        self.resizable(0,0)
        self.title('About Software')
        text = '''
               Programmed by Beven Nyamande AKA 14K.
                  ---------------------------------------------------
                  
                  Phone: +263777054115
                  
                  Email: bevennyamande@gmail.com
                  
                  Skype: beven.nyamande
                  
                  Twitter: @bevy88
                  ---------------------------------------------------
                  
               '''
        m = Message(self,text=text,bg='steelblue',fg='black',font=('times',12,'italic'))
        m.pack()
        
        b = Button(self,text='Ok',command=self.openframe) # to add a method to add to database
        b.pack()


    def hide(self):
        """"""
        self.withdraw()
 
  
    def openframe(self):
        """"""
        self.hide()
        subFrame = MainFrame(self)

##############################################################################
class SearchFrame(Toplevel):
    """Launches the users frame"""

    def __init__(self, original):
        """Constructor"""
        self.master = original
        Toplevel.__init__(self)
        self.config(bg='steelblue')
        self.geometry("600x400+500+90")
        self.iconbitmap('icon.ico')
        #self.resizable(0,0)
        self.title('Searching Records')
        b = Button(self,text='Display Events',command =self.results) # to add a method to add to database
        b2 = Button(self,text='Back',command=self.openframe)
        b.pack()
        b2.pack()

    def results(self):
        try:
            con = sqlite3.connect('events.db')
            c = con.cursor()
            c.execute('''SELECT * FROM events''')
            records = c.fetchall()
            rows = records.__len__()
            columns = records[0].__len__()
            list_columns = [columnames[0] for columnames in c.description]
            tree = Treeview(self)
            tree['columns'] = list_columns

            for column in list_columns:
                tree.column("#0", width=0)
                tree.column(column, width=70)
                tree.heading(column, text=column.capitalize())

            for record in records:
                tree.insert("", 0, text="", values=record)
            tree.pack(expand=True)
            
        except sqlite3.DatabaseError as e:
            mb.showerror('Error','Error occurred %s'% e)

    def hide(self):
        """"""
        self.withdraw()
 
  
    def openframe(self):
        """"""
        self.hide()
        subFrame = MainFrame(self)

if __name__ == "__main__":
    root = Tk()
    root.geometry("300x150+500+90")
    root.resizable(0,0)
    root.iconbitmap('icon.ico')
    app = MyApp(root)
    root.mainloop()
 
