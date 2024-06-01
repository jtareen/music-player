from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QWidget, QListWidget, QListWidgetItem, QMessageBox, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor
from pygame import mixer
import pygame, os
from scripts.songs import SongList

basedir = os.path.dirname(__file__)

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Metro Music Player")
        self.setGeometry(300, 300, 600, 300)
        self.setStyleSheet("background-color: #5d5d5d;")

        mixer.init()

        self.song_list = None
        self.current_index = -1
        self.is_playing = False

        self.play_icon = QIcon(os.path.join(basedir, "../assets/play.png"))
        self.pause_icon = QIcon(os.path.join(basedir, "../assets/pause.png"))
        self.next_icon = QIcon(os.path.join(basedir, "../assets/next.png"))
        self.prev_icon = QIcon(os.path.join(basedir, "../assets/prev.png"))

        self.play_pause_button = QPushButton(self)
        self.play_pause_button.setIcon(self.play_icon)
        self.play_pause_button.setFixedSize(100, 100)  # Set fixed size for circular shape
        self.play_pause_button.setIconSize(QSize(80, 80))
        self.play_pause_button.clicked.connect(self.play_pause_music)

        self.next_button = QPushButton(self)
        self.next_button.setIcon(self.next_icon)
        self.next_button.setFixedSize(75, 75)  # Set fixed size for circular shape
        self.next_button.setIconSize(QSize(55, 55))
        self.next_button.clicked.connect(self.play_next_song)

        self.prev_button = QPushButton(self)
        self.prev_button.setIcon(self.prev_icon)
        self.prev_button.setFixedSize(75, 75)  # Set fixed size for circular shape
        self.prev_button.setIconSize(QSize(55, 55))
        self.prev_button.clicked.connect(self.play_previous_song)

        self.status_label = QLabel("No file loaded", self)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.song_list_widget = QListWidget(self)
        self.song_list_widget.itemDoubleClicked.connect(self.song_double_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.play_pause_button)
        button_layout.addWidget(self.next_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.song_list_widget)
        main_layout.addWidget(self.status_label)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        self.apply_styles()  # Apply styles to buttons

        self.load_songs("D:\\")  # Set your music directory path here

    def apply_styles(self):
        button_style = """
        QPushButton {
            border: none;
            background-color: #b0b0b0;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        QPushButton#play_pause_button {
            border-radius: 50px;  /* (width + height) / 4 for 100x100 */
        }
        QPushButton#next_button, QPushButton#prev_button {
            border-radius: 37px;  /* (width + height) / 4 for 75x75 */
        }
        """
        self.play_pause_button.setObjectName("play_pause_button")
        self.next_button.setObjectName("next_button")
        self.prev_button.setObjectName("prev_button")
        self.setStyleSheet(button_style)

        # Apply shadow effect
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setXOffset(2)
        shadow_effect.setYOffset(2)
        shadow_effect.setColor(QColor(0, 0, 0, 160))

        self.play_pause_button.setGraphicsEffect(shadow_effect)

        shadow_effect2 = QGraphicsDropShadowEffect()
        shadow_effect2.setBlurRadius(10)
        shadow_effect2.setXOffset(2)
        shadow_effect2.setYOffset(2)
        shadow_effect2.setColor(QColor(0, 0, 0, 160))

        self.next_button.setGraphicsEffect(shadow_effect2)

        shadow_effect3 = QGraphicsDropShadowEffect()
        shadow_effect3.setBlurRadius(10)
        shadow_effect3.setXOffset(2)
        shadow_effect3.setYOffset(2)
        shadow_effect3.setColor(QColor(0, 0, 0, 160))

        self.prev_button.setGraphicsEffect(shadow_effect3)

    def load_songs(self, directory):
        self.song_list = SongList(directory)
        self.song_list_widget.clear()
        for song in self.song_list:
            item = QListWidgetItem(song.getName())
            self.song_list_widget.addItem(item)
        self.status_label.setText(f"Loaded {len(self.song_list)} songs")

    def play_pause_music(self):
        if self.current_index == -1 and self.song_list:
            self.current_index = 0

        if self.current_index != -1:
            if not self.is_playing:
                self.is_playing = True
                self.play_pause_button.setIcon(self.pause_icon)
                self.play_pause_button.setIconSize(QSize(80, 80))
                self.play_song()
            else:
                mixer.music.pause()
                self.play_pause_button.setIcon(self.play_icon)
                self.play_pause_button.setIconSize(QSize(80, 80))
                self.is_playing = False

    def play_song(self):
        if self.current_index != -1 and self.song_list:
            song = self.song_list[self.current_index]
            self.status_label.setText(f"Playing: {song.getName()}")
            self.play_pause_button.setIcon(self.pause_icon)
            self.play_pause_button.setIconSize(QSize(80, 80))
            self.song_list_widget.setCurrentRow(self.current_index)
            try:
                mixer.music.load(song.getPath())
                mixer.music.play()
            except pygame.error as e:
                self.show_error_dialog(f"Failed to load {song.getName()}: {e}")
                self.play_pause_button.setIcon(self.play_icon)
                self.play_pause_button.setIconSize(QSize(80, 80))
                self.is_playing = False

    def play_next_song(self):
        if self.song_list and self.current_index < len(self.song_list) - 1:
            self.current_index += 1
            self.play_song()

    def play_previous_song(self):
        if self.song_list and self.current_index > 0:
            self.current_index -= 1
            self.play_song()

    def song_double_clicked(self, item):
        self.current_index = self.song_list_widget.row(item)
        self.play_song()

    def show_error_dialog(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()