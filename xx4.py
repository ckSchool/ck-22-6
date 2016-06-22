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


student_list = [
    ("0", "fruit_images/Apple.64.jpg","Apple","Apple: Super Sweet"),
    ("1", "fruit_images/Banana.64.jpg","Banana","Banana: Want a bunch"),
    ("2", "fruit_images/Strawberry.64.jpg", "Strawberry", "Strawberry: Yummy"),
    ("3", "fruit_images/Orange.64.jpg","Orange","Orange: Florida's BesT"),
    ("4", "fruit_images/Pear.64.jpg","Pear","Pear: Perfect"),
    ("5", "fruit_images/Lime.64.jpg","Lime","Sharp: NZ BesT"),
    ("6", "fruit_images/Apple.64.jpg","Apple","Apple: Super Sweet"),
    ("7", "fruit_images/Banana.64.jpg","Banana","Banana: Want a bunch"),
    ("8", "fruit_images/Strawberry.64.jpg", "Strawberry", "Strawberry: Yummy"),
    ("9", "fruit_images/Orange.64.jpg","Orange","Orange: Florida's BesT"),
    ("10", "fruit_images/Pear.64.jpg","Pear","Pear: Perfect"),
    ("11", "fruit_images/Lime.64.jpg","Lime","Sharp: NZ BesT"),
    ("12", "fruit_images/Apple.64.jpg","Apple","Apple: Super Sweet"),
    ("13", "fruit_images/Banana.64.jpg","Banana","Banana: Want a bunch"),
    ("14", "fruit_images/Strawberry.64.jpg", "Strawberry", "Strawberry: Yummy"),
    ("15", "fruit_images/Orange.64.jpg","Orange","Orange: Florida's BesT"),
    ("16", "fruit_images/Pear.64.jpg","Pear","Pear: Perfect"),
    ("17", "fruit_images/Lime.64.jpg","Lime","Sharp: NZ BesT")
    ]


user_id    = 0
student_id = 0
students_name = ''
users_name = ''
selected_class_id = 0
subject_id = 0

        
class ScreenLogin(Screen):
    def __init__(self,**kwargs):
        super (ScreenLogin,self).__init__(**kwargs)

    def popupwrong_password(self):
        p = CustomPopup()
        p.open()

    def login(self, *args):
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
            
class ScreenNote(Screen):
    text = StringProperty()
    multiline = BooleanProperty(True)
        
class CustomPopup(Popup):
    pass

class DropdownButton(Button):
    id   = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')

class StudentListItemButton(Button):
    wid   = StringProperty('')
    image_source = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')

class ScreenAttend(Screen):
    pass

class ScreenTag(Screen):
    pass

class ScreenFileChooser(Screen):
    pass

class ScreenAction(Screen):
    def take_picture(self, *args):
        print 'take_picture'

    def find_picture(self, *args):
        print 'find_picture'

class ScreenStudentDetails(Screen):
    image_source = StringProperty('')
    def __init__(self,**kwargs):
        super (ScreenStudentDetails,self).__init__(**kwargs)
        
        
    def changer(self,*args):
        self.manager.current = 'ScreenStudents'

    def changer2(self,*args):
        self.manager.current = 'ScreenAttend'

    def update(self, current_student):

        details_grid = self.ids.details_grid
        details_grid.clear_widgets()

        student_image_btn = self.ids.student_image_btn    
        student_image_btn.background_normal = 'student_images/0000%d.jpg' % current_student
    
        sl = self.ids.studentname_label
         
        #'In School'   
        lbl = Label( text = 'In School')
        btn = Button(text = 'YES')
        
        details_grid.add_widget(lbl)
        details_grid.add_widget(btn)
        
        btn.bind(on_press=partial(self.changer2))

        #'In Class'   
        lbl = Label( text = 'In Class')
        btn = Button(text = 'NO')
        
        details_grid.add_widget(lbl)
        details_grid.add_widget(btn)
        
        btn.bind(on_press=partial(self.changer2))

        for i in [1,2,3]:
            txt ='Label'
            lbl = Label(text = txt)
            
            txt ='Info'
            btn = Button(text = txt)
            
            details_grid.add_widget(lbl)
            details_grid.add_widget(btn)

class DropdownButton(Button):
    id   = StringProperty('')
    image = StringProperty('')
    title = StringProperty('')
    label = StringProperty('')

class ScreenMain(Screen):
    settings_popup = ObjectProperty(None, allownone=True)
    top_layout     = ObjectProperty(None)
    main_btn       = ObjectProperty(None)
    dd_btn         = ObjectProperty(None)

    def __init__ (self,**kwargs):
        super (ScreenMain, self).__init__(**kwargs)
        Clock.schedule_once(self.prepare, 0)
        self.dropdown = DropDown()
  
    def prepare(self, *args):
        global user_id
        # if first time or loged out
        user_id = 0
        # call the login screen
        self.manager.current = 'ScreenLogin'

    def new_user(self):
        global user_name
        user_name = ""        
        if user_id > 0:
            user_name = "Andrew Watts" # fetch name for user_id
            first_id = self.add_classes()
            # need to get first list
            self.class_selected(first_id)
        else:
            self.manager.current = 'ScreenLogin'

    def add_classes(self):
        # sql  get classes for user
        # is user a from teacher ?
        # change spinner text & values
        sql = 'SELECT sg.id, s.name \
                FROM studygroups sg \
                JOIN subjects s ON (sg.subject_id = s.id) \
                WHERE sg.staff_id=%d \
                AND sg.schYr = %d' % (user_id, 2016)

        alchemysql = alchemy_text(sql)
        result = engine.execute(alchemysql)

        classes = [r for r in result]
        self.create_dropdown(classes)
        
        first_id   = classes[0][0]
        first_name = classes[0][1]
 
        ddbtn = self.ids.btn_ddID
        ddbtn.text = str(first_name)
        
        return first_id

    def create_dropdown(self, groups):
        self.dropdown.clear_widgets()
        for group in groups:
            # create button
            btn = self.create_button(group)
            # add it the dropdown
            self.dropdown.add_widget(btn)

    def create_button(self, group):
        gid, name = group
        
        # specify the height so the dropdown can calculate the area it needs.
        # store the class id in the buttons name
        btn = Button(text= name, size_hint_y=None, height=40, name=str(gid))
        
        # attach a callback that will call the select() method on the dropdown.
        # pass the button text as the data of the selection.
        btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
        
        # the call to update student list when button pressed
        btn.bind(on_release=partial(self.class_selected, gid))
        return btn

    def class_selected(self, *args ):
        class_id = args[0]

        student_list_widget = self.ids.student_list
        student_list_widget.clear_widgets()

        if not class_id: return
        
        sql = 'SELECT s.id, s.name \
                 FROM students_by_studygroup ss \
                 JOIN students s ON (ss.student_id = s.id) \
                 WHERE ss.studygroup_id=%d ' % (class_id,)
        alchemysql = alchemy_text(sql)
        result = engine.execute(alchemysql)
        # convert to a python list
        students = [r for r in result]
        self.add_students(students)

    def drop_down(self, x=''):
        # open the dropdown buttons
        self.dropdown.open(x)
        # set mainbutton text to select item
        self.dropdown.bind(on_select=lambda instance, y: setattr(x, 'text', y))

    def changer2(self, result, *args):
        global student_id
        student_id = args[0]
        self.manager.get_screen('ScreenStudentDetails').update(result)
        self.manager.current = 'ScreenStudentDetails'        
        
    def add_students(self, lst):
        student_list_widget = self.ids.student_list
        for item in lst:            
            btn = self.build_student_button(item)
            student_list_widget.add_widget(btn)
            sid = item[0]
            btn.bind(on_press=partial(self.changer2, sid))
        student_list_widget.bind(minimum_height=student_list_widget.setter('height'))
    
    def build_student_button(self, item):
        image_file = "student_images/0000%d.jpg" % item[0]
        btn = StudentListItemButton(
                wid = str(item[0]), 
              image = image_file, 
              title = item[1], 
              label = item[1]
            )
        btn.size_hint=(1, None)
        btn.height = 42
        return btn

class xx4_testApp(App):
    def build(self):
        self.my_screenmanager = ScreenManager()
        
        screenMain   = ScreenMain(  name='ScreenMain')
        screenLogin  = ScreenLogin( name='ScreenLogin')
        screenAttend = ScreenAttend(name='ScreenAttend') 
        screenAction = ScreenAction(name='ScreenAction')
        screenStudentDetails = ScreenStudentDetails(name='ScreenStudentDetails')
        screenNote= ScreenNote(name='ScreenNote')
        screenTag = ScreenTag(name='ScreenTag')
        screenFileChooser = ScreenFileChooser(name='ScreenFileChooser')
   
               
        self.my_screenmanager.add_widget(screenMain)
        self.my_screenmanager.add_widget(screenLogin)
        self.my_screenmanager.add_widget(screenStudentDetails)
        self.my_screenmanager.add_widget(screenAction)
        self.my_screenmanager.add_widget(screenAttend)
        self.my_screenmanager.add_widget(screenTag)
        self.my_screenmanager.add_widget(screenNote)
        self.my_screenmanager.add_widget(screenFileChooser)
        return self.my_screenmanager

if __name__ == '__main__':
    app=xx4_testApp()
    app.run()
