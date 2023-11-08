from cryptography.fernet import Fernet


def generate_session_key():
    """Генерация ключа для каждой сессии пользователя
    :return key: ключ шифрования"""
    key = Fernet.generate_key()
    return key


def encrypt(data, key):
    """Шифрование сообщения
    :param data: данные для шифрования
    :param key: ключ шифрования
    :return decrypted_data: шифрованное сообщение"""
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data


def decrypt(data, key):
    """Дешифрование данных
    :param data: данные для дешифрования
    :param key: ключ шифрования
    :return decrypted_data: дешифрованное сообщение"""
    
    f = Fernet(key)
    decrypted_data = f.decrypt(data).decode()
    return decrypted_data