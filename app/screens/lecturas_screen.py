from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from app.data_manager import cargar_datos, guardar_datos, HISTORIAL_LECTURAS_PATH, DEPARTAMENTOS_PATH
from datetime import datetime

class LecturasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idioma = "es"
        self.lecturas = cargar_datos(HISTORIAL_LECTURAS_PATH)
        self.departamentos = cargar_datos(DEPARTAMENTOS_PATH)
        self.titulos = {
            "es": "Registro de Lecturas",
            "en": "Readings Log",
            "fr": "Journal des Relevés"
        }
        self.textos = {
            "id_depto": {"es": "ID Departamento", "en": "Department ID", "fr": "ID Département"},
            "lectura_ant": {"es": "Lectura Anterior", "en": "Previous Reading", "fr": "Relevé Précédent"},
            "lectura_act": {"es": "Lectura Actual", "en": "Current Reading", "fr": "Relevé Actuel"},
            "comentario": {"es": "Comentario", "en": "Comment", "fr": "Commentaire"},
            "registrar": {"es": "Registrar", "en": "Register", "fr": "Enregistrer"},
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
        self.input_depto = TextInput(hint_text=self.textos["id_depto"][self.idioma], size_hint=(1, None), height=50, font_size=20)
        self.input_ant = TextInput(hint_text=self.textos["lectura_ant"][self.idioma], size_hint=(1, None), height=50, font_size=20, input_filter='float')
        self.input_act = TextInput(hint_text=self.textos["lectura_act"][self.idioma], size_hint=(1, None), height=50, font_size=20, input_filter='float')
        self.input_comentario = TextInput(hint_text=self.textos["comentario"][self.idioma], size_hint=(1, None), height=50, font_size=20)
        main_layout.add_widget(self.input_depto)
        main_layout.add_widget(self.input_ant)
        main_layout.add_widget(self.input_act)
        main_layout.add_widget(self.input_comentario)
        btn_style = {"size_hint": (1, None), "height": 55, "background_color": (0.2,0.6,1,1), "color": (1,1,1,1), "font_size": 20}
        main_layout.add_widget(Button(text=self.textos["registrar"][self.idioma], on_release=self.registrar_lectura, **btn_style))
        main_layout.add_widget(Button(text=self.textos["cambiar_idioma"][self.idioma], on_release=self.cambiar_idioma, **btn_style))
        main_layout.add_widget(Button(text=self.textos["volver"][self.idioma], on_release=self.volver, **btn_style))
        scroll = ScrollView(size_hint=(1, 1))
        self.historial_box = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.historial_box.bind(minimum_height=self.historial_box.setter('height'))
        scroll.add_widget(self.historial_box)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
        self.actualizar_historial()

    def actualizar_historial(self):
        self.historial_box.clear_widgets()
        for l in reversed(self.lecturas):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=5)
            row.add_widget(Label(text=f"Depto {l.get('departamento_id','')} | {l.get('fecha_lectura','')}", font_size=16, size_hint_x=0.5))
            row.add_widget(Label(text=f"{l.get('lectura_anterior',0)}→{l.get('lectura_actual',0)}", font_size=16, size_hint_x=0.3))
            row.add_widget(Button(text=self.textos["eliminar"][self.idioma], size_hint_x=0.2, background_color=(1,0.3,0.3,1), color=(1,1,1,1), font_size=14, on_release=lambda inst, lid=l['id']: self.eliminar_lectura(lid)))
            self.historial_box.add_widget(row)

    def registrar_lectura(self, instance):
        depto_id = self.input_depto.text.strip()
        ant = self.input_ant.text.strip()
        act = self.input_act.text.strip()
        comentario = self.input_comentario.text.strip()
        if depto_id and ant and act:
            try:
                ant_val = float(ant)
                act_val = float(act)
                if act_val < ant_val:
                    return
                lectura = {
                    "id": str(len(self.lecturas) + 1),
                    "departamento_id": depto_id,
                    "lectura_anterior": ant_val,
                    "lectura_actual": act_val,
                    "consumo_departamento": round(act_val - ant_val, 2),
                    "fecha_lectura": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "comentario": comentario
                }
                self.lecturas.append(lectura)
                guardar_datos(self.lecturas, HISTORIAL_LECTURAS_PATH)
                self.input_depto.text = ""
                self.input_ant.text = ""
                self.input_act.text = ""
                self.input_comentario.text = ""
                self.actualizar_historial()
            except Exception:
                pass

    def eliminar_lectura(self, lectura_id):
        self.lecturas = [l for l in self.lecturas if l["id"] != lectura_id]
        guardar_datos(self.lecturas, HISTORIAL_LECTURAS_PATH)
        self.actualizar_historial()

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
