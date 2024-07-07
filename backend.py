"""Backend module"""

import cv2
import numpy as np
from typing import Tuple
import torch
import torchvision.transforms as transforms


def load_image_from_disk(file_path: str) -> np.ndarray:
    """
    Загрузка изображения с указанного пути.
    :param file_path: путь к файлу изображения
    :return: изображение в формате numpy array
    """
    img = cv2.imread(file_path)
    if img is None:
        raise ValueError("Не удалось загрузить изображение")
    return img


def capture_image_from_webcam() -> np.ndarray:
    """
    Захват изображения с веб-камеры.
    :return: изображение в формате numpy array
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise ValueError("Не удалось подключиться к веб-камере")
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise ValueError("Не удалось захватить изображение с веб-камеры, проверти подключение")
    return frame


def get_image_with_channels(img: np.ndarray, channel: str) -> np.ndarray:
    """
    Показ выбранного цветового канала изображения.
    :param img: исходное изображение
    :param channel: цветовой канал ("red", "green", "blue")
    :return: изображение с выделенным цветовым каналом
    """
    img_tensor = transforms.ToTensor()(img)
    channels = img_tensor.split(1, dim=0)
    blank = torch.zeros_like(channels[0])
    if channel == "red":
        img_channel = torch.cat([channels[0], blank, blank], dim=0)
    elif channel == "green":
        img_channel = torch.cat([blank, channels[1], blank], dim=0)
    else:
        img_channel = torch.cat([blank, blank, channels[2]], dim=0)
    img_channel = transforms.ToPILImage()(img_channel)
    img_channel = cv2.cvtColor(np.array(img_channel), cv2.COLOR_RGB2BGR)
    return img_channel


def get_image_with_gaussian_blur(img: np.ndarray, kernel_size: int) -> np.ndarray:
    """
    Применение размытия по Гауссу к изображению.
    :param img: исходное изображение
    :param kernel_size: размер ядра (должен быть нечетным числом)
    :return: размытое изображение
    """
    if kernel_size % 2 == 0:
        raise ValueError("Размер ядра должен быть нечетным числом")
    blurred_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    return blurred_img


def get_grey_channel_img(img: np.ndarray) -> np.ndarray:
    """
    Конвертация изображения в оттенки серого.
    :param img: исходное изображение
    :return: изображение в оттенках серого
    """
    img_tensor = transforms.ToTensor()(img)
    gray_tensor = img_tensor.mean(dim=0, keepdim=True)
    img_gray = torch.cat([gray_tensor, gray_tensor, gray_tensor], dim=0)
    img_gray = transforms.ToPILImage()(img_gray)
    img_gray = cv2.cvtColor(np.array(img_gray), cv2.COLOR_RGB2BGR)
    return img_gray


def get_image_with_line(img: np.ndarray, start_point: Tuple[int, int], end_point: Tuple[int, int],
                        thickness: int) -> np.ndarray:
    """
    Рисование линии на изображении.
    :param img: исходное изображение
    :param start_point: координаты начала линии (x1, y1)
    :param end_point: координаты конца линии (x2, y2)
    :param thickness: толщина линии
    :return: изображение с нарисованной линией
    """
    img_with_line = img.copy()
    color = (0, 255, 0)  # Зеленый цвет
    cv2.line(img_with_line, start_point, end_point, color, thickness)
    return img_with_line
