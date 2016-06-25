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
from kivy.uix.screenmanager import Screen, ScreenManager 
   
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, ListProperty, AliasProperty
from kivy.event      import EventDispatcher
from kivy.clock      import Clock
from kivy.lang       import Builder

from functools import partial

import LabelC


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import and_, or_, not_
from sqlalchemy import text as alchemy_text


from models import User, Forms

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
        
class ScreenLogin(Screen):
    def __init__(self,**kwargs):
        super (ScreenLogin,self).__init__(**kwargs)

    def popupwrong_password(self):
        p = CustomPopup()
        p.open()

    def login2(self, *args):
        global user_id
        email_input = self.ids.email_input
        user_email  = email_input.text

        password_input =  self.ids.password_input
        user_password  = password_input.text

        res = session.query(User).filter(and_(User.email == user_email, User.password == user_password)).count()
        if res > 0:
            user_id = 1
            ScreenMain=app.my_screenmanager.get_screen('ScreenMain')
            ScreenMain.new_user()
            app.my_screenmanager.current = 'ScreenMain'
        else:
            self.popupwrong_password()

class LoginPopup(Popup):
    def popupwrong_password(self):
        p = CustomPopup()
        p.open()
        
    def login(self, *args):
        global user_id
        

        res = 0
        # get data from kivy
        email_input = self.ids.email_input_p
        password_input =  self.ids.password_input_p
        
        user_email  = email_input.text

        
        user_password  = password_input.text

        res = session.query(User).filter(and_(User.email == user_email, User.password == user_password)).count()
        if res > 0:
            user_id = 1
            ScreenMain=app.my_screenmanager.get_screen('ScreenMain')
            ScreenMain.new_user()
            app.my_screenmanager.current = 'ScreenMain'

            self.dismiss()
            
        else:
            self.popupwrong_password()
    
            
class CustomPopup(Popup):
    pass

class DropdownButton(Button):
    id   = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')

class ScreenMain(Screen):
    top_layout   = ObjectProperty(None)
    dd_btn       = ObjectProperty(None)
    image_source = StringProperty('')
    #btn_ddID = ObjectProperty(None)

    def __init__(self,**kwargs):
        super (ScreenMain,self).__init__(**kwargs)
        Clock.schedule_once(self.prepare, 0)
        self.dropdown = DropDown()

        print '__init__  done'

    def prepare(self, *args):
        global user_id

        print 'prepare'
        # if first time or loged out
        user_id = 0
        # call the login screen
        p = LoginPopup()
        #p = CustomPopup()
        p.open()
        #self.manager.current = 'ScreenLogin'

    def new_user(self):
        global user_name

        print 'new_user'
        user_name = ""        
        if user_id > 0:
            user_name = "Andrew Watts" # fetch name for user_id
            first_id = self.add_children()
            # need to get first list
            self.child_selected(first_id)
        else:
            self.manager.current = 'ScreenLogin'

    def add_children(self):
        global user_id, children_dict
        children_dict = {}
        print 'add_children'
        # sql  get children for parent
        count_children = 0
        while count_children < 3:
            sql = 'SELECT id, name \
                    FROM students \
                    WHERE mother_id=%d \
                    OR father_id=%d \
                    OR guardian_id= %d' % (user_id, user_id, user_id)

            alchemysql = alchemy_text(sql)
            result = engine.execute(alchemysql)

            children = [r for r in result]
            count_children = len(children)
        
            user_id += 1
        for sid, name in children:
            children_dict[sid] = name
        #print 'children_dict',children_dict
        self.create_dropdown(children)

        first_id   = children[0][0]
        first_name = children[0][1]
        
        ddbtn = self.ids.btn_ddID
        ddbtn.text = str(first_name)
        
        return first_id
            
        
    def changer(self,*args):
        print 'changer'
        pass


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

    def child_selected(self, *args ):
        print 'child_selected', 
        child_id = args[0]
        image_id = str(child_id).zfill(5)
        print 'image_id',image_id
        imagefile =  'student_images/%s' % image_id
        print 'the imagefile', imagefile
        name = children_dict[child_id]
        studentname_label = self.ids.studentname_label
        studentname_label.text = imagefile
        imgbtn = self.ids.student_image_btn
        imgbtn.background_normal = 'student_images/00001.jpg'



class xx4_parentApp(App):
    def build(self):
        self.my_screenmanager = ScreenManager()
        
        screenMain   = ScreenMain(  name='ScreenMain')
        screenLogin  = ScreenLogin( name='ScreenLogin')
   
               
        self.my_screenmanager.add_widget(screenMain)
        self.my_screenmanager.add_widget(screenLogin)
        return self.my_screenmanager

if __name__ == '__main__':
    app=xx4_parentApp()
    app.run()
