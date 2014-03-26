class SerializedData:
    def __init__(self,oscBack,oscPlot,oscGridX,oscGridY,powBack,powPlot,powGridX,powGridY, specBack, colorbar,region):
        self.osc_background = oscBack
        self.osc_plot = oscPlot
        self.osc_GridX =oscGridX
        self.osc_GridY = oscGridY
        self.pow_Back = powBack
        self.pow_Plot = powPlot
        self.pow_GridX = powGridX
        self.pow_GridY = powGridY
        self.spec_background = specBack
        self.colorBarState = colorbar
        self.histRange = region
