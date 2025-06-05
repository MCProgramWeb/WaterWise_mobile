from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from app.data_manager import cargar_datos, HISTORIAL_LECTURAS_PATH
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from app.utils.export_utils import exportar_reporte_pdf, exportar_grafico_consumo
import os
from kivy.uix.spinner import Spinner
from plyer import notification
from app.data_manager import registrar_log_detallado

class ReportsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idioma = "es"
        self.lecturas = cargar_datos(HISTORIAL_LECTURAS_PATH)
        self.departamentos = list({l.get('departamento_id','') for l in self.lecturas if l.get('departamento_id','')})
        self.titulos = {
            "es": "Reporte de Consumo",
            "en": "Consumption Report",
            "fr": "Rapport de Consommation"
        }
        self.textos = {
            "todos": {"es": "Todos", "en": "All", "fr": "Tous"},
            "actualizar": {"es": "Actualizar", "en": "Refresh", "fr": "Actualiser"},
            "exportar_pdf": {"es": "Exportar PDF", "en": "Export PDF", "fr": "Exporter PDF"},
            "exportar_img": {"es": "Exportar Imagen", "en": "Export Image", "fr": "Exporter Image"},
            "ver_grafico": {"es": "Ver Gráfico", "en": "View Chart", "fr": "Voir Graphique"},
            "cambiar_idioma": {"es": "Cambiar idioma", "en": "Change language", "fr": "Changer de langue"},
            "volver": {"es": "Volver", "en": "Back", "fr": "Retour"},
            "total": {"es": "Consumo total registrado: ", "en": "Total consumption: ", "fr": "Consommation totale : "},
            "reporte_actualizado": {"es": "Reporte actualizado", "en": "Report updated", "fr": "Rapport mis à jour"},
            "filtro": {"es": "Filtro", "en": "Filter", "fr": "Filtre"},
            "pdf_exportado": {"es": "PDF exportado", "en": "PDF exported", "fr": "PDF exporté"},
            "archivo_guardado": {"es": "Archivo guardado en:\n", "en": "File saved at:\n", "fr": "Fichier enregistré à :\n"},
            "error_pdf": {"es": "No se pudo exportar el PDF.", "en": "Could not export PDF.", "fr": "Impossible d'exporter le PDF."},
            "img_exportada": {"es": "Imagen exportada", "en": "Image exported", "fr": "Image exportée"},
            "error_img": {"es": "No se pudo exportar la imagen.", "en": "Could not export image.", "fr": "Impossible d'exporter l'image."},
            "error_grafico": {"es": "No se pudo generar el gráfico.", "en": "Could not generate chart.", "fr": "Impossible de générer le graphique."},
            "cerrar": {"es": "Cerrar", "en": "Close", "fr": "Fermer"},
        }
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=[20, 40, 20, 20])
        main_layout.add_widget(Label(
            text=self.titulos[self.idioma],
            font_size=30, bold=True, color=(0.1,0.4,0.7,1),
            size_hint=(1, None), height=60
        ))
        self.total_label = Label(
            text="", font_size=20, color=(0.2,0.6,1,1),
            size_hint=(1, None), height=40
        )
        main_layout.add_widget(self.total_label)
        # Filtro avanzado por departamento
        self.spinner = Spinner(
            text=self.textos["todos"][self.idioma],
            values=[self.textos["todos"][self.idioma]] + self.departamentos,
            size_hint=(1, None), height=50, font_size=18
        )
        self.spinner.bind(text=self.on_spinner_select)
        main_layout.add_widget(self.spinner)
        btn_style = {
            "size_hint": (1, None), "height": 55,
            "background_color": (0.2,0.6,1,1),
            "color": (1,1,1,1), "font_size": 20
        }
        main_layout.add_widget(Button(text=self.textos["actualizar"][self.idioma], on_release=lambda x: self.actualizar_reporte(), **btn_style))
        main_layout.add_widget(Button(text=self.textos["exportar_pdf"][self.idioma], on_release=self.exportar_pdf, **btn_style))
        main_layout.add_widget(Button(text=self.textos["exportar_img"][self.idioma], on_release=self.exportar_imagen, **btn_style))
        main_layout.add_widget(Button(text=self.textos["ver_grafico"][self.idioma], on_release=self.ver_grafico, **btn_style))
        main_layout.add_widget(Button(text=self.textos["cambiar_idioma"][self.idioma], on_release=self.cambiar_idioma, **btn_style))
        main_layout.add_widget(Button(text=self.textos["volver"][self.idioma], on_release=self.volver, **btn_style))
        scroll = ScrollView(size_hint=(1, 1))
        self.report_box = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.report_box.bind(minimum_height=self.report_box.setter('height'))
        scroll.add_widget(self.report_box)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
        self.actualizar_reporte()

    def on_spinner_select(self, spinner, value):
        self.actualizar_reporte()

    def actualizar_reporte(self):
        """Actualiza el reporte de consumo cargando los datos más recientes."""
        self.lecturas = cargar_datos(HISTORIAL_LECTURAS_PATH)
        self.report_box.clear_widgets()
        total_consumo = 0
        filtro = self.spinner.text
        for l in reversed(self.lecturas):
            if filtro not in (self.textos["todos"]["es"], self.textos["todos"]["en"], self.textos["todos"]["fr"]) and l.get('departamento_id','') != filtro:
                continue
            consumo = l.get('consumo_departamento', 0)
            total_consumo += consumo
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            row.add_widget(Label(text=f"Depto {l.get('departamento_id','')} | {l.get('fecha_lectura','')}", size_hint_x=0.5))
            row.add_widget(Label(text=f"Consumo: {consumo}", size_hint_x=0.5))
            self.report_box.add_widget(row)
        self.total_label.text = self.textos["total"][self.idioma] + str(total_consumo)
        registrar_log_detallado(self.textos["reporte_actualizado"][self.idioma], f"{self.textos['filtro'][self.idioma]}: {filtro}", self.idioma)
        notification.notify(
            title=self.textos["reporte_actualizado"][self.idioma],
            message=f"{self.textos['filtro'][self.idioma]}: {filtro}"
        )

    def exportar_pdf(self, instance):
        """Exporta el reporte de consumo a un archivo PDF."""
        ruta = os.path.join(os.path.expanduser("~"), "reporte_consumo.pdf")
        if exportar_reporte_pdf(ruta, self.lecturas):
            self.mostrar_popup(self.textos["pdf_exportado"][self.idioma], self.textos["archivo_guardado"][self.idioma] + ruta)
        else:
            self.mostrar_popup("Error", self.textos["error_pdf"][self.idioma])

    def exportar_imagen(self, instance):
        """Exporta el gráfico de consumo a un archivo de imagen."""
        ruta = os.path.join(os.path.expanduser("~"), "grafico_consumo.png")
        if exportar_grafico_consumo(ruta, self.lecturas):
            self.mostrar_popup(self.textos["img_exportada"][self.idioma], self.textos["archivo_guardado"][self.idioma] + ruta)
        else:
            self.mostrar_popup("Error", self.textos["error_img"][self.idioma])

    def ver_grafico(self, instance):
        """Muestra el gráfico de consumo en un popup."""
        ruta = os.path.join(os.path.expanduser("~"), "grafico_consumo.png")
        if exportar_grafico_consumo(ruta, self.lecturas) and os.path.exists(ruta):
            popup = Popup(title=self.textos["ver_grafico"][self.idioma], size_hint=(0.95, 0.8))
            img = Image(source=ruta, allow_stretch=True, keep_ratio=True)
            popup.add_widget(img)
            popup.open()
        else:
            self.mostrar_popup("Error", self.textos["error_grafico"][self.idioma])

    def mostrar_popup(self, titulo, mensaje):
        """Muestra un popup con un mensaje."""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)
        content.add_widget(Label(text=mensaje, font_size=18))
        btn = Button(text=self.textos["cerrar"][self.idioma], size_hint=(1, 0.3))
        popup = Popup(title=titulo, content=content, size_hint=(0.8, 0.4))
        btn.bind(on_release=popup.dismiss)
        content.add_widget(btn)
        popup.open()

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
        """Vuelve a la pantalla anterior."""
        self.manager.current = 'home'
