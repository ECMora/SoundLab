from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
class DuettoNavigationToolbar(NavigationToolbar):
    "falta modificar la barra de nav para poner los botones de play pause y stop"
    def draw_rubberband( self, event, x0, y0, x1, y1 ):
        pass


