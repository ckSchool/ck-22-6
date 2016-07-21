import kivy
kivy.require('1.8.0')

from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')
#Config.set('graphics', 'resizable', 0)

from kivy.app import App

from kivy.uix.label      import Label
from kivy.uix.popup      import Popup
from kivy.uix.image      import Image
from kivy.uix.button     import Button
from kivy.uix.dropdown   import DropDown
from kivy.uix.boxlayout  import BoxLayout
from kivy.uix.textinput  import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
   
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty, AliasProperty

from kivy.clock      import Clock

from functools import partial


import LabelC

from models    import User, Forms

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import text as alchemy_text

import sqlite3
print 'sqlite ', sqlite3.sqlite_version, ' for python :', sqlite3.version

conn = sqlite3.connect('testDB.db', timeout=10)

cur = conn.cursor()    
v=cur.execute('SELECT SQLITE_VERSION()')
print 'SQLITE_VERSION',v
#705L: 'Vivien Ingrid'
#2L: 'Angelia Ingrid'
#68: 'Brian Ingmar'

# set up dummy data  # server messages
cur.execute("DROP TABLE IF EXISTS messages")
cur.execute("CREATE TABLE messages(id INT, child_id INT,  message TEXT, date TEXT, read INT, user_id)")

cur.execute("INSERT INTO messages VALUES(1, 705, 'message 1 for Vivien',  '01,01,2016', 1, 1)")
cur.execute("INSERT INTO messages VALUES(2, 705, 'message 2 for Vivien',  '01,01,2016', 1, 1)")
cur.execute("INSERT INTO messages VALUES(3, 705, 'message 3 for Vivien',  '01,01,2016', 0, 1)")
cur.execute("INSERT INTO messages VALUES(4, 705, 'message 4 for Vivien',  '01,01,2016', 0, 1)")
cur.execute("INSERT INTO messages VALUES(5,   2, 'message 1 for Angelia', '01,01,2016', 1, 1)")
cur.execute("INSERT INTO messages VALUES(6,   2, 'message 2 for Angelia', '01,01,2016', 1, 1)")
cur.execute("INSERT INTO messages VALUES(7,   2, 'message 3 for Angelia', '01,01,2016', 0, 1)")
cur.execute("INSERT INTO messages VALUES(8,  68, 'message 1 for Brian',   '01,01,2016', 1, 1)")
cur.execute("INSERT INTO messages VALUES(9,  68, 'message 2 for Brian',   '01,01,2016', 0, 1)")






cur.executescript("DROP TABLE IF EXISTS stored_messages; CREATE TABLE stored_messages(id INT, child_id INT,  message TEXT, date TEXT)")
conn.commit()
cur.execute("INSERT INTO stored_messages VALUES(1, 705 , 'message 1 for Vivien',  '01,01,2016')")
cur.execute("INSERT INTO stored_messages VALUES(5,   2 , 'message 1 for Angelia', '01,01,2016')")
cur.execute("INSERT INTO stored_messages VALUES(6,   2 , 'message 2 for Angelia', '01,01,2016')")
cur.execute("INSERT INTO stored_messages VALUES(2, 705 , 'message 2 for Vivien',  '01,01,2016')")
cur.execute("INSERT INTO stored_messages VALUES(8,  68 , 'message 1 for Brian',   '01,01,2016')")







ma =''

try:
    print 'try vostro 17"' 
    engine = create_engine('mysql://root:password@localhost/ckdb', echo=True)
    DBSession = sessionmaker()
    DBSession.configure(bind=engine)
    session = DBSession()
    session.query(User)
    self.fred()
    
except:
    try:
        print ' try my 15"'
        engine = create_engine('mysql://root:andrewroot@localhost/ckdb', echo=True)
        DBSession = sessionmaker()
        DBSession.configure(bind=engine)
        session = DBSession()
        session.query(User)
    except:
        print ' no connection'


user_id    = 0
student_id = 0
students_name = ''
users_name = ''
selected_class_id = 0
subject_id = 0
children_dict = {}
        
import random

class ScreenMain(BoxLayout):
    top_layout   = ObjectProperty(None)
    dd_btn       = ObjectProperty(None)
    student_image_btn    = ObjectProperty('None')
    
    def __init__(self,**kwargs):
        super (ScreenMain,self).__init__(**kwargs)
        self.dropdown = DropDown()
        
        self.messages_grid = self.ids.messages_grid
        self.child_id = 0
        self.msg_id =10
        Clock.schedule_once(self.prepare, 0)
        
        
    def prepare(self, *args):
        global user_id
        print 'prepare'
        # if first time or loged out
        user_id = 0
        self.child_id = 0
        print ' call the login popup'
        p = LoginPopup()
        p.open()
        Clock.schedule_interval(self.get_new_messages, 1)
        Clock.schedule_interval(self.send_rnd_msg, 2)
        
    def send_rnd_msg(self, *args):

        cid = (random.choice([705,2,68]))

        sql ="INSERT INTO messages VALUES(%d, %d, 'rnd msg',  '01,01,2016', 0, 1)" % (self.msg_id, cid )

        print sql
        cur.execute(sql)

        self.msg_id +=1
                    
    def new_user(self):
        global user_name
        print 'new_user'
        user_name = ""        
        if user_id > 0:
            user_name = "Andrew Watts" # fetch name for user_id
            first_id = self.add_children()
            # need to get first list
            self.child_selected(first_id)

    def add_children(self):
        global user_id, children_dict
        children_dict = {}
        print 'add_children'
        # sql  get children for parent
        user_id = 180 # test
        sql = 'SELECT id, name \
                FROM students \
                WHERE father_id=180' 

        alchemysql = alchemy_text(sql)
        result = engine.execute(alchemysql)

        children = [r for r in result]
        count_children = len(children)
        
        for sid, name in children:
            children_dict[sid] = name
        print 'children_dict',children_dict
        self.create_dropdown(children)

        first_id   = children[0][0]
        first_name = children[0][1]
        
        ddbtn = self.ids.btn_ddID
        ddbtn.text = str(first_name)
        
        return first_id

    def drop_down(self, x=''):
        # open the dropdown buttons
        self.dropdown.open(x)
        # set mainbutton text to select item
        self.dropdown.bind(on_select=lambda instance, y: setattr(x, 'text', y))

    def create_dropdown(self, children):
        print 'create_dropdown'
        
        self.dropdown.clear_widgets()
        for child in children:
            # create button
            btn = self.create_button(child)
            # add it the dropdown
            self.dropdown.add_widget(btn)

    def create_button(self, child):
        print 'create_button'
        gid, name = child
        
        # specify the height so the dropdown can calculate the area it needs.
        # store the class id in the buttons name
        btn = Button(text= name, size_hint_y=None, height=40, name=str(gid))
        
        # attach a callback that will call the select() method on the dropdown.
        # pass the button text as the data of the selection.
        btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        
        # the call to update student list when button pressed
        btn.bind(on_release=partial(self.child_selected, gid))
        return btn

    def create_mask(self):
        self.mask = Image.new('L', (200,200), 0)
        draw = ImageDraw.Draw(self.mask) 
        draw.ellipse((0, 0) + self.mask.size, fill=255)
    
    def child_selected(self, *args ):
        print 'child_selected'

        self.messages_grid.clear_widgets()
        
        self.child_id = args[0]
  
        image_id = str(self.child_id).zfill(5)
        self.imagefile =  'student_images/%s' % image_id
        print 'the imagefile', self.imagefile

        name = "Name:%s \n ID:%d" % (children_dict[self.child_id], self.child_id)
        studentname_label = self.ids.studentname_label
        studentname_label.text = name

        # would like to change img_btn to image
        # image would be a background fill with a 
        # round masked image of the student on top
        # or student behind and the fill has a hole in it

        img_btn = self.ids.student_image_btn
        img_btn.background_normal = 'student_images/00001.jpg'

        stored_messages = self.get_stored_messages()
  
        # get new messages
        self.get_new_messages()
        
        
    def get_new_messages(self, x=0):
        new_messages = self.select_column_and_value("SELECT id, message, date \
                                                       FROM messages \
                                                      WHERE child_id = %d \
                                                        AND user_id = 1 \
                                                        AND read <> 1" % self.child_id)
        txt = "there are %d new messages for child_id %d)" % (len(new_messages), self.child_id)
        print txt
        for msg in new_messages:
            msg_id, child_id, content, date = msg['id'], self.child_id, msg['message'], msg['date'] 

            sql = "INSERT INTO stored_messages VALUES (%d, %d, '%s', '%s')" % (msg_id, child_id, content, date)
            print sql
            cur.execute(sql)

            sql = "UPDATE messages SET read=1 WHERE id=%d"  % (msg_id, )
            print sql
            cur.execute(sql)
            

            self.display_msg(msg, 1)

    def notify_db(self, msg_id):
        pass
        

    def select_column_and_value(self, sql, parameters=()):
        execute = cur.execute(sql, parameters)
        fetch = execute.fetchall()

        if fetch is None:
            return {k[0]: None for k in execute.description}

        else:
            lis = []
            for row in fetch:
                lis.append( {k[0]: v for k, v in list(zip(execute.description, row))} )
            return lis


    def get_stored_messages(self):
        print 'get_stored_messages'
        
        stored_messages = self.select_column_and_value("SELECT id, message, date FROM stored_messages WHERE child_id = %d " % self.child_id)

        for msg in stored_messages:
            self.display_msg(msg)
        return stored_messages
   
        # save to file
        # if self.notify_db(key): is sucsessful
        #     pass
        # else:
        #     return # wait for clock 
            

    def display_msg(self, entry, new=0):
        print 'display_msg ', entry
        content = entry['message']
        print 'content = ', content
        if new:
           content = 'new %s' % content 
        lbl = Label( text = content)
        self.messages_grid.add_widget(lbl)

        widget = self.ids.messages_grid
        widget.bind(minimum_height= widget.setter('height'))
    

class LoginPopup(Popup):
    def popupwrong_password(self):
        p = CustomPopup()
        p.open()
        
    def login(self, *args):
        global user_id
        res = 0
        # get widgets from kivy
        email_input    = self.ids.email_input_p
        password_input = self.ids.password_input_p
        # get the data 
        user_email    = email_input.text
        user_password = password_input.text

        #res = session.query(User).filter(and_(User.email == user_email, User.password == user_password)).count()

        # for testing
        res = 1
        
        if res > 0:
            # for testing
            user_id = 1
            self.dismiss()
            ma.new_user()
            
        else:
            self.popupwrong_password()
    
            
class CustomPopup(Popup):
    pass

class DropdownButton(Button):
    id    = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')


from kivy.storage.jsonstore import JsonStore

mystore = JsonStore('hello.json')

class xx4_parentApp(App):
    global mystore
    # put some values
    mystore.put(1, child_id=1, msg='msg 1 for 1')
    mystore.put(2, child_id=1, msg='msg 2 for 1')
    mystore.put(3, child_id=1, msg='msg 3 for 1')
    mystore.put(4, child_id=2, msg='msg 1 for 2')

    

    def my_callback(self, store, key, result):
        global mystore
        print('the key', key, 'has a value of', result)

 


    
    def build(self):
        global ma
        ma = ScreenMain()
        return ma
  

if __name__ == '__main__':
    app=xx4_parentApp()
    app.run()
