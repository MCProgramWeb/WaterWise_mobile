# WaterWise Mobile

Versión móvil multiplataforma (Android/iOS) de la app de gestión de consumo de agua.

## Requisitos

- Python 3.10+
- [Kivy](https://kivy.org/)
- [Buildozer](https://github.com/kivy/buildozer) (para Android)
- [kivy-ios](https://github.com/kivy/kivy-ios) (para iOS, Mac requerido)

## Instalación y ejecución (modo desarrollo)

```bash
pip install -r requirements.txt
python main.py
```

## Compilar para Android

**¡Importante!**  
El archivo `buildozer.spec` debe tener la siguiente estructura (no borres la primera línea `[app]` ni los encabezados de sección):

```ini
[app]
# (No borres esta línea, debe ser la primera del archivo)
# ...otras opciones...
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA,VIBRATE,WAKE_LOCK
requirements = python3,kivy,plyer,reportlab,matplotlib
# ...otras opciones...
```

Si ves el error `MissingSectionHeaderError`, abre tu `buildozer.spec` y asegúrate de que la PRIMERA línea sea `[app]` y que todas las opciones estén bajo una sección.

```bash
# Instala buildozer si no lo tienes
pip install buildozer
# Inicializa buildozer (esto crea un buildozer.spec correcto)
buildozer init
# Edita buildozer.spec según tus necesidades (agrega permisos y requirements)
# Luego compila:
buildozer -v android debug
```

## Compilar para iOS

Sigue la guía oficial de kivy-ios: https://github.com/kivy/kivy-ios

## Compilar APK en la nube con GitHub Actions

Puedes compilar tu APK automáticamente usando [GitHub Actions](https://github.com/kivy/buildozer-action):

1. Sube tu proyecto a un repositorio de GitHub.
2. Crea la carpeta `.github/workflows` en la raíz de tu proyecto.
3. Dentro de esa carpeta, crea un archivo llamado `buildozer-android.yml` con el siguiente contenido:

```yaml
name: Buildozer Android APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Build APK with Buildozer
        uses: kivy/buildozer-action@v1
        with:
          command: buildozer android debug
      - name: Upload APK
        uses: actions/upload-artifact@v3
        with:
          name: app-apk
          path: bin/*.apk
```

4. Haz commit y push de los cambios a GitHub.
5. Ve a la pestaña "Actions" de tu repositorio y ejecuta el workflow manualmente ("Run workflow").
6. Cuando termine, descarga el APK desde los "Artifacts" del workflow.

**¿Qué hacer ahora?**

1. **Sube tu proyecto a un repositorio de GitHub**  
   (Crea un repositorio nuevo y haz commit/push de todos tus archivos).

2. **Agrega el workflow de GitHub Actions:**  
   - Crea la carpeta `.github/workflows` en la raíz de tu proyecto.
   - Dentro de esa carpeta, crea el archivo `buildozer-android.yml` con el contenido YAML que aparece arriba.

3. **Haz commit y push de estos cambios a GitHub.**

4. **Entra a tu repositorio en GitHub → pestaña "Actions".**
   - Haz clic en "Run workflow" para ejecutar el build.

5. **Cuando termine el workflow, descarga el APK**  
   - Ve a la sección "Artifacts" del workflow y descarga el archivo `.apk`.

**¡Listo! Así obtienes tu APK compilado en la nube sin usar Linux localmente.**

## Notas

- Los datos de la app móvil se almacenan en el almacenamiento interno del dispositivo, separados de la versión de escritorio.
- No modifiques el proyecto original de escritorio, este es un proyecto independiente.

## Subir tu proyecto a GitHub desde la línea de comandos

1. Abre la terminal y navega a la carpeta raíz de tu proyecto:
   ```bash
   cd "C:\Users\Miguel Angel\Desktop\MIS CREACIONES IA\waterwise_mobile"
   ```

2. Inicializa un repositorio git (si no lo has hecho):
   ```bash
   git init
   ```

3. Agrega todos los archivos:
   ```bash
   git add .
   ```

4. Haz tu primer commit:
   ```bash
   git commit -m "Primer commit de WaterWise Mobile"
   ```

5. Crea un repositorio vacío en GitHub (desde la web).

6. Conecta tu proyecto local con el repositorio remoto (reemplaza `<URL_DEL_REPO>` por la URL de tu repo en GitHub):
   ```bash
   git remote add origin <URL_DEL_REPO>
   ```

7. Sube tu proyecto:
   ```bash
   git branch -M main
   git push -u origin main
   ```

**¡Listo! Tu proyecto estará en GitHub y podrás usar GitHub Actions para compilar tu APK.**

# WATERWISE_MOBILE