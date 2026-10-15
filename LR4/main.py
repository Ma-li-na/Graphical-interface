import os
import sys
import PyQt5

pyqt_dir = os.path.dirname(PyQt5.__file__)
plugins_root = os.path.join(pyqt_dir, "Qt5", "plugins")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(plugins_root, "platforms")
os.environ['QT_PLUGIN_PATH'] = plugins_root
os.environ['QML2_IMPORT_PATH'] = os.path.join(plugins_root, "..", "qml")

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QUrl

from backend import Interface


def main():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    backend = Interface()
    engine.rootContext().setContextProperty("backend", backend)

    qml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.qml")
    engine.load(QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        print("Ошибка: не удалось загрузить main.qml")
        sys.exit(-1)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()