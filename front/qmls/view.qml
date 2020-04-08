import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Layouts 1.11

Item {
    width: 400
    height: 300
    visible: true

    Layout.maximumWidth: 400
    Layout.minimumWidth: 400

    Layout.maximumHeight: 250
    Layout.minimumHeight: 250

    Rectangle {
        width: parent.width
        height: parent.height
        anchors.bottom: parent.bottom

        Rectangle {
            id: upper_halfh
            width: parent.width
            height: parent.height / 2
            color: '#808080'

            Rectangle {
                id: word_window
                width: 2 * parent.width / 3
                height: 2 * parent.height / 3
                anchors.centerIn: parent

                color: '#E6E6FA'
                anchors.fill: parent
                anchors.margins: 20

//                Row {
//                    anchors.margins: 1
////                    anchors.verticalCenter: parent.verticalCenter
//                    anchors.centerIn: word_window
//                    spacing: 0

                    Text {
                        id: main_word1
                        text: bridge.get_word_A()
                        padding: 0
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: main_word2.left

                        FpsTimer {
                            onTriggered: main_word1.text = bridge.get_word_A()
                        }
                    }

                    Text {
                        id: main_word2
                        text: bridge.get_word_B()
                        color: "red"
                        padding: 0
                        anchors.centerIn: parent

                        FpsTimer {
                            onTriggered: main_word2.text = bridge.get_word_B()
                        }
                    }

                    Text {
                        id: main_word3
                        text: bridge.get_word_C()
                        padding: 0
                        anchors.left: main_word2.right
                        anchors.verticalCenter: parent.verticalCenter

                        FpsTimer {
                            onTriggered: main_word3.text = bridge.get_word_C()
                        }
                    }
//                }
            }

            Rectangle {
                id: bar
                width: 2 * parent.width / 3
                height: parent.height / 20
                anchors.horizontalCenter: parent.horizontalCenter

                anchors.top: word_window.bottom
                anchors.left: word_window.left

                color: "#AFEEEE"

//                FpsTimer {
//                    onTriggered: bar_done.width = bridge.get_progress() * bar.width
//                }

                FpsTimer {
                    onTriggered: bar_not_done.width = (1 - bridge.get_progress()) * bar.width
                }

//                Rectangle {
//                    id: bar_done
//                    height: parent.height
//                    width: 1
//
//                    anchors.left: parent.left
//                    anchors.top: parent.top
//
//                    color: "green"
//                }

                Rectangle {
                    id: bar_not_done
                    height: parent.height
                    width: parent.width

                    anchors.top: parent.top
                    anchors.right: parent.right

                    color: "#20B2AA"
                }
            }
        }

        Rectangle {
            id: bottom_halfh
            width: parent.width
            height: parent.height / 2
            anchors.top: upper_halfh.bottom
            anchors.left: upper_halfh.left

            color: '#808080'

            Column {
                anchors.centerIn: parent
                spacing: 20

                Row {
                    id: speed_row
                    spacing: 17
//                    anchors.centerIn: parent
//                    anchors.top: parent.top

                    Text {
                        text: "Reading speed:"
                    }

                    FpsTimer {
                        onTriggered: speed_field.text = "<b>" + bridge.get_wpm() + "</b> wpm"
                    }


                    Text {
                        id: speed_field
                    }

                    Rectangle {
                        id: pause_indicator
                        height: parent.height
                        width: pause_indicator.height

                        FpsTimer {
                            onTriggered: parent.color = bridge.is_playing() ? "green" : "#BC0022"
                        }

                        color: "#DB6B88"
                    }
                }

                Row {
                    spacing: 75
                    topPadding: 5
                    bottomPadding: 0

                    Text {
                        id: input_file_text
                        text: "File: "
                    }

                    TextField {
                        id: filenamefield
                        anchors.verticalCenter: input_file_text.verticalCenter
                        text: bridge.get_default_filename()

                        FpsTimer {
                            onTriggered: bridge.can_read() ? bridge.read_filename(filenamefield.text) : null
                        }

                        background: Rectangle {
                            radius: 2
                            implicitWidth: 100
                            implicitHeight: 24
                            border.color: "#333"
                            border.width: 1
                        }
                    }
                }

                Row {
                    spacing: 20
                    topPadding: 0

                    Text {
                        text: ""
                        color: '#BC0022'

                        FpsTimer {
                            onTriggered: parent.text = (bridge.error_happened() ? bridge.get_error() : null)
                        }
                    }
                }
            }
        }
    }
}