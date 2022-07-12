# -*- coding: utf-8 -*-
import glob, cv2, os
from PIL import Image
from PyQt5 import QtCore
from pathlib import Path


class Thread(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    video_path = None
    save_path = None
    images = None
    frame_duration = 40
    compression = 0

    def __init__(self, parent=None):
        super().__init__(parent)

    def make_jpgs_from_mp4(self, video_path):
        if '.mp4' in video_path:
            video_capture = cv2.VideoCapture(video_path)
            still_reading, image = video_capture.read()
            frame_count = 0
            while still_reading:
                cv2.imwrite(f"output/{frame_count:03d}.jpg", image)
                still_reading, image = video_capture.read()
                frame_count += 1
        else:
            pass

    def clear(self):
        files = glob.glob(f'output/*.jpg')
        for elem in files:
            os.remove(elem)

    def recursive_optimize(self, rec_count):
        if rec_count > 0:
            self.images.sort()
            for i in self.images:
                if self.images.index(i) % 2 == 0:
                    self.images.remove(i)
                else:
                    continue
            return self.recursive_optimize(rec_count-1)

    def run(self):
        self.clear()
        self.make_jpgs_from_mp4(video_path=self.video_path)
        self.images = glob.glob(f"output/*.jpg")
        self.recursive_optimize(self.compression)
        self.images.sort()
        frames = [Image.open(image) for image in self.images]
        frame_one = frames[0]
        frame_one.save(
            f"{self.save_path}/{Path(self.video_path).stem}.gif",
            format="GIF",
            append_images=frames,
            save_all=True,
            duration=self.frame_duration,
            loop=0
        )
        self.clear()
        self.finished.emit()
