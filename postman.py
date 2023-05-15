import smtplib
import os
from email.mime.text import MIMEText
from configparser import ConfigParser


class Postman:

    def __init__(self, sender, password, server, port):
        self.sender = sender
        self.password = password

        self.server = smtplib.SMTP(server, port)

    def send_email(self, to: str, subject: str, message: str) -> None:
        # self.server.connect()
        self.server.starttls()

        try:
            self._login()
        except Exception as exc:
            print(f"Некорректный адрес или пароль: {exc}")
            return

        mime_message = MIMEText(message)
        if subject:
            mime_message["Subject"] = subject

        try:
            self.server.sendmail(self.sender, to, mime_message.as_string())
        except Exception as exc:
            print(f"Доставить сообщение не удалось: {exc}")
            return
        else:
            print("Письмо отправлено")

    def _login(self) -> None:
        self.server.login(self.sender, self.password)


def get_smtp_config() -> tuple[str, ...]:
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, "email.ini")

    if os.path.exists(config_path):
        smtp_config = ConfigParser()
        smtp_config.read(config_path)
        chapter = "smtp"

        server = smtp_config.get(chapter, "smtp_server")
        port = smtp_config.get(chapter, "smtp_port")
        sender = smtp_config.get(chapter, "from_email")
        password = smtp_config.get(chapter, "from_email_password")

        return server, port, sender, password


def main() -> None:
    server, port, sender, password = get_smtp_config()

    postman = Postman(sender, password, server, port)

    to = input("Введите адрес получателя: ")
    subject = input("Введите тему сообщения (можно оставить пустым): ")
    message = input("Введите сообщение, которое хотите отправить: ")

    postman.send_email(to, subject, message)


if __name__ == '__main__':
    main()
