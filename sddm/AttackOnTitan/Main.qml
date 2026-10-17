/*
    Attack on Titan SDDM theme
    SPDX-FileCopyrightText: 2026 Shubhwtf
    SPDX-License-Identifier: GPL-3.0-or-later
*/
import QtQuick
import QtQuick.Controls

Rectangle {
    id: root
    width: 1920
    height: 1080
    color: "#0c0a09"

    readonly property color parchment: "#e8dcc4"
    readonly property color dim: "#b3a68f"
    readonly property color muted: "#7a6e60"
    readonly property color brass: "#c9a14a"
    readonly property color crimson: "#b8302a"
    readonly property color crimsonHi: "#d23a2f"
    readonly property real u: Math.max(0.6, height / 1080)

    property int userIndex: userModel.lastIndex >= 0 ? userModel.lastIndex : 0
    property int sessionIndex: sessionModel.lastIndex >= 0 ? sessionModel.lastIndex : 0
    property string currentUser: userList.currentItem ? userList.currentItem.userName : userModel.lastUser

    FontLoader { id: cinzel; source: "assets/Cinzel.ttf" }

    Connections {
        target: sddm
        function onLoginFailed() {
            password.text = "";
            errorText.text = "The wall holds. Try again.";
            shake.start();
            password.forceActiveFocus();
        }
        function onLoginSucceeded() {
            errorText.text = "";
        }
    }

    Image {
        id: bg
        anchors.fill: parent
        source: config.background
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
    }

    // darken the left side where the form lives
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: "#f20c0a09" }
            GradientStop { position: 0.38; color: "#d90c0a09" }
            GradientStop { position: 0.62; color: "#400c0a09" }
            GradientStop { position: 1.0; color: "#000c0a09" }
        }
    }

    // ---------------------------------------------------------------- clock
    Column {
        id: clockCol
        x: 120 * u
        y: 120 * u
        spacing: 6 * u

        Text {
            id: time
            color: root.parchment
            font.family: cinzel.name
            font.weight: Font.Bold
            font.pixelSize: 112 * u
            text: Qt.formatTime(new Date(), "hh:mm")
        }
        Rectangle { width: 90 * u; height: 2; color: root.crimson }
        Text {
            id: date
            color: root.brass
            font.family: cinzel.name
            font.pixelSize: 26 * u
            font.letterSpacing: 6 * u
            text: Qt.formatDate(new Date(), "dddd, d MMMM").toUpperCase()
        }
        Timer {
            interval: 1000; running: true; repeat: true
            onTriggered: {
                time.text = Qt.formatTime(new Date(), "hh:mm");
                date.text = Qt.formatDate(new Date(), "dddd, d MMMM").toUpperCase();
            }
        }
    }

    // ---------------------------------------------------------------- login form
    Column {
        id: form
        x: 120 * u
        anchors.verticalCenter: parent.verticalCenter
        anchors.verticalCenterOffset: 80 * u
        width: 460 * u
        spacing: 22 * u

        Row {
            spacing: 22 * u
            Image {
                source: "assets/emblem.svg"
                width: 96 * u; height: 96 * u
                sourceSize.width: width; sourceSize.height: height
            }
            Column {
                anchors.verticalCenter: parent.verticalCenter
                spacing: 4 * u
                Text {
                    text: "SURVEY CORPS"
                    color: root.muted
                    font.family: cinzel.name
                    font.pixelSize: 14 * u
                    font.letterSpacing: 6 * u
                }
                Text {
                    text: userList.currentItem ? userList.currentItem.displayName : root.currentUser
                    color: root.parchment
                    font.family: cinzel.name
                    font.weight: Font.Bold
                    font.pixelSize: 34 * u
                    elide: Text.ElideRight
                    width: form.width - 120 * u
                }
            }
        }

        // user picker, only shown when there is more than one soldier
        ListView {
            id: userList
            width: form.width
            height: count > 1 ? 34 * u : 0
            visible: count > 1
            orientation: ListView.Horizontal
            spacing: 18 * u
            clip: true
            model: userModel
            currentIndex: root.userIndex
            delegate: Text {
                required property int index
                required property string name
                required property string realName
                readonly property string userName: name
                readonly property string displayName: realName.length > 0 ? realName : name
                text: displayName
                color: ListView.isCurrentItem ? root.brass : root.muted
                font.family: cinzel.name
                font.pixelSize: 18 * u
                font.underline: ListView.isCurrentItem
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: { userList.currentIndex = index; password.forceActiveFocus(); }
                }
            }
        }

        Item {
            id: fieldBox
            width: form.width
            height: 56 * u

            SequentialAnimation {
                id: shake
                NumberAnimation { target: fieldBox; property: "x"; to: 12; duration: 50 }
                NumberAnimation { target: fieldBox; property: "x"; to: -12; duration: 70 }
                NumberAnimation { target: fieldBox; property: "x"; to: 8; duration: 60 }
                NumberAnimation { target: fieldBox; property: "x"; to: 0; duration: 50 }
            }

            Rectangle {
                anchors.fill: parent
                color: "#cc141110"
                border.width: 1
                border.color: password.activeFocus ? root.brass : "#2e2722"
                radius: 4 * u
                Behavior on border.color { ColorAnimation { duration: 200 } }
            }

            TextField {
                id: password
                anchors.left: parent.left
                anchors.right: loginBtn.left
                anchors.verticalCenter: parent.verticalCenter
                anchors.leftMargin: 18 * u
                anchors.rightMargin: 8 * u
                echoMode: TextInput.Password
                passwordCharacter: "◆"
                placeholderText: "Password"
                placeholderTextColor: root.muted
                color: root.parchment
                selectionColor: root.crimson
                font.pixelSize: 20 * u
                font.letterSpacing: 2 * u
                background: Item {}
                focus: true
                Keys.onReturnPressed: root.doLogin()
                Keys.onEnterPressed: root.doLogin()
            }

            Item {
                id: loginBtn
                width: 56 * u; height: 56 * u
                anchors.right: parent.right
                Rectangle {
                    anchors.centerIn: parent
                    width: 26 * u; height: 26 * u
                    rotation: 45
                    color: btnArea.containsMouse ? root.crimsonHi : root.crimson
                    border.color: btnArea.pressed ? root.parchment : "transparent"
                    Behavior on color { ColorAnimation { duration: 150 } }
                }
                Text {
                    anchors.centerIn: parent
                    text: "›"
                    color: root.parchment
                    font.pixelSize: 26 * u
                    font.bold: true
                }
                MouseArea {
                    id: btnArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.doLogin()
                }
            }
        }

        Text {
            id: errorText
            text: ""
            color: root.crimsonHi
            font.family: cinzel.name
            font.pixelSize: 16 * u
            font.letterSpacing: 2 * u
            height: 20 * u
        }
    }

    // ---------------------------------------------------------------- bottom bar
    Row {
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.leftMargin: 120 * u
        anchors.bottomMargin: 60 * u
        spacing: 34 * u

        Text {
            id: sessionLabel
            property int idx: root.sessionIndex
            color: sessionArea.containsMouse ? root.brass : root.dim
            font.family: cinzel.name
            font.pixelSize: 16 * u
            font.letterSpacing: 3 * u
            text: "◇  " + (sessionList.currentItem ? sessionList.currentItem.sname : "Session")
            MouseArea {
                id: sessionArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                onClicked: root.sessionIndex = (root.sessionIndex + 1) % sessionModel.rowCount()
            }
            ListView {
                id: sessionList
                width: 1; height: 1
                opacity: 0
                cacheBuffer: 10000
                model: sessionModel
                currentIndex: root.sessionIndex
                delegate: Item { required property string name; readonly property string sname: name; width: 1; height: 1 }
            }
        }
    }

    Row {
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 80 * u
        anchors.bottomMargin: 60 * u
        spacing: 34 * u

        Repeater {
            model: [
                { label: "Suspend", enabled: sddm.canSuspend, action: function () { sddm.suspend(); } },
                { label: "Restart", enabled: sddm.canReboot, action: function () { sddm.reboot(); } },
                { label: "Shut down", enabled: sddm.canPowerOff, action: function () { sddm.powerOff(); } }
            ]
            delegate: Text {
                required property var modelData
                visible: modelData.enabled
                text: modelData.label.toUpperCase()
                color: area.containsMouse ? root.crimsonHi : root.dim
                font.family: cinzel.name
                font.pixelSize: 15 * u
                font.letterSpacing: 4 * u
                Behavior on color { ColorAnimation { duration: 150 } }
                MouseArea {
                    id: area
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: modelData.action()
                }
            }
        }
    }

    function doLogin() {
        errorText.text = "";
        sddm.login(root.currentUser, password.text, root.sessionIndex);
    }

    Component.onCompleted: password.forceActiveFocus()
}
