
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import logging
import cv2

class MovieMaker():

    def __init__(self):
        self.frame_collection = []

    def add_frame(self, data, hold=1):

        if isinstance(data, matplotlib.figure.Figure):
            _ = data.canvas.draw()
            data = np.array(fig.canvas.renderer._renderer).astype(np.uint8)

            plt.close()

        assert len(data.shape)==3, "Data must be a rank 3 array (w,h,c)."
        if data.shape[2]==4:
            logging.warning("It looks like your array might be RGBA. Ignoring the alpha channel.")
            data = data[:,:,0:3]

        data = data.astype(np.uint8)
        for i in range(hold):
            self.frame_collection.append(data)

    def render(self, outputfile, fps=30):
        assert outputfile[-4:]=='.avi', "Outputfile must end in .avi."
        width, height = self.frame_collection[0].shape[0:2]
        fourcc = cv2.VideoWriter_fourcc(*'mjpg') # Be sure to use the lower case
        out = cv2.VideoWriter(outputfile, fourcc, float(fps), (height, width))
        for frame in self.frame_collection:
            dat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(dat)
        out.release()


