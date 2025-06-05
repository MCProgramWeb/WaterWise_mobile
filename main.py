from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from app.screens.home_screen import HomeScreen
from app.screens.departments_screen import DepartmentsScreen
from app.screens.lecturas_screen import LecturasScreen
from app.screens.debt_screen import DebtScreen
from app.screens.receipts_screen import ReceiptsScreen
from app.screens.reports_screen import ReportsScreen
# Importa aquí las demás pantallas cuando las vayas creando

class WaterWiseMobileApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(DepartmentsScreen(name='departments'))
        sm.add_widget(LecturasScreen(name='lecturas'))
        sm.add_widget(DebtScreen(name='deudas'))
        sm.add_widget(ReceiptsScreen(name='recibos'))
        sm.add_widget(ReportsScreen(name='reportes'))
        # Agrega aquí las demás pantallas (lecturas, deudas, etc.)
        return sm

if __name__ == '__main__':
    WaterWiseMobileApp().run()
