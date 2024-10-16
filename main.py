import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizeGrip, QMenu, QLabel, QVBoxLayout, QGraphicsDropShadowEffect, QSizePolicy
from PySide6.QtCore import Qt, QPoint, QEvent, QSettings, QSize
from PySide6.QtGui import QCursor, QIcon, QPixmap, QPainter, QColor
from BlurWindow.blurWindow import GlobalBlur

class DraggableBlurWindow(QWidget):
    def __init__(self):
        super(DraggableBlurWindow, self).__init__()

        # Load settings
        self.settings = QSettings("SubtitleHider", "DraggableBlurWindow")
        self.resize(self.settings.value("size", QSize(800, 400)))
        previous_position = self.settings.value("pos", False)
        if previous_position:
            self.move(previous_position)
        # Default background color
        self.bg_color = self.settings.value("background-color", QColor(0, 0, 0, 0))
        self.text_color = self.settings.value("text-color", "black")
        self.always_hide_instructions = self.settings.value("always-hide-instructions", "false")
        self.always_hide_grips = self.settings.value("always-hide-grips", "false")
        self.always_hide_instructions = string_to_bool(self.always_hide_instructions)
        self.always_hide_grips = string_to_bool(self.always_hide_grips)

        # Set window attributes
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('icon.ico'))

        # Apply blur effect
        GlobalBlur(self.winId())

        # Set a transparent background after applying blur
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Variables for dragging
        self.is_dragging = False
        self.drag_position = QPoint()

        # Initialize grips for resizing
        self.gripSize = 16
        self.grips = []
        for i in range(4):
            grip = QSizeGrip(self)
            grip.resize(self.gripSize, self.gripSize)
            self.grips.append(grip)

        # Create a layout and add it to this widget
        layout = QVBoxLayout(self)

        # Add text label
        self.text_label = QLabel("""
            Click+drag middle to <strong>move</strong><br>
            Click+drag corners to <strong>resize</strong><br>
            Click without dragging to <strong>temporarily hide</strong><br>
            Right-click to <strong>change color</strong> or <strong>close</strong>
        """, self)
        self.text_label.setAlignment(Qt.AlignCenter)  # Center the text inside the label
        self.text_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.text_label, alignment=Qt.AlignCenter)  # Center the label in the layout
        self.setLayout(layout)
        self.text_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.text_label.setStyleSheet("color: "+self.text_color+";")

        # Give the text label a blur
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(0)
        effect.setColor(QColor("#FFFFFF"))
        effect.setOffset(1, 0)
        self.text_label.setGraphicsEffect(effect)

        self.hideTipsAndGrips()
        self.showTipsAndGrips()

    def resizeEvent(self, event):
        super(DraggableBlurWindow, self).resizeEvent(event)
        rect = self.rect()
        # Set the positions for each grip
        self.grips[0].move(0, 0)  # Top left
        self.grips[1].move(rect.right() - self.gripSize, 0)  # Top right
        self.grips[2].move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)  # Bottom right
        self.grips[3].move(0, rect.bottom() - self.gripSize)  # Bottom left

    def mousePressEvent(self, event):
        # Start dragging on left mouse button press
        if event.button() == Qt.LeftButton:
            self.is_dragging = True
            self.drag_position = QCursor.pos() - self.frameGeometry().topLeft()
            self.setWindowOpacity(0)

    def mouseMoveEvent(self, event):
        # Drag the window while the left button is pressed
        if self.is_dragging:
            self.setWindowOpacity(1)
            self.move(QCursor.pos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        # Stop dragging on mouse button release
        if event.button() == Qt.LeftButton:
            self.is_dragging = False
            self.setWindowOpacity(1)

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)

        blur_action = context_menu.addAction("Blur")
        black_action = context_menu.addAction("Black")
        white_action = context_menu.addAction("White")
        context_menu.addSeparator()
        hide_instructions = context_menu.addAction("Always hide instructions")
        hide_instructions.setCheckable(True)
        hide_instructions.setChecked(self.always_hide_instructions)
        hide_grips = context_menu.addAction("Always hide grips")
        hide_grips.setCheckable(True)
        hide_grips.setChecked(self.always_hide_grips)
        context_menu.addSeparator()
        close_action = context_menu.addAction("Close")
        
        action = context_menu.exec(event.globalPos())
        
        if action == black_action:
            self.bg_color = QColor(0, 0, 0, 255)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.text_label.setStyleSheet("color: white;")
            self.text_color = "white";
            self.update()
        elif action == white_action:
            self.bg_color = QColor(255, 255, 255, 255)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.text_label.setStyleSheet("color: black;")
            self.text_color = "black";
            self.update()
        elif action == blur_action:
            self.bg_color = QColor(0, 0, 0, 0)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.text_label.setStyleSheet("color: black;")
            self.text_color = "black";
            self.update()
        elif action == hide_instructions:
            if hide_instructions.isChecked():
                self.always_hide_instructions = True
            else:
                self.always_hide_instructions = False
            self.hideTipsAndGrips()
            self.showTipsAndGrips()
        elif action == hide_grips:
            if hide_grips.isChecked():
                self.always_hide_grips = True
            else:
                self.always_hide_grips = False
            self.hideTipsAndGrips()
            self.showTipsAndGrips()
        elif action == close_action:
            self.close()

    def event(self, event):
        # Window focus
        if event.type() == QEvent.WindowActivate:
            self.showTipsAndGrips()
        # Window loses focus
        elif event.type() == QEvent.WindowDeactivate:
            self.hideTipsAndGrips()
        return super(DraggableBlurWindow, self).event(event)

    def showTipsAndGrips(self):
        if self.always_hide_instructions == False:
            self.text_label.show()
        if self.always_hide_grips == False:
            for grip in self.grips:
                grip.setStyleSheet("")

    def hideTipsAndGrips(self):
        self.text_label.hide()
        for grip in self.grips:
            grip.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Fully transparent

    def paintEvent(self, event):
        # Manually clear the background by painting the background (or transparent) color
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(self.rect(), self.bg_color)
        painter.end()

        # Call the default paint event to draw the widgets
        super().paintEvent(event)

    def closeEvent(self, event):
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.setValue("background-color", self.bg_color)
        self.settings.setValue("text-color", self.text_color)
        self.settings.setValue("always-hide-instructions", self.always_hide_instructions)
        self.settings.setValue("always-hide-grips", self.always_hide_grips)
        super().closeEvent(event)

def string_to_bool(s):
    if s.lower() == "true":
        return True
    elif s.lower() == "false":
        return False
    else:
        raise ValueError("Input must be 'true' or 'false'")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DraggableBlurWindow()
    window.show()
    sys.exit(app.exec())
