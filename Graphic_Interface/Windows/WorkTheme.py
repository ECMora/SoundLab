# -*- coding: utf-8 -*-
class SoundLabTheme:
    """
        The options to customize the environment of work in the system
    """

    def __init__(self, oscBack="000", oscPlot="", oscGridX=True, oscGridY=True, powBack="000", powPlot="FFF", powGridX=True,
                 powGridY=True, specBack="000", specGridX=True, specGridY=True, colorbar=None, region=None, endColor="FFF", centerColor="FFF", startColor="FFF",
                 quart1Color="FFF", quart2Color="FFF",powMinY=-60,powMaxY=5,powLines= True):
        self.osc_background = oscBack
        self.osc_plot = oscPlot
        self.osc_GridX = oscGridX
        self.osc_GridY = oscGridY
        self.spec_GridX = specGridX
        self.spec_GridY = specGridY
        self.pow_spec_lines = powLines
        self.pow_spec_maxY = powMaxY
        self.pow_spec_minY = powMinY
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


class SerializedData:
    """
        The options to customize the environment of work in the system
    """

    def __init__(self, oscBack="000", oscPlot="", oscGridX=True, oscGridY=True, minYOsc = -100,maxYOsc = 100, minYSpec = 0,maxYSpec = 22, powBack="000", powPlot="FFF", powGridX=True,
                 powGridY=True, specBack="000", specGridX=True, specGridY=True, colorbar=None, region=None, endColor="FFF", centerColor="FFF", startColor="FFF",
                 quart1Color="FFF", quart2Color="FFF"):
        self.osc_background = oscBack
        self.osc_plot = oscPlot
        self.osc_GridX = oscGridX
        self.osc_GridY = oscGridY
        self.spec_GridX = specGridX
        self.spec_GridY = specGridY
        self.minYOsc = minYOsc
        self.maxYOsc  = maxYOsc
        self.minYSpec = minYSpec
        self.maxYSpec  = maxYSpec
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