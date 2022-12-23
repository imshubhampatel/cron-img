import time
import schedule
import boto3
import asyncio
from pdf2image import convert_from_path, convert_from_bytes
import matplotlib.image as mpimg
import io
import base64
from io import StringIO
import cv2
import PIL.Image
from PIL import Image
import pyperclip


session = boto3.Session(
    aws_access_key_id='AKIAQ34Y5OZLLY47NDFW',
    aws_secret_access_key='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'
)

s3 = session.resource("s3")
s3_client = boto3.client(
    "s3",
    aws_access_key_id='AKIAQ34Y5OZLLY47NDFW',
    aws_secret_access_key='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'
)

hdfctests_bucket = s3.Bucket("hdfctests")
bucket = s3.Bucket('hdfctests')
s3 = boto3.resource('s3', region_name="ap-south-1")


def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


def bytes_to_base64_string(value: bytes) -> str:
    return base64.b64encode(value).decode('ASCII')


def call_cronjob():
    for my_bucket_object in hdfctests_bucket.objects.all():
        s3_object = s3_client.get_object(
            Bucket="hdfctests", Key=my_bucket_object.key)
        data = s3_object['Body'].read()
        jpg_image = convert_from_bytes(data, fmt="jpg")

        print(type(jpg_image[0]))
        bytes_image = image_to_byte_array(jpg_image[0])
        print(type(bytes_image))

        encoded = base64.b64encode(bytes_image)
        data_bytes = base64.b64decode(encoded)
        data_bytes = bytes_to_base64_string(data_bytes)
        print(type(data_bytes))
        pyperclip.copy(data_bytes)
    print("HELLO Func")
    print("HELLO Func")


# schedule.every(1).day.do(call_cronjob)
# schedule.every().hour.do(job)
schedule.every().day.at("15:16").do(call_cronjob)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)

print("HELLO WORLD")
print("HELLO WORLD")

while True:
    schedule.run_pending()
    time.sleep(1)
