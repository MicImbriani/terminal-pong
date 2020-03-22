from DrawingUtils import *
from Constants import COLOURS

class Screen:

    def __init__(self, dims):
        self._dimensions = dims
        self._size = (dims[0] * dims[1])
        self._oldPixels = set()
        self._newPixels = set()

    def setColourIdxAt(self, colourIdx, pos_xy):
        OUT_OF_BOUNDS_WARNING = False

        if(not self._checkInRange(pos_xy)):
            if(OUT_OF_BOUNDS_WARNING):
                print("position (" + str(pos_xy[0]) + " " + str(pos_xy[1]) + ") is out of range")
                input()
        else:
            self._newPixels.add(tuple([tuple(pos_xy), colourIdx]))

    def clear(self):
        self._newPixels.clear()

    def getOutputString(self):
        # Build the string that removes all old data
        output = ""

        # All pixels that were in the last frame but are not in this frame (should become background colour)
        toRemove = self._oldPixels.difference(self._newPixels)

        for oldPixel in toRemove:
            output += colourChangeCode(COLOURS["background"])
            output += moveCursorCode(oldPixel[0], self._dimensions)
            output += " "

        # And combine it with the string that adds any new data
        # TODO: Look into why this works
        #toAdd = self._newPixels
        # but this does not

        #toAdd = self._newPixels.difference(self._oldPixels)
        toAdd = self._newPixels

        for newPixel in toAdd:
            output += colourChangeCode(list(COLOURS.values())[newPixel[1]])
            output += moveCursorCode(newPixel[0], self._dimensions)
            output += " "

        return output

    def swapBuffers(self):
        self._oldPixels = self._newPixels.copy()

    def getSize(self):
        return self._size

    def _checkInRange(self, pos_xy):
        return pos_xy[0] >= 0 and pos_xy[0] < self._dimensions[0] and pos_xy[1] >= 0 and pos_xy[1] < self._dimensions[1]
