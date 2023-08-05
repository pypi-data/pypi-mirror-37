"""
AUTHOR： YOU
VERSION： V1.0.00
DESC： 邮件操作模块
INTRO： 使用简介
    # 创建邮件对象
    mail = MailSender('smtp.163.com', 465, '填写邮箱登录账号', '填写邮箱登录密码')
    # 添加附件
    mail.add_attachment('../attachment/py08tools-1.00.001.tar.gz')
    mail.add_attachment('../attachment/a.jpg')
    # 定义文本内容
    msg = "<h1>发送的测试邮件</h1>"
    # 发送邮件
    mail.send('测试邮件', 'muwenbin@qikux.com', msg)
    # 关闭
    mail.close()
"""

from smtplib              import SMTP_SSL
from email.mime.text      import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base      import MIMEBase
from email.header         import Header
from email.utils          import parseaddr, formataddr
from email                import encoders
from logging              import debug, info, warning, error, basicConfig, DEBUG


class MailSender(object):
    """邮件发送模块对象"""
    # 发件人
    _from = None
    # 附件列表
    _attachments = []

    def __init__(self, smtp_server, port, email_user, email_password):
        """初始化服务器连接"""
        # 初始化日志模块
        basicConfig(level=DEBUG, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        # 连接服务器
        info("连接指定smtp服务器..{}".format(smtp_server))
        self.smtp_server = SMTP_SSL(smtp_server, port)
        info("服务器连接成功")
        # 登录服务器
        self.__login(email_user, email_password)

    def __login(self, user, pwd):
        """使用指定的账号+密码连接服务器"""
        debug("设置发件人信息")
        self._from = user
        info("开始使用指定账号{}密码{}登录服务器".format(user, pwd))
        try:
            self.smtp_server.login(user, pwd)
        except:
            info("服务器登录失败")
        info("服务器登录成功")

    def add_attachment(self, file):
        """
        添加附件
        :param filename: 添加附件的完整路径/相对路径
        :return: None
        """
        info("邮件中添加附件{}".format(file))
        with open(file, 'rb') as f:
            debug("封装附件对象")
            attach = MIMEBase('application', 'octet-stream')
            debug(attach)
            attach.set_payload(f.read())
            debug(attach)
            attach.add_header('Content-Disposition', 'attachment', filename=('gbk', '', f.name))
            debug("附件开始编码")
            encoders.encode_base64(attach)
            debug("编码完成")
        self._attachments.append(attach)
        info("附件{}添加完成".format(file))

    def send(self, subject, to_addr, content):
        """
        发送邮件
        :param subject: 邮件标题
        :param to_addr: 收件人列表
        :param content: 邮件文本内容
        :return:
        """
        info("开始封装邮件")
        msg = MIMEMultipart()
        debug("开始添加文本邮件内容")
        contents = MIMEText(content, "html", _charset='utf-8')
        debug("开始设置邮件标题")
        msg['Subject'] = subject
        debug("开始设置发件人信息")
        msg['From'] = self._from
        debug("开始设置收件人信息")
        msg['To'] = to_addr
        info("添加附件....")
        for att in self._attachments:
            msg.attach(att)
        info("添加文本内容")
        msg.attach(contents)
        try:
            info("开始发送邮件")
            self.smtp_server.sendmail(self._from, to_addr, msg.as_string())
            info("邮件发送成功")
            return True
        except Exception as e:
            info("邮件发送失败", e)
            return False

    def close(self):
        self.smtp_server.quit()
        info("邮件客户端退出")
























