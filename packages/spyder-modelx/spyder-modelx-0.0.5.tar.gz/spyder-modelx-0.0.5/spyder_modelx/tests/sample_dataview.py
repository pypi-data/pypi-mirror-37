import sys
import numpy
from pandas import DataFrame, MultiIndex

from spyder_modelx.widgets.mxdataview import MxDataFrameWidget, MxDataFrameModel

from qtpy.QtWidgets import QApplication

arrays = [numpy.array(['bar', 'bar', 'baz', 'baz',
                       'foo', 'foo', 'qux', 'qux']),
          numpy.array(['one', 'two', 'one', 'two',
                       'one', 'two', 'one', 'two'])]
tuples = list(zip(*arrays))
index = MultiIndex.from_tuples(tuples, names=['first', 'second'])
df = DataFrame(numpy.random.randn(8, 8), index=index[:8],
               columns=index[:8])



def main1():

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # print(df.T)
    model = MxDataFrameModel(df)
    widget = MxDataFrameWidget(data=df)

    # widget.dataModel = model
    # widget.setModel(model)
    print(widget.table_level.model().rowCount())
    print(widget.table_header.model().rowCount())
    widget.show()
    app.exec_()

def main2():
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    # print(df.T)
    model = MxDataFrameModel(df)
    widget = MxDataFrameWidget()

    # widget.dataModel = model
    widget.setModel(model)
    widget.resizeColumnsToContents()
    print(widget.table_level.model().rowCount())
    print(widget.table_header.model().rowCount())
    widget.show()
    app.exec_()


if __name__ == '__main__':
    main2()
