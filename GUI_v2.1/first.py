from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
import os
import time
import cv2
from kivy.clock import Clock
from kivy.config import Config
from datetime import datetime
from datetime import timedelta
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.camera import Camera
from kivy.uix.video import Video
from kivy.graphics.texture import Texture
from kivy.uix.popup import Popup
from kivy.uix.videoplayer import VideoPlayer


t = StringProperty()
class P(Popup):
    def next_check(self,*arg):
        self.ques = self.ids['ques']
        self.ques.text = "Do you have any big luggage ?"
    
    def small_articles(self,*arg):
        #pop_up = self.ids['pop']
        #pop_up.dismiss()
        #pop_up.dismiss()
        print('hello')
        #self.secondwindow = SecondWindow()
        #temp=SecondWindow()
        #temp.small_articles_in()
        #temp.smallarticles= SecondWindow.ids['instruction']
        #SecondWindow.instruction.text = "Put your valuables into box1"
        #SecondWindow.instruction.color = 1,1,1,1
        #Clock.schedule_once(SecondWindow.small_articles_in)
    
    
    pass



class LogoWindow(Screen):
    pass

class MainWindow(Screen):
    time = ObjectProperty(None)
    def on_enter(self):
    #t = StringProperty()
        #self.main_window = MainWindow()
        Clock.schedule_once(go_to1,10)
        os.system('echo "welcome to icapotech!" | festival --tts')
        Clock.schedule_interval(self.update1, 1)
        pass
    
    def update1(self,*arg):
        time = datetime.now()
        self.label1 = self.ids['time1']
        self.label1.text = "Time: " + time.strftime('%H:%M:%S')
        self.label2 = self.ids['time2']
        self.label2.text = "Date: " + time.strftime('%m/%d/%Y')
        



class SecondWindow(Screen):
    time = ObjectProperty(None)
    
    def on_enter(self):
    #t = StringProperty()
        #---------------------below lines to be uncommented for live video
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update1, 1.0/33.0)
        Clock.schedule_once(self.mask_status,10)
        pass
    
    def small_articles_in(self,*arg):
        #pop_up = self.ids['pop']
        #pop_up.dismiss()
        #pop_up.dismiss()
        print('hello')
        instruction= self.ids['instruction']
        instruction.text = "Put your valuables into box"
        instruction.color = 0,0,0,1
        #Clock.schedule_once(P.next_check, 10)
        Clock.schedule_once(self.sanitize,15)
        
    def mask_status(self,*arg):
        self.instruction = self.ids['instruction']
        self.instruction.text = "Mask Detected"
        self.instruction.color = 0,0,1,1
        Clock.schedule_once(self.body_temp,2)
        
    def body_temp(self,*arg):
        self.opmsg = self.ids['opmsg']
        self.opmsg.text = "Body Temperature: 37 deg Celcius"
        self.opmsg.color = 0,1,0,1
        Clock.schedule_once(self.popwindow,5)
        Clock.schedule_once(self.small_articles_in,10)
    
    def sanitize(self,*arg):
        #self.sanitize_window = SecondWindow()
        #self.instruction = self.ids['instruction']
        #self.instruction.text = "Mask Detected"
        #self.instruction.color = 0,1,0,1
        self.opmsg = self.ids['opmsg']
        self.opmsg.text = "Sanitize your hands in Hand Sanitization Chamber"
        self.opmsg.color = 1,1,1,1
        Clock.schedule_once(go_to2, 10)
    
    def popwindow(self,*arg):
        show_popup()
    
    #def btn(self):
        #show_popup()
    def update1(self,*arg):
        time = datetime.now()
        self.label1 = self.ids['time_sec1']
        self.label1.text = "Time: " + time.strftime('%H:%M:%S')
        self.label2 = self.ids['time_sec2']
        self.label2.text = "Date:" + time.strftime('%m/%d/%Y')
        #----------------------------once you get camera uncomment below lines
        self.Image=self.ids['cam']
        ret, frame = self.capture.read()
        cv2.imshow("CV2 Image", frame)
        width = frame.shape[1]+300 # keep original width
        height = 700
        dim = (width, height)
        
 
# resize image
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.Image.texture = texture1
        #----------------------------------

class ThirdWindow(Screen):

    def on_enter(self):
    #t = StringProperty()
        #self.main_window = MainWindow()
        #Clock.unschedule(self.update2)
        cv2.destroyAllWindows()
        self.capture = cv2.VideoCapture('/home/pi/Load_screen_.mp4')
        cv2.namedWindow("CV2 Image")
        Clock.schedule_once(self.second_last,20)
        #Clock.schedule_once(self.play_vid)
        #os.system('echo "welcome to icapotech!" | festival --tts')
        Clock.schedule_interval(self.update2, 1.0/1000000.0)
        Clock.schedule_interval(self.update1, 1)
        pass
    #def play_vid(self,*arg):
     #   self.player= Video(source='/home/pi/test.mp4',  state='play', options={'allow_stretch': True})
        #return self.player
    def update1(self,*arg):
        time = datetime.now()
        self.label1 = self.ids['time1']
        self.label1.text = "Time: "+ time.strftime('%H:%M:%S')
        self.label2 = self.ids['time2']
        self.label2.text = "Date: " + time.strftime('%m/%d/%Y')
    def update2(self,*arg):
        self.Image=self.ids['cam1']
        ret, frame = self.capture.read()
        cv2.imshow("CV2 Image", frame)
        width = frame.shape[1]+300 # keep original width
        height = 700
        dim = (width, height)
        
 
# resize image
        frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
        # convert it to texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        # display image from the texture
        self.Image.texture = texture1
        
    def second_last(self, *arg):
        Clock.unschedule(self.update2)
        cv2.destroyAllWindows()
        greeting = self.ids['cam1']
        #greeting.text = "Sanitization Done !!! \n .................. \n Pick up your goods & \n Wave over the box \n to close it"
        greeting.source = '/home/pi/sanit.jpg'
        #greeting.texture = None
        Clock.schedule_once(self.thank_you,7)
    
    def thank_you(self, *arg):
        
        #self.bac_im = self.ids['cand']
        #self.bac_im.color.rgba = 0.2,0.6,1,1
        greeting = self.ids['cam1']
        #greeting.text = "Thank you \n for your Cooperation"
        greeting.source = '/home/pi/Thank.jpg'
        #greeting.texture = None
        #Clock.schedule_once(reset_all,15)


kv = Builder.load_file("my.kv")

#Builder.load_file("status.kv")

sm = ScreenManager(transition=FadeTransition())
sm.add_widget(LogoWindow(name='logo'))
sm.add_widget(MainWindow(name='main'))
sm.add_widget(SecondWindow(name='second'))
sm.add_widget(ThirdWindow(name='third'))
def go_to(self):
    sm.current = 'main'

def go_to1(self):
    sm.current = 'second'

def go_to2(self):
    sm.current = 'third'



    


clock = Clock.schedule_once(go_to,15)

    

class MyMainApp(App):
    
    def __init__(self,**kwargs):
        super(MyMainApp,self).__init__(**kwargs)
        
    def update(self, *args):
        time = datetime.now()
        #label1 = self.main_window.ids['time']
        #lbl1.text = str(time)
        
        
        
    def build(self):
        #Window.clearcolor = (1,1,1,1)
        #Config.set('graphics','KIVY_CLOCK','interrupt')
        #Config.write()
        
        #Clock.schedule_interval(updateTime,1)
        #self.load_kv('my.kv')
        #Clock.schedule_interval(self.update, 1)
        return sm

def show_popup():
    popupWindow = P()
    #popupWindow = Popup(title = "Popup Window", content = show, size_hint = (None,None), size = (400,400))
    popupWindow.open()
    

if __name__ == "__main__":
    MyMainApp().run()