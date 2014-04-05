import sys
from PyQt4.QtGui import *
from datetime import datetime

date = datetime.now()
filename = date.strftime('%Y-%m-%d_%H-%M-%S.jpg')
app = QApplication(sys.argv)
widget = QWidget()
# set up the QWidget...
#widget.setLayout(QVBoxLayout())
#
#label = QLabel()
#widget.layout().addWidget(label)
#
#def shoot():
#    p = QPixmap.grabWindow(widget.winId())
#    p.save(filename, 'jpg')
#    label.setPixmap(p)        # just for fun :)
#    print "shot taken"
#
#widget.layout().addWidget(QPushButton('take screenshot', clicked=shoot))
#
#widget.show()
#app.exec_()
a = []
b = [1]
print([x for x in a])
b.extend(a)
print("a")
b.extend([x for x in a if x[1]])
print(b)