from cut import cut_captcha
from captcha import recognize
import setting


captcha_path = setting.DOWNLOAD_Path / '5U62_1539929795.png'
# 如果需要切图
cut_captcha(captcha_path)

code = recognize()
print(code)
