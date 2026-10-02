import os
import sys
import PyQt5

pyqt_dir = os.path.dirname(PyQt5.__file__)
plugins_root = os.path.join(pyqt_dir, "Qt5", "plugins")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(plugins_root, "platforms")
os.environ['QT_PLUGIN_PATH'] = plugins_root

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 — задание")
        self.resize(700, 420)

        self.label = QLabel("Надпись")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.label.setWordWrap(True)
        self.label.setFixedHeight(60)

        # Кнопка 1
        self.btn1 = QPushButton("Кнопка 1")
        self.btn1.clicked.connect(self.change_text)

        left_layout = QVBoxLayout()
        left_layout.addStretch()
        left_layout.addWidget(self.label)
        left_layout.addWidget(self.btn1)
        left_layout.addStretch()

        left_frame = QFrame()
        left_frame.setLayout(left_layout)

        self.image_label = QLabel("Здесь появится изображение")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(280, 280)
        self.image_label.setStyleSheet(
            "border: 1px dashed gray; color: gray; font-size: 13px;"
        )
        self.image_label.setScaledContents(False)

        # Кнопка 2
        self.btn2 = QPushButton("Кнопка 2")
        self.btn2.clicked.connect(self.show_image)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.image_label)
        right_layout.addWidget(self.btn2)

        right_frame = QFrame()
        right_frame.setLayout(right_layout)

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_frame, 1)
        main_layout.addWidget(right_frame, 1)
        self.setLayout(main_layout)

    def change_text(self):
        """Кнопка 1 — меняет надпись слева."""
        self.label.setText("Текст изменён!\nКнопка 1 сработала.")

    def show_image(self):
        """Кнопка 2 — показывает PNG справа."""
        image_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "image.png"
        )
        print("Ищу файл:", image_path)
        print("Файл существует:", os.path.exists(image_path))

        pixmap = QPixmap(image_path)
        print("QPixmap загружен:", not pixmap.isNull())

        if pixmap.isNull():
            self.image_label.setText(
                "Не удалось загрузить файл.\n"
                "Смотрите вывод в терминале."
            )
            return

        # Масштабируем под размер области, сохраняя пропорции
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.width() - 10,
                self.image_label.height() - 10,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )
        self.image_label.setStyleSheet("border: none;")
        self.image_label.setText("")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())