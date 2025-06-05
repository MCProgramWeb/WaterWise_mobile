import os
import shutil
from app.data_manager import APP_DATA_DIR, BACKUP_DIR

def crear_backup(nombre="backup.zip"):
    backup_path = os.path.join(BACKUP_DIR, nombre)
    try:
        shutil.make_archive(backup_path.replace('.zip',''), 'zip', APP_DATA_DIR)
        return backup_path
    except Exception as e:
        print(f"Error creando backup: {e}")
        return None

def restaurar_backup(backup_zip_path):
    try:
        shutil.unpack_archive(backup_zip_path, APP_DATA_DIR, 'zip')
        return True
    except Exception as e:
        print(f"Error restaurando backup: {e}")
        return False
