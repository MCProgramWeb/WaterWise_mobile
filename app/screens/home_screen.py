from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idioma = "es"
        self.titulos = {
            "es": "WaterWise Mobile",
            "en": "WaterWise Mobile",
            "fr": "WaterWise Mobile"
        }
        self.textos = {
            "departamentos": {"es": "Departamentos", "en": "Departments", "fr": "Départements"},
            "lecturas": {"es": "Lecturas", "en": "Readings", "fr": "Relevés"},
            "deudas": {"es": "Deudas", "en": "Debts", "fr": "Dettes"},
            "recibos": {"es": "Recibos", "en": "Receipts", "fr": "Reçus"},
            "reportes": {"es": "Reportes", "en": "Reports", "fr": "Rapports"},
            "cambiar_idioma": {"es": "Cambiar idioma", "en": "Change language", "fr": "Changer de langue"},
        }
        scroll = ScrollView(size_hint=(1, 1))
        layout = BoxLayout(orientation='vertical', spacing=30, padding=[30, 60, 30, 60], size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))
        layout.add_widget(Label(text=self.titulos[self.idioma], font_size=38, bold=True, color=(0.1,0.4,0.7,1), size_hint=(1, None), height=80))
        btn_style = {"size_hint": (1, None), "height": 70, "background_color": (0.2,0.6,1,1), "color": (1,1,1,1), "font_size": 24}
        layout.add_widget(Button(text=self.textos["departamentos"][self.idioma], on_release=self.go_departments, **btn_style))
        layout.add_widget(Button(text=self.textos["lecturas"][self.idioma], on_release=self.go_lecturas, **btn_style))
        layout.add_widget(Button(text=self.textos["deudas"][self.idioma], on_release=self.go_deudas, **btn_style))
        layout.add_widget(Button(text=self.textos["recibos"][self.idioma], on_release=self.go_recibos, **btn_style))
        layout.add_widget(Button(text=self.textos["reportes"][self.idioma], on_release=self.go_reportes, **btn_style))
        layout.add_widget(Button(text=self.textos["cambiar_idioma"][self.idioma], on_release=self.cambiar_idioma, **btn_style))
        scroll.add_widget(layout)
        self.add_widget(scroll)

    def cambiar_idioma(self, instance):
        if self.idioma == "es":
            self.idioma = "en"
        elif self.idioma == "en":
            self.idioma = "fr"
        else:
            self.idioma = "es"
        self.clear_widgets()
        self.__init__()

    # Puedes pasar el idioma a otras pantallas al navegar:
    def go_departments(self, instance):
        self.manager.get_screen('departments').idioma = self.idioma
        self.manager.get_screen('departments').clear_widgets()
        self.manager.get_screen('departments').__init__()
        self.manager.current = 'departments'

    def go_lecturas(self, instance):
        self.manager.get_screen('lecturas').idioma = self.idioma
        self.manager.get_screen('lecturas').clear_widgets()
        self.manager.get_screen('lecturas').__init__()
        self.manager.current = 'lecturas'

    def go_deudas(self, instance):
        self.manager.get_screen('deudas').idioma = self.idioma
        self.manager.get_screen('deudas').clear_widgets()
        self.manager.get_screen('deudas').__init__()
        self.manager.current = 'deudas'

    def go_recibos(self, instance):
        self.manager.get_screen('recibos').idioma = self.idioma
        self.manager.get_screen('recibos').clear_widgets()
        self.manager.get_screen('recibos').__init__()
        self.manager.current = 'recibos'

    def go_reportes(self, instance):
        self.manager.get_screen('reportes').idioma = self.idioma
        self.manager.get_screen('reportes').clear_widgets()
        self.manager.get_screen('reportes').__init__()
        self.manager.current = 'reportes'
