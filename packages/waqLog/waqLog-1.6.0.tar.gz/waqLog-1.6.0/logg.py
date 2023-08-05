import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import os
import time
def opens(*args):
    f = open(*args, encoding='utf-8')
    return f

class mailLog():
    def __init__(self):
        # 第三方 SMTP 服务
        self.mail_host = "smtp.163.com"  # SMTP服务器
        self.mail_user = "wmm1996528@163.com"  # 用户名
        self.mail_pass = "aq918927"  # 授权密码，非登录密码

        self.sender = 'wmm1996528@163.com'  # 发件人邮箱(最好写全, 不然会失败)
        self.receivers = ['912594746@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    def sendEmail(self, title, content):

        message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
        message['From'] = "{}".format(self.sender)
        message['To'] = ",".join(self.receivers)
        message['Subject'] = title

        try:
            smtpObj = smtplib.SMTP_SSL(self.mail_host, 465)  # 启用SSL发信, 端口一般是465
            smtpObj.login(self.mail_user, self.mail_pass)  # 登录验证
            smtpObj.sendmail(self.sender, self.receivers, message.as_string())  # 发送
            print("mail has been send successfully.")
        except smtplib.SMTPException as e:
            print(e)


def logClass(name):
    """
    return logger 对象
    可以将日志按照时间和日期保存到当前目录log下
    :param name: app name
    :return:
    """
    logger = logging.getLogger("mainModule")
    logger.setLevel(level=logging.INFO)
    if not os.path.exists('logs'):
        os.mkdir('logs')
    today = time.strftime('%Y%m%d', time.localtime())
    handler = logging.FileHandler('logs/' + name + '_' + today + '.txt', mode='a', delay=False)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s-%(filename)s[%(lineno)d]-%(levelname)s:%(message)s")
    handler.setFormatter(formatter)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(handler)
    logger.addHandler(console)
    return logger


def retry(retryTime):
    """
    @retry(retryTime=n)
    将函数重试n次！
    :param retryTime:
    :return:
    """

    def wrapper(func):
        def inner(*args, **kwargs):
            n = 0
            while True:
                try:
                    func(*args, **kwargs)
                    n += 1
                except:
                    pass
                if n == retryTime:
                    print(n)

        return inner

    return wrapper


mail = mailLog()
import random

first_num = random.randint(55, 62)
third_num = random.randint(0, 3200)
fourth_num = random.randint(0, 140)


class FakeChromeUA:
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]

    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    @classmethod
    def get_ua(cls):
        return ' '.join(['Mozilla/5.0', random.choice(cls.os_type), 'AppleWebKit/537.36',
                         '(KHTML, like Gecko)', cls.chrome_version, 'Safari/537.36']
                        )


def get_ua():
    return {
        'User-Agent': FakeChromeUA.get_ua(),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

class SingelList():

    def __init__(self):
        self.data = {}

    def add(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]

    def ifexist(self, key):
        try:
            self.data[key]
            return True
        except:
            return False
    def __len__(self):
        return len(self.data)

def sechd(s):
	def outer_wrapper(func):
		def wrapper(*args, **kwargs):
			print(time.time())
			time.sleep(s)
			func(*args, **kwargs)

		return wrapper

	return outer_wrapper

def strips(str):
    return str.strip().replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', '').replace('\r\n', '')

def costtime(func):
	def wrapper(*args, **kwargs):
			t1 = time.time()
			func(*args, **kwargs)
			print('FUNC:%s COST:%s ' % (func.__name__, time.time() - t1))
	return wrapper

