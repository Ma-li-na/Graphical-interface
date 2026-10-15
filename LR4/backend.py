import os
import base64
from datetime import datetime

from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class Interface(QObject):

    saved = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._save_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "saves"
        )
        os.makedirs(self._save_dir, exist_ok=True)

        self._counter = 0

    @pyqtSlot(str)
    def saveImage(self, data_url):
     
        try:
            header, b64_data = data_url.split(",", 1)
        except ValueError:
            print("[backend] Ошибка: некорректный data URL")
            return

        try:
            raw_bytes = base64.b64decode(b64_data)
        except Exception as e:
            print("[backend] Ошибка декодирования base64:", e)
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{timestamp}_{self._counter:04d}.png"
        filepath = os.path.join(self._save_dir, filename)

        try:
            with open(filepath, "wb") as f:
                f.write(raw_bytes)
        except OSError as e:
            print("[backend] Не удалось записать файл:", e)
            return

        self._counter += 1
        print(f"[backend] Сохранено: {filepath} ({len(raw_bytes)} байт)")

        self.saved.emit(filepath)

    @pyqtSlot()
    def resetCounter(self):
        self._counter = 0
        print("[backend] Счётчик сброшен")


    @pyqtSlot(result=str)
    def getSaveDir(self):
        return self._save_dir