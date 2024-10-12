# Subtitle Hider

This program adds a box to your screen that can be used to hide/blur unwanted hard-coded subtitles on videos.

***If you wish to support me and my work, you can purchase a subscription to our website, [Comprehensible Japanese](https://cijapanese.com), and get access to nearly 1000 Japanese learning videos based on comprehensible input.***

## Example of Subtitle Blurring

[![image](https://github.com/user-attachments/assets/d7e7d7f5-5912-47e5-8f07-059c0a2ebb4d)](https://cijapanese.com/video/1/Snowman)

Image source: [雪だるま Snowman - Comprehensible Japanese](https://cijapanese.com/video/1/Snowman)

## Features

- Draggable
- Resizable
- Three background options: Blur (default), Black, and White
- Always on top of other windows
- Click on the box to show what's underneath it

## Windows Instructions

- [Download the program here](https://github.com/Bennycopter/subtitle-hider/releases)
- Extract the files
- Double-click the .exe
- (Optional) replace the icon.ico file with your own icon

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

## Copyright Notice

The icon file `icon.ico` is copyright Comprehensible Japanese (https://cijapanese.com).
