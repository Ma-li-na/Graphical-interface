import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: window
    visible: true
    width: 950
    height: 650
    title: "Lab 4 — Painter с автосохранением"

    // Текущие параметры рисования
    property color penColor: "black"
    property int   penWidth: 3

    ColumnLayout {
        anchors.fill: parent
        spacing: 4

        RowLayout {
            Layout.fillWidth: true
            Layout.margins: 8
            spacing: 10

            Button {
                text: "Clear"
                onClicked: canvas.clearCanvas()
            }

            // Выбор цвета пера
            Repeater {
                model: ["black", "red", "green", "blue"]
                delegate: Rectangle {
                    width: 26; height: 26
                    color: modelData
                    border.color: window.penColor === modelData ? "orange" : "gray"
                    border.width: 2
                    radius: 4

                    MouseArea {
                        anchors.fill: parent
                        onClicked: window.penColor = modelData
                    }
                }
            }

            // Толщина пера
            Label { text: "Толщина:" }
            Slider {
                from: 1; to: 15; value: window.penWidth
                stepSize: 1
                onValueChanged: window.penWidth = value
                Layout.preferredWidth: 120
            }

            // Переключатель автосохранения
            Switch {
                id: autosaveSwitch
                text: "Автосохранение"
                checked: true
            }

            // Кнопка «Сохранить сейчас»
            Button {
                text: "Save now"
                onClicked: backend.saveImage(canvas.toDataURL("image/png"))
            }

            Item { Layout.fillWidth: true }

            Label {
                id: statusLabel
                text: "Готово"
                color: "dimgray"
            }
        }


        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: 8
            color: "white"
            border.color: "gray"

            Canvas {
                id: canvas
                anchors.fill: parent

                property bool initialized: false

                property string backup: ""

                onPaint: {
                    var ctx = getContext("2d")
                    if (!initialized) {
                        // Первая отрисовка — белый фон
                        ctx.fillStyle = "white"
                        ctx.fillRect(0, 0, width, height)
                        initialized = true
                    } else if (backup !== "") {
                        // После изменения размера — восстанавливаем из копии
                        ctx.drawImage(backup, 0, 0, width, height)
                        backup = ""
                    }
                }

                onWidthChanged: {
                    if (initialized) {
                        backup = toDataURL("image/png")
                        requestPaint()
                    }
                }
                onHeightChanged: {
                    if (initialized) {
                        backup = toDataURL("image/png")
                        requestPaint()
                    }
                }


                function clearCanvas() {
                    var ctx = getContext("2d")
                    ctx.clearRect(0, 0, width, height)
                    ctx.fillStyle = "white"
                    ctx.fillRect(0, 0, width, height)
                    initialized = true
                }

                MouseArea {
                    anchors.fill: parent

                    onPressed: {
                        var ctx = canvas.getContext("2d")
                        ctx.beginPath()
                        ctx.moveTo(mouseX, mouseY)
                        ctx.strokeStyle = window.penColor
                        ctx.lineWidth = window.penWidth
                        ctx.lineCap = "round"
                        ctx.lineJoin = "round"
                    }

                    onPositionChanged: {
                        if (pressed) {
                            var ctx = canvas.getContext("2d")
                            ctx.lineTo(mouseX, mouseY)
                            ctx.stroke()
                            canvas.requestPaint()
                        }
                    }
                }
            }
        }
    }

    Timer {
        id: autosaveTimer
        interval: 50000
        repeat: true
        running: autosaveSwitch.checked
        onTriggered: {
            backend.saveImage(canvas.toDataURL("image/png"))
        }
    }

    Connections {
        target: backend
        function onSaved(path) {
            statusLabel.text = "Сохранено: " + path
            console.log("[QML] Файл сохранён:", path)
        }
    }
}