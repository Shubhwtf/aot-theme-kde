/*
    SPDX-FileCopyrightText: 2026 Shubhwtf
    SPDX-License-Identifier: GPL-3.0-or-later
*/
import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    color: "#0c0a09"

    property int stage
    readonly property var mottos: [
        "Dedicate your heart.",
        "Beyond the walls, the sea.",
        "Tatakae.",
        "The world is cruel, and beautiful.",
        "Advance. Do not look back."
    ]

    onStageChanged: {
        if (stage == 2) {
            intro.start();
        } else if (stage == 5) {
            outro.start();
        }
    }

    FontLoader { id: cinzel; source: "images/Cinzel.ttf" }

    Image {
        anchors.fill: parent
        source: "images/background.jpg"
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
    }

    Item {
        id: content
        anchors.fill: parent
        opacity: 0

        Image {
            id: emblem
            readonly property real size: Math.round(root.height * 0.32)
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            anchors.verticalCenterOffset: -root.height * 0.07
            source: "images/emblem.svg"
            sourceSize.width: size
            sourceSize.height: size
            asynchronous: true
            scale: 0.92

            SequentialAnimation on opacity {
                loops: Animation.Infinite
                running: Kirigami.Units.longDuration > 1
                NumberAnimation { from: 1; to: 0.82; duration: 1600; easing.type: Easing.InOutSine }
                NumberAnimation { from: 0.82; to: 1; duration: 1600; easing.type: Easing.InOutSine }
            }
        }

        Text {
            id: title
            anchors.top: emblem.bottom
            anchors.topMargin: root.height * 0.045
            anchors.horizontalCenter: parent.horizontalCenter
            text: "SHINZOU WO SASAGEYO"
            color: "#c9a14a"
            font.family: cinzel.name
            font.weight: Font.Bold
            font.pixelSize: Math.round(root.height * 0.026)
            font.letterSpacing: font.pixelSize * 0.55
        }

        Rectangle {
            id: track
            anchors.top: title.bottom
            anchors.topMargin: root.height * 0.035
            anchors.horizontalCenter: parent.horizontalCenter
            width: Math.round(root.width * 0.2)
            height: 2
            color: "#2e2722"

            Rectangle {
                height: parent.height
                width: parent.width * Math.min(1, root.stage / 6)
                color: "#b8302a"
                Behavior on width { NumberAnimation { duration: 600; easing.type: Easing.OutCubic } }

                Rectangle {
                    anchors.right: parent.right
                    anchors.verticalCenter: parent.verticalCenter
                    width: 8; height: 8; rotation: 45
                    color: "#e8dcc4"
                    visible: parent.width > 0
                }
            }
        }

        Text {
            anchors.top: track.bottom
            anchors.topMargin: root.height * 0.03
            anchors.horizontalCenter: parent.horizontalCenter
            text: root.mottos[Math.floor(Math.random() * root.mottos.length)]
            color: "#b3a68f"
            opacity: 0.85
            font.family: cinzel.name
            font.pixelSize: Math.round(root.height * 0.016)
            font.letterSpacing: 2
        }
    }

    ParallelAnimation {
        id: intro
        OpacityAnimator { target: content; from: 0; to: 1; duration: 900; easing.type: Easing.InOutQuad }
        ScaleAnimator { target: emblem; from: 0.92; to: 1; duration: 1400; easing.type: Easing.OutCubic }
    }

    OpacityAnimator {
        id: outro
        target: content
        from: 1; to: 0
        duration: 500
        easing.type: Easing.InQuad
    }
}
