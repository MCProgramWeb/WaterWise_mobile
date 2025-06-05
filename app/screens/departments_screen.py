from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from app.data_manager import cargar_datos, guardar_datos, DEPARTAMENTOS_PATH

class DepartmentsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idioma = "es"
        self.departamentos = cargar_datos(DEPARTAMENTOS_PATH)
        self.titulos = {
            "es": "Departamentos",
            "en": "Departments",
            "fr": "Départements"
        }
        self.textos = {
            "nombre": {"es": "Nombre", "en": "Name", "fr": "Nom"},
            "numero": {"es": "Número", "en": "Number", "fr": "Numéro"},
            "agregar": {"es": "Agregar", "en": "Add", "fr": "Ajouter"},
            "eliminar": {"es": "Eliminar", "en": "Delete", "fr": "Supprimer"},
            "volver": {"es": "Volver", "en": "Back", "fr": "Retour"},
            "cambiar_idioma": {"es": "Cambiar idioma", "en": "Change language", "fr": "Changer de langue"},
        }
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=[20, 40, 20, 20])
        main_layout.add_widget(Label(
            text=self.titulos[self.idioma],
            font_size=30, bold=True, color=(0.1,0.4,0.7,1),
            size_hint=(1, None), height=60
        ))
        self.input_nombre = TextInput(hint_text=self.textos["nombre"][self.idioma], size_hint=(1, None), height=50, font_size=20)
        self.input_numero = TextInput(hint_text=self.textos["numero"][self.idioma], size_hint=(1, None), height=50, font_size=20)
        main_layout.add_widget(self.input_nombre)
        main_layout.add_widget(self.input_numero)
        btn_style = {"size_hint": (1, None), "height": 55, "background_color": (0.2,0.6,1,1), "color": (1,1,1,1), "font_size": 20}
        main_layout.add_widget(Button(text=self.textos["agregar"][self.idioma], on_release=self.agregar_departamento, **btn_style))
        main_layout.add_widget(Button(text=self.textos["cambiar_idioma"][self.idioma], on_release=self.cambiar_idioma, **btn_style))
        main_layout.add_widget(Button(text=self.textos["volver"][self.idioma], on_release=self.volver, **btn_style))
        scroll = ScrollView(size_hint=(1, 1))
        self.list_layout = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll.add_widget(self.list_layout)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
        self.actualizar_lista()

    def actualizar_lista(self):
        self.list_layout.clear_widgets()
        for dept in self.departamentos:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=5)
            row.add_widget(Label(text=f"{dept.get('numero', '')} - {dept.get('nombre', '')}", font_size=18, size_hint_x=0.8))
            btn = Button(text=self.textos["eliminar"][self.idioma], size_hint_x=0.2, background_color=(1,0.3,0.3,1), color=(1,1,1,1), font_size=16)
            btn.bind(on_release=lambda inst, d=dept: self.eliminar_departamento(d))
            row.add_widget(btn)
            self.list_layout.add_widget(row)

    def agregar_departamento(self, instance):
        nombre = self.input_nombre.text.strip()
        numero = self.input_numero.text.strip()
        if nombre and numero:
            nuevo = {
                "id": str(len(self.departamentos) + 1),
                "nombre": nombre,
                "numero": numero,
                "fecha_registro": ""
            }
            self.departamentos.append(nuevo)
            guardar_datos(self.departamentos, DEPARTAMENTOS_PATH)
            self.input_nombre.text = ""
            self.input_numero.text = ""
            self.actualizar_lista()

    def eliminar_departamento(self, dept):
        self.departamentos = [d for d in self.departamentos if d["id"] != dept["id"]]
        guardar_datos(self.departamentos, DEPARTAMENTOS_PATH)
        self.actualizar_lista()

    def cambiar_idioma(self, instance):
        if self.idioma == "es":
            self.idioma = "en"
        elif self.idioma == "en":
            self.idioma = "fr"
        else:
            self.idioma = "es"
        self.clear_widgets()
        self.__init__()

    def volver(self, instance):
        self.manager.current = 'home'
