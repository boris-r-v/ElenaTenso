import pyqtgraph as pg
import numpy as np

print("Generating 1000 lines with 50 data points each (total 50,000 data points)..")
win1 = pg.plot()
for i in range(5):
  win1.plot(np.arange(50), np.random.random(50))

print("Generating one line with 50,000 data points..")
win2 = pg.plot()
win2.plot(np.arange(50000), np.random.random(50000))

print("Done")

pg.QtGui.QApplication.exec_()
