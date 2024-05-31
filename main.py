import sys
from PyQt5 import QtWidgets
from gui import ShobbakTool
import addFolders as af
if __name__ == "__main__":
    af.folder_creation_helpe("input")
    af.folder_creation_helpe("output")
    app = QtWidgets.QApplication(sys.argv)
    window = ShobbakTool()
    window.show()
    sys.exit(app.exec_())
