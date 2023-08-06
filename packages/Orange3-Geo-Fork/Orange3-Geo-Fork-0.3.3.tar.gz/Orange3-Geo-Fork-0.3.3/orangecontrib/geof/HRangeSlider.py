# Written by Jonathon Loh
import numpy as np

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
from AnyQt.QtWidgets import QAbstractSlider, QSlider, QStyle, QStylePainter, QStyleOptionSlider, QSizePolicy
from AnyQt.QtGui import QPixmap, QPen, QPainter, QTransform, QBrush, QFont, QPalette, QColor
from AnyQt.QtCore import Qt, pyqtSignal, QRect, QSize, QPoint


def _INVALID(*args):
    raise RuntimeError

# A HORIZONTAL-only range slider widget. Accepts and returns float values
# Most QAbstractSlider signals are implemented
# Internally uses an integer (steps) whose value will affect the
# precision of the slider. Use higher values for more precise scrubbing.
# Scales the step value to the appropriate output value based on supplied
# maximum and minimum values.
# The slider has 3 handles:
#   ID 0 - left handle, value always leq right handle's
#   ID 1 - right handle, value always geq left handle's
#   ID 2 - middle handle. Dragging this handle moves both left and right handles
# Supports setTracking()
class HRangeSlider(QAbstractSlider):
    # emitted when the maximum/minimum of the slider is changed.
    # arguments are the new maximum/minimum values
    rangeChanged = pyqtSignal(float, float)
    # emitted when the slider position moves
    # arguments are the new position values
    sliderMoved = pyqtSignal(float, float)
    # emitted when the handle is pressed with its ID
    sliderPressed = pyqtSignal(int)
    # emitted when a handle is released with its ID
    sliderReleased = pyqtSignal(int)
    # emitted when the slider value changes. Changes with position
    # if tracking is enabled: setTracking/hasTracking()
    valueChanged = pyqtSignal(float, float)
    # emitted when the interval changes (gap between max and min)
    # arguments is the new interval value. Always emitted AFTER
    # valueChanged
    intervalChanged = pyqtSignal(float)

    # not supported
    setInvertedAppearance = setInvertedControls = setOrientation = pageStep = setPageStep\
    = singleStep = setSingleStep = setSliderDown = setSliderPosition = actionTriggered\
    = triggerAction = _INVALID

    # creates a slider with
    # minimum   - minimum value of the slider
    # maximum   - maximum value of the slider
    # steps     - affects the granularity (precision) of the slider
    # tracking  - sets tracking on/off
    def __init__(self, *args, **kwargs):
        self.__scaledMinimum = kwargs.pop('minimum', 0)
        self.__scaledMaximum = kwargs.pop('maximum', 99)
        tracking = kwargs.pop('tracking', True)

        self.__steps = max(kwargs.pop('steps', 1024),1)
        self.__scale = (self.__scaledMaximum - self.__scaledMinimum) / self.__steps
        self._tickList = kwargs.pop('ticks', None)

        if self._tickList is not None:
            self._tickList = np.unique(self._tickList)


        self._tickImage = QPixmap()

        minimum = kwargs['minimum'] = 0
        maximum = kwargs['maximum'] = self.__steps

        self.__position0 = self.__value0 = kwargs.pop('value0', minimum)
        self.__position1 = self.__value1 = kwargs.pop('value1', maximum)

        self._handleWidth = kwargs.pop('handleWidth', 10)
        self._tickHeight = 4

        kwargs['orientation'] = Qt.Horizontal
        super().__init__(*args, **kwargs)

        self.setTracking(tracking)
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)

        # holds bounding rectangles for handle0, handle1, inner handle and groove respectively; last rect is invalid
        self._rects = [QRect(), QRect(), QRect(), QRect()]

        # the index of the handle used as index to _rects; -1 is none
        self._hover = -1
        self._press = -1

        # used to calculate mouse events
        self._handleOffset = QPoint()
        self._lastPos = (maximum, minimum)
        self._lastClick = QPoint()

        # 
        self._makeTickMarks()

    # OVERRIDE QABSTRACTSLIDER PROPERTIES
    def invertedAppearance(self):
        return false
    
    def invertedControls(self):
        return false

    def steps(self):
        return self.__steps

    def valueSteps(self):
        return (int(self.__value0), int(self.__value1))
    
    def setValueSteps(self, value0, value1):
        if value0 > value1:
            return
        steps0 = value0
        steps1 = value1
        self.setSliderValue(steps0, steps1)
        if self.__position0 != self.__value0 or self.__position1 != self.__value1:
            self.__position0 = self.__value0
            self.__position1 = self.__value1
            self.sliderMoved.emit(self.stepsToValue(self.__position0), self.stepsToValue(self.__position1))
            self.update()

    # sets a new step value and tries to approximate the old values
    def setSteps(self, steps):
        if steps <= 0:
            return
        oldValue = self.value()
        self.__steps = steps
        self.setValue(oldValue[0], oldValue[1])

    def maximum(self):
        return self.__scaledMaximum

    # sets the maximum value. The minimum value will be set to the new maximum if it is
    # greater (or equal) to the new maximum. Slider positions and values will maintain 
    # their proportion of value between maximum and minimum, so the caller should re-set
    # slider values to their values before the range change if so desired. Note that depending
    # on the step size of the slider, it may not be possible to exactly restore the previous value
    def setMaximum(self, newMaximum):
        if self.__scaledMaximum == newMaximum:
            return False
        self.__scaledMaximum = newMaximum
        self.__scaledMinimum = min(self.__scaledMinimum, self.__scaledMaximum)
        self.rangeChanged.emit(self.__scaledMinimum, self.__scaledMaximum)
        val0 = self.stepsToValue(self.__value0)
        val1 = self.stepsToValue(self.__value1)
        self.valueChanged.emit(val0, val1)
        self.intervalChanged.emit(val1 - val0)
        self._makeTickMarks()
        self.update()
        return True

    def minimum(self):
        return self.__scaledMinimum


    # sets the maximum value. The minimum value will be set to the new maximum if it is
    # greater (or equal) to the new maximum. Slider positions and values will maintain 
    # their proportion of value between maximum and minimum, so the caller should re-set
    # slider values to their values before the range change if so desired. Note that depending
    # on the step size of the slider, it may not be possible to exactly restore the previous value
    def setMinimum(self, newMinimum):
        if self.__scaledMinimum == newMinimum:
            return False
        self.__scaledMinimum = newMinimum
        self.__scaledMaximum = max(self.__scaledMinimum, self.__scaledMaximum)
        self.rangeChanged.emit(self.__scaledMinimum, self.__scaledMaximum)
        val0 = self.stepsToValue(self.__value0)
        val1 = self.stepsToValue(self.__value1)
        self.valueChanged.emit(val0, val1)
        self.intervalChanged.emit(val1 - val0)
        self._makeTickMarks()
        self.update()
        return True

    def orientation(self):
        return Qt.Horizontal

    def isSliderDown(self):
        return self._press in {0,1,2}

    def value(self):
        return (self.stepsToValue(self.__value0), self.stepsToValue(self.__value1))

    # Used to (programatically) set the values AND positions on the slider
    # Slider values will be forced within the range [maximum, minimum], so
    # change slider range before values if necessary
    def setValue(self, value0, value1):
        if value0 > value1:
            return
        steps0 = self.valueToSteps(value0)
        steps1 = self.valueToSteps(value1)
        
        self.setSliderValue(steps0, steps1)
        if self.__position0 != self.__value0 or self.__position1 != self.__value1:
            self.__position0 = self.__value0
            self.__position1 = self.__value1
            self.sliderMoved.emit(self.stepsToValue(self.__position0), self.stepsToValue(self.__position1))
            self.update()

    def setTickList(self, tickList):
        self._tickList = np.nan_to_num(np.unique(tickList))
        self._makeTickMarks()
        self.update()


    # OVERRIDE QABSTRACTSLIDER FUNCTIONS
    # ...
    def stepsToValue(self, steps):
        return steps / self.__steps * (self.__scaledMaximum - self.__scaledMinimum) + self.__scaledMinimum

    def valueToSteps(self, value):
        if self.__scaledMaximum == self.__scaledMinimum:
            return 0
        return round((value - self.__scaledMinimum) / (self.__scaledMaximum - self.__scaledMinimum) * self.__steps)
    


    def _setSliderPosition(self, pos0, pos1):
        oldPos0 = self.__position0
        oldPos1 = self.__position1
        if pos0 is not None:
            self.__position0 = pos0
        if pos1 is not None:
            self.__position1 = pos1
        if self.__position0 > self.__position1:
            if pos1 is None:
                self.__position0 = self.__position1
            if pos0 is None:
                self.__position1 = self.__position0
        
        if self.hasTracking():
            self.setSliderValue(self.__position0, self.__position1)
        if oldPos0 != self.__position0 or oldPos1 != self.__position1:
            self.sliderMoved.emit(self.stepsToValue(self.__position0), self.stepsToValue(self.__position1))
        self.update()

    def setSliderValue(self, val0, val1):
        oldVal0 = self.__value0
        oldVal1 = self.__value1
        if val0 is not None:
            self.__value0 = max(val0, 0)
        if val1 is not None:
            self.__value1 = min(val1, self.__steps)
        val0 = self.stepsToValue(self.__value0)
        val1 = self.stepsToValue(self.__value1)
        if oldVal0 != val0 or oldVal1 != val1:
            self.valueChanged.emit(val0, val1)
        if (oldVal1 - oldVal0) != (self.__value1 - self.__value0):
            #print(oldVal1, ',', oldVal0, ',', val1, ',', val0)
            self.intervalChanged.emit(val1 - val0)

    def updateValues(self):
        self.setSliderValue(self.__position0, self.__position1)

    # override
    def sizeHint(self):
        return QSize(100,21)

    def resizeEvent(self, e):
        self._makeTickMarks()


    # override
    def leaveEvent(self, e):
        oldHoverRect = self._rects[self._hover]
        self._hover = -1
        self.update(oldHoverRect)

    def mouseMoveEvent(self, e):
        #print("pressed: ",self._press,",pos0: ",self.__position0,",pos1: ",self.__position1)
        measureWidth = self.width() - self._handleWidth - self._handleWidth
        if self._press == 0:
            newValue = round((e.pos().x() - self._handleOffset.x()) / measureWidth * self.__steps)
            self._setSliderPosition(max(0, newValue), None)
        if self._press == 1:
            newValue = round((e.pos().x() - self._handleOffset.x() - self._handleWidth) / measureWidth * self.__steps)
            self._setSliderPosition(None, min(self.__steps, newValue))
        elif self._press == 2:
            delta = round((e.pos().x() - self._lastClick.x()) / measureWidth * self.__steps)
            if self._lastPos[0] + delta < 0:
                self._setSliderPosition(0, self.__position1 - self.__position0)
            elif self._lastPos[1] + delta > self.__steps:
                self._setSliderPosition(self.__steps - self.__position1 + self.__position0, self.__steps)
            else:
                self._setSliderPosition(self._lastPos[0] + delta, self._lastPos[1] + delta)
        else:
            oldHover = self._hover
            self._hover = self._testHandles(e.pos())

            if oldHover != self._hover:
                self.update(self._rects[oldHover])
                self.update(self._rects[self._hover])

    def mouseReleaseEvent(self, e):
        e.accept()
        oldPressRect = self._rects[self._press]
        if self._press in {0,1,2}:
            self.sliderReleased.emit(self._press)
            if not self.hasTracking():
                self.setSliderValue(self.__position0, self.__position1)
        self._press = -1
        self.update(oldPressRect)
        

    def mousePressEvent(self, e):
        e.accept()
        self._press = self._testHandles(e.pos())
        if self._press in {0,1,2}:
            if e.button() == Qt.RightButton:
                self._press = 2
            self._handleOffset = e.pos() - self._rects[self._press].topLeft()
            self._lastPos = (self.__position0, self.__position1)
            self._lastClick = e.pos()
            self.sliderPressed.emit(self._press)
        self.update(self._rects[self._press])



    # test all rects for intersection with pos and returns the index
    def _testHandles(self, pos):
        for i, rect in enumerate(self._rects):
            if rect.contains(pos):
                return i
        return -1

    def _makeTickMarks(self):
        if self._tickList is None:
            return
        self._tickImage = pixmap = QPixmap(self.width()-self._handleWidth-self._handleWidth, self._tickHeight)
        pixmap.fill(self.palette().color(QPalette.Active, QPalette.Background))
        painter = QPainter(self._tickImage)
        painter.setPen(QColor(165,162,148))

        w = pixmap.width() - 1
        v = self.__steps
        for val in self._tickList:
            if val < self.__scaledMinimum or val > self.__scaledMaximum:
                continue
            step = self.valueToSteps(val)
            x = step*w/v
            painter.drawLine(x, 0, x, self._tickHeight - 1)



    # override
    def paintEvent(self, e):
        #print("hover: ",self._hover,",press: ",self._press)
        painter = QStylePainter(self)

        # prepare the drawing options
        # for drawing slider groove
        opt = QStyleOptionSlider()
        opt.initFrom(self)

        opt.subControls = QStyle.SC_SliderGroove

        opt.maximum = self.__steps
        opt.minimum = 0
        opt.orientation = self.orientation()
        opt.sliderPosition = self.__position0
        opt.sliderValue = self.__value0

        if self._tickList is not None:
            opt.tickPosition = QSlider.TicksBelow
        else:
            opt.tickPosition = QSlider.NoTicks

        handleWidth = self._handleWidth
        measureWidth = self.width() - handleWidth - handleWidth

        painter.drawComplexControl(QStyle.CC_Slider, opt)

        # draw tickmarks
        if self._tickList is not None:
            painter.drawPixmap(self._handleWidth, self.height() - self._tickHeight, self._tickImage)
            

        # handle colors
        colorPRESS = QColor(204,204,204)
        colorHOVER = QColor(23,23,23)
        colorNORMAL = QColor(0,122,217) if self.isEnabled() else colorPRESS
        
        handleHeight = self.height() if self._tickList is None else self.height() - self._tickHeight
        
        # draw handle 0
        if self._press in {0,2}:
            color = colorPRESS
        elif self._hover == 0:
            color = colorHOVER
        else:
            color = colorNORMAL
        self._rects[0] = r0 = QRect(self.__position0 / self.__steps * measureWidth, 0, handleWidth, handleHeight)
        painter.fillRect(self._rects[0], color)

        # draw handle 1
        if self._press in {1,2}:
            color = colorPRESS
        elif self._hover == 1:
            color = colorHOVER
        else:
            color = colorNORMAL

        self._rects[1] = r1 = QRect(self.__position1 / self.__steps * measureWidth + handleWidth, 0, handleWidth, handleHeight)
        painter.fillRect(self._rects[1], color)

        # draw inner handle
        if self._press == 2 or not self.isEnabled():
            color = QColor(0, 0, 0, 15)
        elif self._hover == 2:
            color = QColor(0, 61, 108, 63)
        else:
            color = QColor(0, 122, 217, 63)

        self._rects[2] = QRect(r0.left(), r0.top(), r1.right()-r0.left()+1, handleHeight)

            
        painter.fillRect(self._rects[2], color)




if __name__ == "__main__":
    from AnyQt.QtWidgets import QApplication, QDialog, QGridLayout, QLabel
    app = QApplication([])
    win = QDialog()
    grid = QGridLayout(win)
    win.setLayout(grid)
    kwargs = dict(
        minimum=-5,
        maximum=7,
        orientation=Qt.Horizontal
    )
    def _printValues(val0, val1):
        print("value0:",val0,", value1:",val1)

    def _printPosition(val0, val1):
        print("position0:",val0,", position1:",val1)

    grid.addWidget(QLabel('Double Slider:', parent=win), 0, 0)
    slider = HRangeSlider(win, **kwargs)
    slider.valueChanged.connect(_printValues)
    slider.sliderMoved.connect(_printPosition)
    slider.setTickList([-5,-1,7,2.2,2.1,5.0])
    grid.addWidget(slider, 0, 1)


    grid.addWidget(QLabel('Double Slider no ticks:', parent=win), 1, 0)
    grid.addWidget(HRangeSlider(win, **kwargs), 1, 1)

    grid.addWidget(QLabel('QSlider:', parent=win), 2, 0)
    slider = QSlider(win, **kwargs)
    slider.setTickPosition(QSlider.TicksBelow)
    grid.addWidget(slider, 2, 1)


    win.show()
    app.exec()

