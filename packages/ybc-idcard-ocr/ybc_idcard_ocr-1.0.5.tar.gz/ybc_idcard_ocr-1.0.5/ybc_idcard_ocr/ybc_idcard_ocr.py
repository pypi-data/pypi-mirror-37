import requests
import json
import base64
import os
import cv2
import time
from PIL import Image
import ybc_config


__PREFIX = ybc_config.config['prefix']
__IDCARD_URL = __PREFIX + ybc_config.uri + '/idCardOcr'


__CARD_TYPE = 0


def camera():
    cap = cv2.VideoCapture(0)
    while(1):
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            now = time.localtime()
            filename = str(now.tm_year) + str(now.tm_mon) + str(now.tm_mday) + str(now.tm_hour) + str(now.tm_min) + str(now.tm_sec) + '.jpg'
            cv2.imwrite(filename, frame)
            break
    cap.release()
    cv2.destroyAllWindows()
    return filename


def idcard_info(filename=''):
    """
    功能：身份证识别。

    参数 filename 是当前目录下期望被识别的图片名字，

    返回：识别出的身份证信息。
    """

    if not filename:
        return -1

    url = __IDCARD_URL

    filepath = os.path.abspath(filename)

    files = {
        'file': open(filepath, 'rb')
    }

    data = {
        'cardType': __CARD_TYPE
    }

    for i in range(3):
        r = requests.post(url, files=files, data=data)
        if r.status_code == 200:
            res = r.json()
            if 'result_list' in res:
                res = res['result_list'][0]['data']
                del res['name_confidence_all']
                del res['sex_confidence_all']
                del res['nation_confidence_all']
                del res['birth_confidence_all']
                del res['address_confidence_all']
                del res['id_confidence_all']
                return res

    raise ConnectionError('识别身份证图片失败', r._content)


def main():
    res = idcard_info('test.jpg')
    print(res)


if __name__ == '__main__':
    main()
