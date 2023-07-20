from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
import sys, os, serial
import sqlite3, time

class SqlLiteTimeSeries():
    def __init__(self, p2f, p2c ):

      self.insert_cntr = 0
      self.path2file = p2f
      self.ins2commit = p2c

      self.con = sqlite3.connect(p2f)
      self.cur = self.con.cursor()
      self.cur.execute("CREATE TABLE IF NOT EXISTS data(sensor1 REAL,sensor2 REAL,sensor3 REAL,sensor4 REAL,time INTEGER)")
      self.cur.execute("BEGIN")

    def store (self, data ):
      self.insert_cntr +=1
      if ( self.insert_cntr > self.ins2commit ):
          self.insert_cntr = 0
          self.flush()

      data.append( time.time() )
      self.cur.execute("INSERT INTO data VALUES(?, ?, ?, ?, ?)", data )

    def flush(self):
      self.cur.execute("COMMIT")
      self.cur.execute("BEGIN")



class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.lenX = 200

      
        self.store = SqlLiteTimeSeries("tenso."+str(time.ctime(time.time()).replace(' ', '_'))+".db", self.lenX )

        self.init_plot()
        self.init_serial()

    def handle_serial(self):
      line = self.ser.readline().decode("utf-8")
      #print(line)
      yx = list(map(float, line.split(',') ))
      self.store2db(yx)
      self.draw2plot(yx)

    def store2db(self, yx):
      self.store.store(yx)

    def draw2plot(self, yx):
      self.list_chan1 = self.list_chan1[1:]
      self.list_chan2 = self.list_chan2[1:]
      self.list_chan3 = self.list_chan3[1:]
      self.list_chan4 = self.list_chan4[1:]
      self.list_chan1.append( yx[0] )
      self.list_chan2.append( yx[1] )
      self.list_chan3.append( yx[2] )
      self.list_chan4.append( yx[3] )

      self.graphWidget.clear()
      self.graphWidget.plot(self.listX, self.list_chan1, name="Sensor 1", pen=self.pen1 )
      self.graphWidget.plot(self.listX, self.list_chan2, name="Sensor 2", pen=self.pen2 )
      self.graphWidget.plot(self.listX, self.list_chan3, name="Sensor 3", pen=self.pen3 )
      self.graphWidget.plot(self.listX, self.list_chan4, name="Sensor 4", pen=self.pen4 )

    def init_serial(self):
        print("Open Serial")
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        if ( self.ser.is_open ):
          self.timer = QTimer()
          self.timer.setInterval(50)
          self.timer.setSingleShot(False)
          self.timer.start()
          self.timer.timeout.connect(self.handle_serial)

    def init_plot(self):
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        #Add Background colour to white
        self.graphWidget.setBackground('w')
        # Add Title
        self.graphWidget.setTitle("200 last tics (other in db)", color="b", size="14pt")
        # Add Axis Labels
        styles = {"color": "#46f", "font-size": "12px"}
        self.graphWidget.setLabel("left", "ADC_points", **styles)
        self.graphWidget.setLabel("bottom", "Tics", **styles)
        #Add legend
        self.graphWidget.addLegend()
        #Add grid
        self.graphWidget.showGrid(x=True, y=True)
        #Set Range
        self.graphWidget.setXRange(0, self.lenX, padding=0)


        self.listX = []
        self.list_chan1 = []
        self.list_chan2 = []
        self.list_chan3 = []
        self.list_chan4 = []
        for x in range(self.lenX): self.listX.append(x)
        for x in range(self.lenX): self.list_chan1.append(0)
        for x in range(self.lenX): self.list_chan2.append(0)
        for x in range(self.lenX): self.list_chan3.append(0)
        for x in range(self.lenX): self.list_chan4.append(0)

        self.pen1 = pg.mkPen(color=(255, 0, 0), width=2)
        self.pen2 = pg.mkPen(color=(255, 255, 0), width=2)
        self.pen3 = pg.mkPen(color=(255, 0, 255), width=2)
        self.pen4 = pg.mkPen(color=(0, 255, 255), width=2)

        self.graphWidget.plot(self.listX, self.list_chan1, name="Sensor 1", pen=self.pen1 )
        self.graphWidget.plot(self.listX, self.list_chan2, name="Sensor 2", pen=self.pen2 )
        self.graphWidget.plot(self.listX, self.list_chan3, name="Sensor 3", pen=self.pen3 )
        self.graphWidget.plot(self.listX, self.list_chan4, name="Sensor 4", pen=self.pen4 )



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()