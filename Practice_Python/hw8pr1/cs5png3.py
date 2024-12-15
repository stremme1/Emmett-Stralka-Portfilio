import os
import sys
from PIL import Image
import time

def saveRGB(boxed_pixels, filename = "out.png"):
    """Save the given pixel array in the chosen file as an image."""
    print(f'Starting to save {filename}...', end = '')
    w, h = getWH(boxed_pixels)
    im = Image.new("RGB", (w, h), "black")
    px = im.load()
    for r in range(h):
        #print(".", end = "")
        for c in range(w):
            bp = boxed_pixels[r][c]
            t = tuple(bp)
            px[c,r] = t
    im.save(filename)
    time.sleep(0.5)
    print(filename, "saved.")

def getRGB(filename = "in.png"):
    """Reads an image png file and returns it as a list of lists of pixels
       (i.e., and array of pixels).
    """
    original = Image.open(filename)
    print(f"{filename} contains a {original.size[0]}x{original.size[1]}"
      f" {original.format} image with mode {original.mode}.")
    WIDTH, HEIGHT = original.size
    px = original.load()
    PIXEL_LIST = []
    for r in range(HEIGHT):
        row = []
        if original.mode == 'RGB':
            for c in range(WIDTH):
                row.append(px[c, r][:3])
        else:
            for c in range(WIDTH):
                pixel = px[c, r]
                row.append((pixel, pixel, pixel))
        PIXEL_LIST.append(row)
    return PIXEL_LIST

def getWH(px):
    """Given a pixel array, return its width and height as a pair."""
    h = len(px)
    w = len(px[0])
    return w, h

def binaryIm(s, cols, rows):
    """Given a binary image s of size rows x cols, represented as
       a single string of 1's and 0's, write a file named "binary.png",
       which contains an equivalent black-and-white image."""
    px = []
    for row in range(rows):
        row = []
        for col in range(cols):
            c = int(s[row*cols + col])*255
            px = [c, c, c]
            row.append(px)
        px.append(row)
    saveRGB(px, 'binary.png')
    #return px

class PNGImage:
    """Class to support simple manipulations on PNG images."""

    def __init__(self, width, height):
        """Construct a PNGImage of the given dimensions."""
        self.width = width
        self.height = height
        default = (255, 255, 255)
        self.image_data = [[(255, 255, 255) for col in range(width)]
                                            for row in range(height)]

    def plotPoint(self, col, row, rgb = (0, 0, 0)):
        """Plot a single RGB point in at the given location in a PNGImage."""
        # Ensure that rgb is a three-tuple
        if not isinstance(rgb, (list, tuple))  or  len(rgb) != 3:
            print(f"In plotPoint, the color {rgb} was not"
              f" in a recognized format.", file = sys.stderr)

        # Check if we're in bounds
        if 0 <= col < self.width and \
           0 <= row < self.height:
            self.image_data[row][col] = rgb

        else:
            print(f"In plotPoint, column {col} or row {row}", file = sys.stderr)
        return

    def saveFile(self, filename = "test.png"):
        """Save the object's data to a file."""
        # We reverse the rows so that the y direction
        # increases upwards...
        saveRGB(self.image_data[::-1], filename)
