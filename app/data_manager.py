import os
import json
from datetime import datetime
from kivy.utils import platform

def get_app_data_dir():
    # Usa la carpeta de usuario en Android/iOS, o local en desarrollo
    if platform == 'android':
        from android.storage import app_storage_path
        return app_storage_path()
    elif platform == 'ios':
        from os.path import expanduser
        return os.path.join(expanduser("~"), "Documents", "waterwise_mobile_data")
    else:
        # Para pruebas en PC
        return os.path.join(os.path.expanduser("~"), "waterwise_mobile_data")

APP_DATA_DIR = get_app_data_dir()
DATA_DIR = os.path.join(APP_DATA_DIR, "data")
LOGS_DIR = os.path.join(APP_DATA_DIR, "logs")
BACKUP_DIR = os.path.join(APP_DATA_DIR, "backups")
TICKETS_DIR = os.path.join(APP_DATA_DIR, "tickets")
RECEIPTS_DIR = os.path.join(APP_DATA_DIR, "receipts")

DEPARTAMENTOS_PATH = os.path.join(DATA_DIR, "departamentos.json")
HISTORIAL_LECTURAS_PATH = os.path.join(DATA_DIR, "historial_lecturas.json")
DEUDAS_PATH = os.path.join(DATA_DIR, "deudas.json")
RECEIPTS_METADATA_PATH = os.path.join(DATA_DIR, "receipts_metadata.json")
LOG_ACTIONS_PATH = os.path.join(LOGS_DIR, "acciones.log")

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(TICKETS_DIR, exist_ok=True)
    os.makedirs(RECEIPTS_DIR, exist_ok=True)

ensure_dirs()

def cargar_datos(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def guardar_datos(data, filepath):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def registrar_accion(accion, detalles=""):
    # Log simple (español por defecto)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {accion} - {detalles}\n"
    try:
        with open(LOG_ACTIONS_PATH, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception:
        pass

def registrar_log_detallado(evento, detalles="", idioma="es"):
    """
    Registra un log detallado en el idioma seleccionado.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensajes = {
        "es": f"{timestamp} - {evento} - {detalles}\n",
        "en": f"{timestamp} - {evento} - {detalles}\n"
    }
    log_entry = mensajes.get(idioma, mensajes["es"])
    try:
        with open(LOG_ACTIONS_PATH, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except Exception:
        pass
