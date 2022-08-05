# -*- coding: utf-8 -*-
import glob, cv2, os
from PIL import Image
from PyQt5 import QtCore
from pathlib import Path
from io import BytesIO
from tempfile import TemporaryDirectory


class Thread(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    video_path = None
    save_path = None
    images = None
    rec_indexes = []
    frame_duration = 40
    compression = 0

    def __init__(self, parent=None):
        super().__init__(parent)

    def make_jpgs_from_mp4(self, video_path):
        if '.mp4' in video_path:
            video_capture = cv2.VideoCapture(video_path)
            still_reading, image = video_capture.read()
            frame_count = 0
            frames = {}
            while still_reading:
                is_success, buffer = cv2.imencode(".jpg", image)
                frames[frame_count] = BytesIO(buffer)
                still_reading, image = video_capture.read()
                frame_count += 1
            self.images = frames
        else:
            pass

    def optimize(self, rec_count):
        self.indexing()
        self.recursive_enumerate(rec_count)
        new_images = {}
        for elem in self.rec_indexes:
            new_images[elem] = self.images.get(elem)
        self.images = new_images

    def recursive_enumerate(self, rec_count):
        if rec_count > 0:
            for i in self.rec_indexes:
                if self.rec_indexes.index(i) % 2 == 0:
                    self.rec_indexes.remove(i)
                else:
                    continue
            return self.recursive_enumerate(rec_count-1)
        else:
            pass

    def indexing(self):
        for i in self.images:
            self.rec_indexes.append(i)

    def run(self):
        try:
            self.make_jpgs_from_mp4(self.video_path)
            self.optimize(self.compression)
            frames = [Image.open(image) for image in self.images.values()]
            frame_one = frames[0]
            frame_one.save(
                f"{self.save_path}/{Path(self.video_path).stem}.gif",
                format="GIF",
                append_images=frames,
                save_all=True,
                duration=self.frame_duration,
                loop=0
            )
            self.finished.emit()
        except Exception as e:
            print(e)
