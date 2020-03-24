from DrawingUtils import *
from Colours import COLOURS


class Screen:


    def __init__(self, dims):
        self._dimensions = dims
        self._size = (dims[0] * dims[1])
        self._old_pixels = set()
        self._new_pixels = set()


    def set_colour_idx_at(self, colour_idx, pos_xy):
        OUT_OF_BOUNDS_WARNING = False

        if(not self._check_in_range(pos_xy)):
            if(OUT_OF_BOUNDS_WARNING):
                print("position (" + str(pos_xy[0]) + " " + str(pos_xy[1]) + ") is out of range")
                input()
        else:
            self._new_pixels.add(tuple([tuple(pos_xy), colour_idx]))


    def _check_in_range(self, pos_xy):
        return pos_xy[0] >= 0 and pos_xy[0] < self._dimensions[0] and pos_xy[1] >= 0 and pos_xy[1] < self._dimensions[1]


    def clear(self):
        self._new_pixels.clear()


    def get_output_string(self):
        # Build the string that removes all old data
        output = ""

        # All pixels that were in the last frame but are not in this frame (should become background colour)
        to_remove = self._old_pixels.difference(self._new_pixels)

        for old_pixel in to_remove:
            output += colour_change_code(COLOURS["background"])
            output += move_cursor_code(old_pixel[0], self._dimensions)
            output += " "

        # And combine it with the string that adds any new data
        # TODO: Look into why this works
        #toAdd = self._new_pixels
        # but this does not

        #toAdd = self._new_pixels.difference(self._oldPixels)
        to_add = self._new_pixels

        for new_pixel in to_add:
            output += colour_change_code(list(COLOURS.values())[new_pixel[1]])
            output += move_cursor_code(new_pixel[0], self._dimensions)
            output += " "

        return output


    def swap_buffers(self):
        self._old_pixels = self._new_pixels.copy()
