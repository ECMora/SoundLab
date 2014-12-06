class OscillogramTheme:
    def __init__(self, background_color="000", plot_color="CC3", gridX=True, gridY=True, connectPoints=True):  # , minY=-100, maxY=100):
        self.background_color = background_color
        self.plot_color = plot_color
        self.gridX = gridX
        self.gridY = gridY
        # self.minY = minY
        # self.maxY = maxY
        self.connectPoints = connectPoints

    def copy(self):
        return OscillogramTheme(self.background_color, self.plot_color, self.gridX, self.gridY, self.connectPoints)


class SpectrogramTheme:
    def __init__(self, background_color="000", gridX=True, gridY=True, colorbar=None, histRange=(-40, 0)):  # ,minY=0, maxY=22,
        self.gridX = gridX
        self.gridY = gridY
        # self.minY = minY
        # self.maxY = maxY
        self.background_color = background_color
        self.colorBarState = colorbar if colorbar is not None else {
            'ticks': [(0.3333, (185, 0, 0, 255)), (0.6666, (255, 220, 0, 255)), (1, (255, 255, 255, 255)),
                      (0, (0, 0, 0, 255))],
            'mode': 'rgb'}
        self.histRange = histRange

    def copy(self):
        return SpectrogramTheme(self.background_color, self.gridX, self.gridY, self.colorBarState, self.histRange)


class OneDimensinalTheme:
    def __init__(self, background_color="000", plot_color="FFF", gridX=True, gridY=True):
        self.background_color = background_color
        self.plot_color = plot_color
        self.gridX = gridX
        self.gridY = gridY

    def copy(self):
        return OneDimensinalTheme(self.background_color, self.plot_color, self.gridX, self.gridY)


class DetectionTheme:
    def __init__(self, endColor='FFF', startColor='FFF', quart1Color='FFF', centerColor='FFF', quart2Color='FFF'):
        self.endColor = endColor
        self.startColor = startColor
        self.quart1Color = quart1Color
        self.centerColor = centerColor
        self.quart2Color = quart2Color

    def copy(self):
        return DetectionTheme(self.endColor, self.startColor, self.quart1Color, self.centerColor, self.quart2Color)


class WorkTheme:
    """
    The options to customize the environment of work in the system
    """

    def __init__(self, oscillogramTheme=None, spectrogramTheme=None, oneDimensionalTheme=None, detectionTheme=None):
        self.oscillogramTheme = oscillogramTheme if oscillogramTheme is not None else OscillogramTheme()
        self.spectrogramTheme = spectrogramTheme if spectrogramTheme is not None else SpectrogramTheme()
        self.oneDimensionalTheme = oneDimensionalTheme if oneDimensionalTheme is not None else OneDimensinalTheme()
        self.detectionTheme = detectionTheme if detectionTheme is not None else DetectionTheme()

    def copy(self):
        return WorkTheme(self.oscillogramTheme.copy(), self.spectrogramTheme.copy(), self.oneDimensionalTheme.copy(),
                         self.detectionTheme.copy())
