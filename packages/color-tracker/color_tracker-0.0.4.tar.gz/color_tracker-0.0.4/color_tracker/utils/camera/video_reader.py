import cv2
import imageio

from color_tracker.utils.camera.base_camera import Camera
from color_tracker.utils.helpers import resize_img


class VideoReader(Camera):
    def __init__(self, video_name):
        super().__init__()
        self._current_frame_number = 0
        self._full_length = 0
        self._video_name = video_name

    def _init_camera(self):
        super()._init_camera()
        self._cam = imageio.get_reader(self._video_name, "ffmpeg")
        self._full_length = self._cam.get_length()
        try:
            self._frame = self._cam.get_data(self._current_frame_number)
            self._frame = self._convert_frame_from_rgb_to_bgr(self._cam.get_data(self._current_frame_number))
            self._ret = True
        except Exception:
            self._ret = False
        if not self._ret:
            raise Exception("No camera feed")
        self._frame_height, self._frame_width, c = self._frame.shape
        return self._ret

    def _read_from_camera(self):
        super()._read_from_camera()
        try:
            self._frame = resize_img(
                cv2.flip(self._convert_frame_from_rgb_to_bgr(self._cam.get_data(self._current_frame_number)),
                         1), 640, 480)
            self._ret = True
            self._current_frame_number += 1
            if self._full_length - 50 <= self._current_frame_number:
                self._current_frame_number = 0
        except Exception:
            self._ret = False

        if self._ret:
            if self._auto_undistortion:
                self._frame = self._undistort_image(self._frame)
            return True, self._frame
        else:
            return False, None

    def _convert_frame_from_rgb_to_bgr(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image

    def release(self):
        super().release()
