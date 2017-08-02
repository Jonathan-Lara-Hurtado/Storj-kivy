import kivy
kivy.require('1.9.0')

#librerias de kivy aplicacion
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.vector import Vector
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock


#posibles librerias para ver si funciona
import storj
import json

class MenuPrincipal(Screen):
    pass



class MenuRegistro(Screen):
    pass

    def my_callback(self,dt):
        self.manager.current = 'menu_ingresar'

    def registro(self):
        self.correo = self.ids['correo']
        self.email = self.correo.text
        self.pass1 = self.ids['contra']
        self.password = self.pass1.text
        self.repass1 = self.ids['recontra']
        self.password_repeat = self.repass1.text
        self.mensaje = self.ids['mensaje_registro']
        self.bridge_api_url= 'https://api.storj.io/'
        success = False
        if self.email != "" and self.password != "" and self.password_repeat != "":
            if self.password == self.password_repeat:
                try:
                    self.storj_client = storj.Client(None, "",self.bridge_api_url).user_create(str(self.email),str(self.password))

                except storj.exception.StorjBridgeApiError as xavi:
                    j = json.loads(str(xavi))
                    if j[0]["error"] == "Email is already registered":
                        self.mensaje.text = "Se a creado con exito revisa tu correo para confirmar tu cuenta"
                        success = True
                    else:
                        self.mensaje.text= str(xavi)
            else:
                    self.mensaje.text ="Las contrasenas son diferentes reviselas Porfavor"
        else:
                self.mensaje.text ="Porfavor rellene todos los campos"
        if success == True:
            event = Clock.schedule_once(self.my_callback,7)

class MenuIngresar(Screen):
    pass

class Menufinal(Screen):
    pass


class Manager(ScreenManager):

    menuprincipal = ObjectProperty(None)
    menuregistro = ObjectProperty(None)
    menuingresar = ObjectProperty(None)
    menufinal = ObjectProperty(None)



class StorjApp(App):
    title = "Storj"
    def build(self):
        return Manager()

if __name__ in "__main__":
    StorjApp().run()
