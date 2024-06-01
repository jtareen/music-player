import sys , os
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from ui.ui import MusicPlayer

basedir = os.path.dirname(__file__)

try:
  from ctypes import windll # Only exists on Windows.
  myappid = "myprojec.oopproject.musicplayer" 
  windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
  pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, "icons/icon.svg")))
    player = MusicPlayer()
    player.show()
    sys.exit(app.exec())