import mammoth
import base64
from pathlib import Path
import shortuuid
import datetime
import os


class QtConvert:

    @staticmethod
    def convert_image(image):
        """
        "data:{0};base64,{1}".format(image.content_type, encoded_src)
        :param image:
        :return:
        """
        with image.open() as image_bytes:
            encoded_src = base64.b64encode(image_bytes.read()).decode("ascii")
        base_path = Path('media/article/') / datetime.datetime.now().strftime('%Y%m%d')
        if not base_path.is_dir():
            os.makedirs(base_path)
        image_path = base_path.joinpath(shortuuid.uuid() + '.jpg')
        with open(str(image_path), 'wb') as image_file:
            image_file.write(base64.b64decode(encoded_src))
        return {
            "src": '/' + str(image_path)
        }

    @staticmethod
    def convert_html_text(doc_path):
        with open(doc_path, 'rb') as docx_file:
            result = mammoth.convert_to_html(docx_file, convert_image=mammoth.images.img_element(QtConvert.convert_image))
        return result.value
