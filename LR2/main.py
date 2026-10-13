#  Лабораторная работа №2. Сигналы и слоты в PyQt5
#  Конвертер валют: доллар — рубль — евро.
#  Меняешь одно поле — пересчитываются два других.

import os
import sys
import PyQt5

pyqt_dir = os.path.dirname(PyQt5.__file__)
plugins_root = os.path.join(pyqt_dir, "Qt5", "plugins")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(plugins_root, "platforms")
os.environ['QT_PLUGIN_PATH'] = plugins_root

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QDoubleSpinBox,
    QVBoxLayout, QFormLayout, QGroupBox
)
from PyQt5.QtCore import Qt



#  Примерные курсы валют 
USD_TO_RUB = 95.0                    
EUR_TO_RUB = 103.0                   
USD_TO_EUR = USD_TO_RUB / EUR_TO_RUB 


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Конвертер валют — сигналы и слоты")
        self.resize(420, 320)

        # пока True, обработчики valueChanged игнорируют изменения, чтобы не было бесконечной рекурсии
        self._updating = False

        self.usd = self._make_spinbox()
        self.rub = self._make_spinbox()
        self.eur = self._make_spinbox()

        self.usd.setValue(1.0)
        self.rub.setValue(USD_TO_RUB)
        self.eur.setValue(USD_TO_EUR)

        self.usd.valueChanged.connect(self.on_usd_changed)
        self.rub.valueChanged.connect(self.on_rub_changed)
        self.eur.valueChanged.connect(self.on_eur_changed)

        form = QFormLayout()
        form.addRow("Доллары (USD):", self.usd)
        form.addRow("Рубли (RUB):",   self.rub)
        form.addRow("Евро (EUR):",    self.eur)

        group = QGroupBox("Введите сумму в любом поле")
        group.setLayout(form)

        info = QLabel(
            f"Курсы:  1 USD = {USD_TO_RUB} ₽     "
            f"1 EUR = {EUR_TO_RUB} ₽     "
            f"1 USD = {USD_TO_EUR:.3f} €"
        )
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: gray; font-size: 12px;")

        layout = QVBoxLayout()
        layout.addWidget(group)
        layout.addWidget(info)
        layout.addStretch()
        self.setLayout(layout)

    def _make_spinbox(self):
        box = QDoubleSpinBox()
        box.setRange(0.0, 1_000_000_000.0)  
        box.setDecimals(2)                   
        box.setSingleStep(1.0)               
        box.setSuffix("")                    
        return box

    def on_usd_changed(self, value):
       # Пользователь изменил поле «Доллары»
        if self._updating:     
            return
        self._updating = True

        self.rub.setValue(value * USD_TO_RUB)
        self.eur.setValue(value * USD_TO_EUR)

        self._updating = False

    def on_rub_changed(self, value):
        # Пользователь изменил поле «Рубли»
        if self._updating:
            return
        self._updating = True

        self.usd.setValue(value / USD_TO_RUB)
        self.eur.setValue(value / EUR_TO_RUB)

        self._updating = False

    def on_eur_changed(self, value):
        # Пользователь изменил поле «Евро»
        if self._updating:
            return
        self._updating = True

        self.usd.setValue(value / USD_TO_EUR)
        self.rub.setValue(value * EUR_TO_RUB)

        self._updating = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CurrencyConverter()
    window.show()
    sys.exit(app.exec_())