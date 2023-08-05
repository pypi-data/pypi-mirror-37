
import sys
from PySide import QtGui

from publisher.gui.channel_editor import ChannelEditor


def channel_editor():
    app = QtGui.QApplication(sys.argv)
    dialog = ChannelEditor()
    dialog.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    channel_editor()
