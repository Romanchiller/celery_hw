import cv2
from cv2 import dnn_superres


upscale_model = dnn_superres.DnnSuperResImpl_create().readModel('EDSR_x2.pb')


def upscale(input_path: str, output_path: str,) -> str:
    """
    :param input_path: путь к изображению для апскейла
    :param output_path:  путь к выходному файлу
    :param model_path: путь к ИИ модели
    :return:
    """
    scaler = upscale_model
    scaler.setModel("edsr", 2)
    image = cv2.imread(input_path)
    result = scaler.upsample(image)
    cv2.imwrite(output_path, result)
    return f'{output_path}'

def example():
    upscale('lama_300px.png', 'lama_.png')


if __name__ == '__main__':
    example()
