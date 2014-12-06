class OscillogramTheme:
    def __init__(self, background_color="000", plot_color="CC3", gridX=True, gridY=True):  # , minY=-100, maxY=100):
        self.background_color = background_color
        self.plot_color = plot_color
        self.gridX = gridX
        self.gridY = gridY
        # self.minY = minY
        # self.maxY = maxY


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


class PowerSpectrumTheme:
    def __init__(self, background_color="000", plot_color="FFF", gridX=True, gridY=True):
        self.background_color = background_color
        self.plot_color = plot_color
        self.gridX = gridX
        self.gridY = gridY


class DetectionTheme:
    def __init__(self, endColor='FFF', startColor='FFF', quart1Color='FFF', centerColor='FFF', quart2Color='FFF'):
        self.endColor = endColor
        self.startColor = startColor
        self.quart1Color = quart1Color
        self.centerColor = centerColor
        self.quart2Color = quart2Color


class WorkTheme:
    """
    The options to customize the environment of work in the system
    """

    def __init__(self, oscillogramTheme=None, spectrogramTheme=None, powerSpectrumTheme=None, detectionTheme=None):
        self.oscillogramTheme = oscillogramTheme if oscillogramTheme is not None else OscillogramTheme()
        self.spectrogramTheme = spectrogramTheme if spectrogramTheme is not None else SpectrogramTheme()
        self.powerSpectrumTheme = powerSpectrumTheme if powerSpectrumTheme is not None else PowerSpectrumTheme()
        self.detectionTheme = detectionTheme if detectionTheme is not None else DetectionTheme()
