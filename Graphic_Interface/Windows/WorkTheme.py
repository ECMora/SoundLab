class SerializedData:
    def __init__(self,oscBack,oscPlot,oscGridX,oscGridY,powBack,powPlot,powGridX,powGridY, specBack,specGridX,specGridY, colorbar,region):
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
