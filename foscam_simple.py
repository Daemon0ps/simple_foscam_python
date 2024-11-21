import cv2
import numpy as np
import keyring
from threading import Thread
import multiprocessing

class VideoStreamWidget(object):
    def __init__(self, src=0):
        self._fc:int=0
        self.capture = cv2.VideoCapture(src)
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
        self.img1:np.uint8=[[[]]]

    def update(self):
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()

    def show_frame(self):
        if self._fc % 60 == 0:
            cv2.namedWindow('IPCAM',cv2.WINDOW_FREERATIO)
            img = np.uint8(self.frame)
            self.img1 = img
            if self.status:
                cv2.imshow('IPCAM', img)
            key = cv2.waitKey(100)

    def maintain_aspect_ratio_resize(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))
        return cv2.resize(image, dim, interpolation=inter)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    USER:str = keyring.get_password('foscam','user')
    PASSWORD:str = keyring.get_password('foscam','password')
    IP_ADDR:str = keyring.get_password('foscam','ip_addr')
    PORT_NUM:str = keyring.get_password('foscam','port_num')
    CAM_ADDR:str = str(f'rtsp://{USER}:{PASSWORD}@{IP_ADDR}:{PORT_NUM}/videoMain')
    stream_link = CAM_ADDR
    video_stream_widget = VideoStreamWidget(stream_link)
    while True:
        try:
            video_stream_widget.show_frame()
        except AttributeError:
            pass
