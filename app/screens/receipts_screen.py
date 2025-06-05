from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.spinner import Spinner
from plyer import filechooser, camera, notification
from kivy.core.window import Window
from app.data_manager import cargar_datos, guardar_datos, RECEIPTS_METADATA_PATH, RECEIPTS_DIR, registrar_log_detallado
import os
import shutil

class ReceiptsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.idioma = "es"
        self.receipts = cargar_datos(RECEIPTS_METADATA_PATH)
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=[20, 40, 20, 20])
        self.titulos = {
            "es": "Gestión de Recibos",
            "en": "Receipts Management",
            "fr": "Gestion des Reçus"
        }
        main_layout.add_widget(Label(
            text=self.titulos[self.idioma],
            font_size=30, bold=True, color=(0.1,0.4,0.7,1),
            size_hint=(1, None), height=60
        ))
        self.textos = {
            "nombre_recibo": {"es": "Nombre Recibo", "en": "Receipt Name", "fr": "Nom du Reçu"},
            "todos": {"es": "Todos", "en": "All", "fr": "Tous"},
            "cargar_archivo": {"es": "Cargar Recibo (Archivo)", "en": "Load Receipt (File)", "fr": "Charger Reçu (Fichier)"},
            "tomar_foto": {"es": "Tomar Foto", "en": "Take Photo", "fr": "Prendre Photo"},
            "elegir_galeria": {"es": "Elegir de Galería", "en": "Choose from Gallery", "fr": "Choisir depuis la Galerie"},
            "cambiar_idioma": {"es": "Cambiar idioma", "en": "Change language", "fr": "Changer de langue"},
            "volver": {"es": "Volver", "en": "Back", "fr": "Retour"},
            "ver": {"es": "Ver", "en": "View", "fr": "Voir"},
            "eliminar": {"es": "Eliminar", "en": "Delete", "fr": "Supprimer"},
            "cerrar": {"es": "Cerrar", "en": "Close", "fr": "Fermer"},
            "recibo_cargado": {"es": "Recibo cargado", "en": "Receipt loaded", "fr": "Reçu chargé"},
            "foto_tomada": {"es": "Foto tomada", "en": "Photo taken", "fr": "Photo prise"},
            "recibo_galeria": {"es": "Recibo desde galería", "en": "Receipt from gallery", "fr": "Reçu depuis la galerie"},
            "recibo_eliminado": {"es": "Recibo eliminado", "en": "Receipt deleted", "fr": "Reçu supprimé"},
        }
        self.input_nombre = TextInput(
            hint_text=self.textos["nombre_recibo"][self.idioma],
            size_hint=(1, None), height=50, font_size=20
        )
        main_layout.add_widget(self.input_nombre)
        # Filtro avanzado por nombre de recibo
        self.spinner = Spinner(
            text=self.textos["todos"][self.idioma],
            values=[self.textos["todos"][self.idioma]] + [r.get('original_filename','') for r in self.receipts if r.get('original_filename','')],
            size_hint=(1, None), height=50, font_size=18
        )
        self.spinner.bind(text=self.on_spinner_select)
        main_layout.add_widget(self.spinner)
        btn_style = {"size_hint": (1, None), "height": 55, "background_color": (0.2,0.6,1,1), "color": (1,1,1,1), "font_size": 20}
        main_layout.add_widget(Button(text=self.textos["cargar_archivo"][self.idioma], on_release=self.cargar_recibo, **btn_style))
        main_layout.add_widget(Button(text=self.textos["tomar_foto"][self.idioma], on_release=self.tomar_foto, **btn_style))
        main_layout.add_widget(Button(text=self.textos["elegir_galeria"][self.idioma], on_release=self.elegir_galeria, **btn_style))
        main_layout.add_widget(Button(text=self.textos["cambiar_idioma"][self.idioma], on_release=self.cambiar_idioma, **btn_style))
        main_layout.add_widget(Button(text=self.textos["volver"][self.idioma], on_release=self.volver, **btn_style))
        scroll = ScrollView(size_hint=(1, 1))
        self.receipts_box = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None)
        self.receipts_box.bind(minimum_height=self.receipts_box.setter('height'))
        scroll.add_widget(self.receipts_box)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
        self.actualizar_lista()

    def on_spinner_select(self, spinner, value):
        self.actualizar_lista()

    def cargar_recibo(self, instance):
        # Solo funciona en desktop/emulador, para móvil se requiere integración nativa
        chooser = FileChooserIconView(path='.', filters=['*.png', '*.jpg', '*.jpeg'])
        def on_selection(instance, selection):
            if selection:
                src = selection[0]
                nombre = self.input_nombre.text.strip() or os.path.basename(src)
                dest = os.path.join(RECEIPTS_DIR, os.path.basename(src))
                shutil.copy2(src, dest)
                nuevo = {
                    "id": str(len(self.receipts) + 1),
                    "original_filename": nombre,
                    "filename": os.path.basename(src),
                    "file_path": dest
                }
                self.receipts.append(nuevo)
                guardar_datos(self.receipts, RECEIPTS_METADATA_PATH)
                self.input_nombre.text = ""
                self.actualizar_lista()
                registrar_log_detallado("Recibo cargado", nombre, self.idioma)
                notification.notify(
                    title=self.textos["recibo_cargado"][self.idioma],
                    message=nombre
                )
            self.layout.remove_widget(chooser)
        chooser.bind(on_selection=on_selection)
        self.layout.add_widget(chooser)

    def tomar_foto(self, instance):
        nombre = self.input_nombre.text.strip() or "recibo_foto"
        dest = os.path.join(RECEIPTS_DIR, f"{nombre}_cam.jpg")
        def on_complete(path):
            if path and os.path.exists(path):
                nuevo = {
                    "id": str(len(self.receipts) + 1),
                    "original_filename": nombre,
                    "filename": os.path.basename(dest),
                    "file_path": dest
                }
                self.receipts.append(nuevo)
                guardar_datos(self.receipts, RECEIPTS_METADATA_PATH)
                self.input_nombre.text = ""
                self.actualizar_lista()
                registrar_log_detallado("Foto recibo tomada", nombre, self.idioma)
                notification.notify(
                    title=self.textos["foto_tomada"][self.idioma],
                    message=nombre
                )
        try:
            camera.take_picture(filename=dest, on_complete=on_complete)
        except Exception as e:
            print("Error al tomar foto:", e)

    def elegir_galeria(self, instance):
        nombre = self.input_nombre.text.strip()
        def on_selection(selection):
            if selection:
                src = selection[0]
                nombre_final = nombre or os.path.basename(src)
                dest = os.path.join(RECEIPTS_DIR, os.path.basename(src))
                try:
                    shutil.copy2(src, dest)
                    nuevo = {
                        "id": str(len(self.receipts) + 1),
                        "original_filename": nombre_final,
                        "filename": os.path.basename(src),
                        "file_path": dest
                    }
                    self.receipts.append(nuevo)
                    guardar_datos(self.receipts, RECEIPTS_METADATA_PATH)
                    self.input_nombre.text = ""
                    self.actualizar_lista()
                    registrar_log_detallado("Recibo desde galería", nombre_final, self.idioma)
                    notification.notify(
                        title=self.textos["recibo_galeria"][self.idioma],
                        message=nombre_final
                    )
                except Exception as e:
                    print("Error al copiar archivo:", e)
        try:
            filechooser.open_file(on_selection=on_selection, filters=["*.png", "*.jpg", "*.jpeg"])
        except Exception as e:
            print("Error al abrir galería:", e)

    def actualizar_lista(self):
        self.receipts_box.clear_widgets()
        filtro = self.spinner.text
        for r in reversed(self.receipts):
            if filtro not in (self.textos["todos"]["es"], self.textos["todos"]["en"], self.textos["todos"]["fr"]) and r.get('original_filename','') != filtro:
                continue
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=45, spacing=5)
            row.add_widget(Label(text=f"{r.get('original_filename','')}", font_size=16, size_hint_x=0.6))
            btn_view = Button(text=self.textos["ver"][self.idioma], size_hint_x=0.2, background_color=(0.2,0.6,1,1), color=(1,1,1,1), font_size=14)
            btn_view.bind(on_release=lambda inst, path=r['file_path']: self.ver_recibo(path))
            btn_del = Button(text=self.textos["eliminar"][self.idioma], size_hint_x=0.2, background_color=(1,0.3,0.3,1), color=(1,1,1,1), font_size=14)
            btn_del.bind(on_release=lambda inst, rid=r['id']: self.eliminar_recibo(rid))
            row.add_widget(btn_view)
            row.add_widget(btn_del)
            self.receipts_box.add_widget(row)

    def ver_recibo(self, path):
        if os.path.exists(path):
            popup = BoxLayout(orientation='vertical')
            popup.add_widget(Image(source=path))
            popup.add_widget(Button(text=self.textos["cerrar"][self.idioma], size_hint=(1, 0.1), on_release=lambda inst: self.remove_widget(popup)))
            self.add_widget(popup)
            registrar_log_detallado("Recibo visualizado", path, self.idioma)

    def eliminar_recibo(self, rid):
        self.receipts = [r for r in self.receipts if r["id"] != rid]
        guardar_datos(self.receipts, RECEIPTS_METADATA_PATH)
        self.actualizar_lista()
        registrar_log_detallado("Recibo eliminado", rid, self.idioma)
        notification.notify(
            title=self.textos["recibo_eliminado"][self.idioma],
            message=str(rid)
        )

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
