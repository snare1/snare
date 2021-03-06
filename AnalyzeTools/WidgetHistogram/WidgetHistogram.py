# This file is part of SNARE.
# Copyright (C) 2016  Philipp Merz and Malte Merdes
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from AnalyzeTools.AnalyzeWidget import AnalyzeWidget

# adjust these imports
from AnalyzeTools.WidgetHistogram.CalculationHistogram import CalculationHistogram
from AnalyzeTools.WidgetHistogram.PlotHistogram import PlotHistogram
from AnalyzeTools.NavMenu import NavMenuStandard


class WidgetHistogram(AnalyzeWidget):
    """
    Histogram Analyze Widget.

    The Histogram shows the probability of occurance for every 0.1 dB sound pressure level step. Beside the
    propability bar plot a rising cumultative sum is overlayed.
    Depending on calibration either with dB fullscale peakvalues or in dB soundpressure level values.
    seealso::For further information on the calculation implementation have a look at CalculationHistogram.

    note::At initialisation the calculation and plotFigure methods are executed automatically.
    The QWidget stored in self.plot will be integrated in the Analyze Frame.
    """

    def __init__(self, snare, channel, selNo, timeWeight, fqWeight, parm1=None, parm2=None, parm3=None):
        """
        Initialize the parameters and submit them to the constructor of the AnalyzeWidget base class.
        :param snare: Common used variables implenented in MainBackend.
        :type snare: object
        :param channel: Channelobject
        :type channel: object
        :param selNo: String of selection label
        :type selNo: str
        :param timeWeight: Time weight slow, fast or impulse
        :type timeWeight: str
        :param fqWeight: Frequency weight A, B, C or Z
        :type fqWeight: str
        :param parm1: optional widget parameter (for widget NavMenu)
        :param parm2: optional widget parameter (for widget NavMenu)
        :param parm3: optional widget parameter (for widget NavMenu)
        """
        self.nav = NavMenuStandard()
        self.buffer = snare.analyzeBuffer.getBuffer(channel, selNo)
        self.resolution = 10    # resolution: 10 probability bars/dB
        super().__init__(snare, channel, selNo, timeWeight, fqWeight)

    def calculate(self):
        """
        Initialize the calculation object and execute it.
        """
        self.calc = CalculationHistogram(self.snare, self.buffer, self.calib, self.timeWeight, self.fqWeight,
                                         self.resolution)

    def plot(self):
        """
        Initialize the plot object, store the matplot figure and fill out the labels.
         """
        # store & plotting
        self.plot = PlotHistogram(self.calc.xAxis, self.calc.probDb, self.calib, 'dBSPL', 'dBFS',
                                        'Probability of Occurrence (%)', self.calc.probSum, self.resolution).getPlot()

        # labeling
        self.titleLabel = QLabel(self.channel.getName() + ' ' + self.selNo + ': ' + 'Histogram')
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.infoLabel = QLabel(self.calibInfo + ' Weighting: ' + self.fqWeight + self.spacing + 'Meter Speed: ' +
                                self.timeWeight + self.spacing)