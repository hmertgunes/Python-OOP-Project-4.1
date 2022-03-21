from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import time
import webbrowser
from FileSharer import FileSharer
from kivy.core.clipboard import Clipboard

Builder.load_string("""
<CameraScreen>:
    GridLayout:
        cols:1
        padding: 10
        spacing: 10
        Camera:
            resolution: (1280, 1024)
            size_hint_y: 0.8
            play: False
            id: camera
            opacity: 0
        Button:
            size_hint_y: 0.1
            id: button
            text: "Start Camera"
            background_down: "images/down.png"
            background_normal:"images/normal.png"
            on_press: root.start() if root.ids.camera.play == False else root.stop()
        Button:
            size_hint_y: 0.1
            text: "Capture"  
            background_down: "images/down.png"
            background_normal:"images/normal.png"
            on_press: root.capture() 
            
<ImageScreen>:
    GridLayout:
        padding:10
        spacing:10
        cols:1
        Image:
            id: img
            size_hint_y: 0.8
        Button:
            text: "Create Shareable Link"
            size_hint_y: 0.05
            background_down: "images/down.png"
            background_normal:"images/normal.png"
            on_press: root.create_link()
        Label:
            id: label
            text:
            size_hint_y: 0.05
            color: (1,1,1,1)
            
        GridLayout:
            size_hint_y: 0.1
            cols:2
            Button:
                text: "Copy"
                size_hint_x: 0.5
                on_press: root.copy()
                background_down: "images/down.png"
                background_normal:"images/normal.png"
            Button:
                text: "Open"
                size_hint_x: 0.5
                on_press: root.open()
                background_down: "images/down.png"
                background_normal:"images/normal.png"
<RootWidget>:
    canvas.before:
        Color:
            rgba: (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size      
    CameraScreen:
        id: camera_screen
        name: "camera_screen"
        
    ImageScreen:
        id: image_screen
        name: "image_screen"    
""")


class CameraScreen(Screen):

    def start(self):
        self.ids.camera.play = True
        self.ids.button.text = "Stop Camera"
        self.ids.camera.opacity = 1

    def stop(self):
        self.ids.camera.play = False
        self.ids.button.text = "Start Camera"
        self.ids.camera.texture = None
        self.ids.camera.opacity = 0

    def capture(self):
        current_time = time.strftime("%Y%m%d_%H%M%S")
        self.name = "files/" + current_time + ".png"
        self.ids.camera.export_to_png(self.name)
        print("Captured.")
        self.manager.current = "image_screen"
        self.manager.current_screen.ids.img.source = self.name


class ImageScreen(Screen):

    def create_link(self):
        filepath = App.get_running_app().root.ids.camera_screen.name
        filesharer = FileSharer(filepath=filepath)
        self.url = filesharer.share()
        self.ids.label.text = self.url

    def copy(self):
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.label.text = "Firstly, create a link!"

    def open(self):
        try:
            webbrowser.open(self.url, new=2)
        except:
            self.ids.label.text = "Firstly, create a link!"


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()
