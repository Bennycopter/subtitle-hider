import sys
from PySide6.QtWidgets import QApplication, QWidget, QSizeGrip, QMenu
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QCursor, QIcon
from BlurWindow.blurWindow import blur

class DraggableBlurWindow(QWidget):
    def __init__(self):
        super(DraggableBlurWindow, self).__init__()

        # Set window attributes
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.resize(800, 200)
        
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
            grip.setStyleSheet("background-color: transparent;")  # Make grips transparent
            self.grips.append(grip)
    
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
        close_action = context_menu.addAction("Close")
        action = context_menu.exec(event.globalPos())
        if action == close_action:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DraggableBlurWindow()
    window.show()
    sys.exit(app.exec())
    
