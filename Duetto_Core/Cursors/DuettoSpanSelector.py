from matplotlib.widgets import SpanSelector
class DuettoSpanSelector(SpanSelector):

    def setVisible(self,visible=True):
        self.visible=visible
        self.rect.set_visible(self.visible)
        self.canvas.draw()



