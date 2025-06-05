from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from app.data_manager import cargar_datos, guardar_datos, DEUDAS_PATH
from datetime import datetime

class DebtScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idioma = "es"
        self.deudas = cargar_datos(DEUDAS_PATH)
        self.titulos = {
            "es": "Gestión de Deudas",
            "en": "Debt Management",
            "fr": "Gestion des Dettes"
        }
        self.textos = {
            "id_deuda": {"es": "ID Deuda", "en": "Debt ID", "fr": "ID Dette"},
            "monto_pago": {"es": "Monto Pago", "en": "Payment Amount", "fr": "Montant du Paiement"},
            "registrar_pago": {"es": "Registrar Pago", "en": "Register Payment", "fr": "Enregistrer Paiement"},
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
        self.input_deuda_id = TextInput(hint_text=self.textos["id_deuda"][self.idioma], size_hint=(1, None), height=50, font_size=20)
        self.input_pago = TextInput(hint_text=self.textos["monto_pago"][self.idioma], size_hint=(1, None), height=50, font_size=20, input_filter='float')
        main_layout.add_widget(self.input_deuda_id)
        main_layout.add_widget(self.input_pago)
        btn_style = {"size_hint": (1, None), "height": 55, "background_color": (0.2,0.6,1,1), "color": (1,1,1,1), "font_size": 20}
        main_layout.add_widget(Button(text=self.textos["registrar_pago"][self.idioma], on_release=self.registrar_pago, **btn_style))
        main_layout.add_widget(Button(text=self.textos["cambiar_idioma"][self.idioma], on_release=self.cambiar_idioma, **btn_style))
        main_layout.add_widget(Button(text=self.textos["volver"][self.idioma], on_release=self.volver, **btn_style))
        scroll = ScrollView(size_hint=(1, 1))
        self.deuda_box = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.deuda_box.bind(minimum_height=self.deuda_box.setter('height'))
        scroll.add_widget(self.deuda_box)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
        self.actualizar_lista()

    def actualizar_lista(self):
        self.deuda_box.clear_widgets()
        for d in reversed(self.deudas):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=5)
            row.add_widget(Label(text=f"ID:{d.get('id','')} | Monto:{d.get('monto_total',0)} | Pagado:{d.get('pagado',0)} | Saldo:{d.get('saldo',0)}", font_size=16, size_hint_x=0.8))
            btn = Button(text=self.textos["eliminar"][self.idioma], size_hint_x=0.2, background_color=(1,0.3,0.3,1), color=(1,1,1,1), font_size=14)
            btn.bind(on_release=lambda inst, did=d['id']: self.eliminar_deuda(did))
            row.add_widget(btn)
            self.deuda_box.add_widget(row)

    def registrar_pago(self, instance):
        deuda_id = self.input_deuda_id.text.strip()
        monto_pago = self.input_pago.text.strip()
        if deuda_id and monto_pago:
            try:
                pago = float(monto_pago)
                for d in self.deudas:
                    if d["id"] == deuda_id and d.get("saldo", 0) > 0:
                        d["pagado"] = d.get("pagado", 0) + pago
                        d["saldo"] = max(0, d.get("monto_total", 0) - d["pagado"])
                        d["estado"] = "Pagada" if d["saldo"] <= 0.01 else "Pendiente"
                        if "pagos" not in d:
                            d["pagos"] = []
                        d["pagos"].append({
                            "id": str(len(d["pagos"]) + 1),
                            "monto_pago": pago,
                            "fecha_pago": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })
                        guardar_datos(self.deudas, DEUDAS_PATH)
                        break
                self.input_deuda_id.text = ""
                self.input_pago.text = ""
                self.actualizar_lista()
            except Exception:
                pass

    def eliminar_deuda(self, deuda_id):
        self.deudas = [d for d in self.deudas if d["id"] != deuda_id]
        guardar_datos(self.deudas, DEUDAS_PATH)
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
