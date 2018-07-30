import os
import pytesseract

CAPTCHA_DIR = 'captcha-test'
captchas = os.listdir('captcha-test')


for captcha in captchas:
    ocr_str = pytesseract.image_to_string(f'{CAPTCHA_DIR}/{captcha}')
    print(captcha, ocr_str)
