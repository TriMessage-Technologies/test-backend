from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import from_email, password
import smtplib


def send_mail(to_email: str, subject: str, content: str, content_type: str = "plain") -> bool:
    """
    Отправляет электронное письмо через SMTP сервер Gmail.

    Args:
        to_email (str): Email адрес получателя
        subject (str): Тема письма
        content (str): Содержание письма
        content_type (str, optional): Тип контента. "plain" для текста, "html" для HTML.
                                     По умолчанию "plain".

    Returns:
        bool: True если письмо отправлено успешно, False в случае ошибки
    """
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(MIMEText(content, content_type))

    try:
        print("Установка соединения с SMTP сервером...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        print("Авторизация на сервере...")
        server.login(from_email, password)
        print("Отправка письма...")
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        print("✅ Письмо успешно отправлено!")
        return True

    except smtplib.SMTPException as smtp_error:
        print(f"❌ Ошибка SMTP при отправке письма: {smtp_error}")
        return False
    except Exception as error:
        print(f"❌ Неожиданная ошибка при отправке письма: {error}")
        return False


def main():
    """
    Основная функция для тестирования отправки писем.
    """
    test_recipient = "straight12345678900987654321@gmail.com"
    test_subject = "Тестовое письмо из Python"
    test_content = """
    Здравствуйте!

    Это тестовое письмо, отправленное с помощью Python скрипта.

    С уважением,
    Автоматизированная система
    """

    print(f"Отправка тестового письма на: {test_recipient}")
    print(f"Тема: {test_subject}")
    print("-" * 50)

    success = send_mail(
        to_email=test_recipient,
        subject=test_subject,
        content=test_content
    )

    if success:
        print("Тест завершен успешно!")
    else:
        print("Тест завершен с ошибками!")


if __name__ == "__main__":
    main()
