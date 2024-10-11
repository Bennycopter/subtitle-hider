# Subtitle Hider

This program adds a blurrable box on your screen that can be used to hide subtitles on videos.

***If you wish to support me and my work, you can purchase a subscription to our website, [Comprehensible Japanese](https://cijapanese.com), and get access to nearly 1000 Japanese learning videos based on comprehensible input.***

## Windows Instructions

- [Download the program here](https://github.com/Bennycopter/subtitle-hider/releases)
- Extract the files
- Double-click the .exe
- (Optional) replace the icon.ico file with your own icon
- Drag the middle of the window to position it.
- Drag the corners of the window to resize it.
- Right-click the window and select "close" to close it.

## Running from source

**Requires Python 3.12.7**

```shell
pip install PySide6 BlurWindow
python main
```

## Compiling into an exe (Windows-only)

```python
pyinstaller --onefile --icon=icon.ico --windowed main.py
```
