class SerializedData:
    def __init__(self,oscBack,oscPlot,oscGridX,oscGridY,powBack,powPlot,powGridX,powGridY, specBack,specGridX,specGridY, colorbar,region,endColor,centerColor,startColor,quart1Color,quart2Color):
        self.osc_background = oscBack
        self.osc_plot = oscPlot
        self.osc_GridX =oscGridX
        self.osc_GridY = oscGridY
        self.spec_GridX =specGridX
        self.spec_GridY = specGridY
        self.pow_Back = powBack
        self.pow_Plot = powPlot
        self.pow_GridX = powGridX
        self.pow_GridY = powGridY
        self.spec_background = specBack
        self.colorBarState = colorbar
        self.histRange = region
        self.endColor = endColor
        self.startColor = startColor
        self.quart1Color = quart1Color
        self.centerColor = centerColor
        self.quart2Color = quart2Color