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
from utilidades.cuenta_manager import AccountManager

#posibles librerias para ver si funciona
import storj
import json

class MenuPrincipal(Screen):
    pass




class MenuRegistro(Screen):
    pass

    def my_callback(self,dt):
        self.manager.current = 'menu_ingresar'
        self.limpiarpantalla()

    def limpiarpantalla(self):
        print "limpie pantalla"
        self.correo = self.ids['correo']
        self.pass1 = self.ids['contra']
        self.repass1 = self.ids['recontra']
        self.mensaje = self.ids['mensaje_registro']
        self.mensaje.text=""
        self.correo.text=""
        self.pass1.text=""
        self.repass1.text=""


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

    def my_callback(self,dt):
        self.manager.current = 'menu_final'
        self.limpiarpantalla()

    def limpiarpantalla(self):
        print "limpie pantalla"
        self.correo = self.ids['correo']
        self.pass1 = self.ids['contra']
        self.mensaje = self.ids['mensaje_registro']
        self.mensaje.text=""
        self.correo.text=""
        self.pass1.text=""

    def Ingresar(self):
        self.correo = self.ids['correo']
        self.email = self.correo.text
        self.pass1 = self.ids['contra']
        self.password = self.pass1.text
        self.mensaje = self.ids['mensaje_registro']
        self.storj_client = storj.Client(email= self.email, password=self.password)
        success = False

        try:
            self.storj_client.key_list()
            success = True
        except storj.exception.StorjBridgeApiError as gato:
            j = json.loads(str(gato))
#            self.__logger.debug(j)
            if j[0]['error']=='Invalid email or password':
                self.mensaje.text= "Invalido correo o contrasena Porfavor de Verificarlos"
            else:
                self.mensaje.text=str(gato)
        if success == True:
            print "guardando credinciales"
            self.account_manager = AccountManager(self.email, self.password)
            self.account_manager.save_account_credentials()
            self.mensaje.text = "Ingreso Exitoso"
            event = Clock.schedule_once(self.my_callback,7)

class MenuFinal(Screen):
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
