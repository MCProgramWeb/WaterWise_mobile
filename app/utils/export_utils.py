from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

def exportar_reporte_pdf(filepath, lecturas):
    """
    Exporta un reporte de lecturas a un archivo PDF.
    :param filepath: Ruta destino del PDF.
    :param lecturas: Lista de dicts con lecturas.
    """
    try:
        c = canvas.Canvas(filepath, pagesize=letter)
        c.drawString(100, 750, "Reporte de Consumo de Agua")
        y = 700
        for l in lecturas:
            c.drawString(100, y, f"Depto {l.get('departamento_id','')} | {l.get('fecha_lectura','')} | Consumo: {l.get('consumo_departamento',0)}")
            y -= 20
            if y < 50:
                c.showPage()
                y = 750
        c.save()
        return True
    except Exception as e:
        print(f"Error exportando PDF: {e}")
        return False

def exportar_grafico_consumo(filepath, lecturas):
    """
    Exporta un gráfico de consumo a una imagen JPG/PNG.
    :param filepath: Ruta destino de la imagen.
    :param lecturas: Lista de dicts con lecturas.
    """
    try:
        fechas = [l.get('fecha_lectura','') for l in lecturas]
        consumos = [l.get('consumo_departamento',0) for l in lecturas]
        plt.figure(figsize=(8,4))
        plt.plot(fechas, consumos, marker='o')
        plt.title("Consumo de Agua")
        plt.xlabel("Fecha")
        plt.ylabel("Consumo")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(filepath)
        plt.close()
        return True
    except Exception as e:
        print(f"Error exportando gráfico: {e}")
        return False
