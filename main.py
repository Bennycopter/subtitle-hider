import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizeGrip, QMenu, QLabel, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPoint, QEvent
from PySide6.QtGui import QCursor, QIcon, QPixmap, QPainter, QColor
from BlurWindow.blurWindow import blur

class DraggableBlurWindow(QWidget):
    def __init__(self):
        super(DraggableBlurWindow, self).__init__()

        # Set window attributes
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.resize(800, 400)  # Adjust size as needed
        
        self.setWindowIcon(QIcon('icon.ico'))

        # Apply blur effect
        blur(self.winId())

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
            Right-click to <strong>change color</strong> or <strong>close</strong>
        """, self)
        self.text_label.setAlignment(Qt.AlignCenter)  # Center the text inside the label
        self.text_label.setAttribute(Qt.WA_TransparentForMouseEvents)
        layout.addWidget(self.text_label, alignment=Qt.AlignCenter)  # Center the label in the layout
        self.setLayout(layout)

        # Give the text label a blur
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(0)
        effect.setColor(QColor("#FFFFFF"))
        effect.setOffset(1, 0)
        self.text_label.setGraphicsEffect(effect)

        # Default background color
        self.bg_color = QColor(0, 0, 0, 0)

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

    def mouseMoveEvent(self, event):
        # Drag the window while the left button is pressed
        if self.is_dragging:
            self.move(QCursor.pos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        # Stop dragging on mouse button release
        if event.button() == Qt.LeftButton:
            self.is_dragging = False

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        
        black_action = context_menu.addAction("Black")
        white_action = context_menu.addAction("White")
        blur_action = context_menu.addAction("Blur")
        close_action = context_menu.addAction("Close")
        action = context_menu.exec(event.globalPos())
        
        if action == black_action:
            print("Black")
            self.bg_color = QColor(0, 0, 0, 255)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.text_label.setStyleSheet("color: white;")
            self.update()
        elif action == white_action:
            print("White")
            self.bg_color = QColor(255, 255, 255, 255)
            self.setAttribute(Qt.WA_TranslucentBackground, False)
            self.text_label.setStyleSheet("color: black;")
            self.update()
        elif action == blur_action:
            print("Blur")
            self.bg_color = QColor(0, 0, 0, 0)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.text_label.setStyleSheet("color: black;")
            self.update()
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
        self.text_label.show()
        for grip in self.grips:
            grip.show()

    def hideTipsAndGrips(self):
        self.text_label.hide()
        for grip in self.grips:
            grip.hide()

    def paintEvent(self, event):
        # Manually clear the background by painting the background (or transparent) color
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(self.rect(), self.bg_color)
        painter.end()

        # Call the default paint event to draw the widgets
        super().paintEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DraggableBlurWindow()
    window.show()
    sys.exit(app.exec())
