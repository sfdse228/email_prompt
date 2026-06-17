"""
email_validator.py - Простой валидатор email-адресов
"""

import re
import socket


class EmailValidator:
    """Класс для проверки email-адресов"""
    
    def __init__(self, check_domain=True):
        """
        check_domain: проверять ли существование домена
        """
        self.check_domain = check_domain
    
    def validate(self, email):
        """
        Проверяет один email-адрес
        
        Возвращает словарь:
        {
            "valid": True/False,
            "email": "исходный email",
            "error": "текст ошибки или None"
        }
        """
        # Убираем пробелы по краям
        email = email.strip()
        
        # Проверка 1: не пустой
        if not email:
            return {"valid": False, "email": email, "error": "Email не может быть пустым"}
        
        # Проверка 2: длина
        if len(email) > 100:
            return {"valid": False, "email": email, "error": "Email слишком длинный (макс. 100 символов)"}
        
        # Проверка 3: есть @
        if '@' not in email:
            return {"valid": False, "email": email, "error": "В email должен быть символ @"}
        
        # Проверка 4: количество @
        if email.count('@') != 1:
            return {"valid": False, "email": email, "error": "Должен быть ровно один символ @"}
        
        # Разделяем на локальную часть и домен
        local, domain = email.split('@')
        
        # Проверка 5: локальная часть не пустая
        if not local:
            return {"valid": False, "email": email, "error": "Локальная часть не может быть пустой"}
        
        # Проверка 6: домен не пустой
        if not domain:
            return {"valid": False, "email": email, "error": "Домен не может быть пустым"}
        
        # Проверка 7: в домене есть точка
        if '.' not in domain:
            return {"valid": False, "email": email, "error": "В домене должна быть точка"}
        
        # Проверка 8: нет пробелов
        if ' ' in email:
            return {"valid": False, "email": email, "error": "Email не должен содержать пробелов"}
        
        # Проверка 9: домен существует (если включено)
        if self.check_domain:
            if not self._domain_exists(domain):
                return {"valid": False, "email": email, "error": f"Домен {domain} не существует"}
        
        # Все проверки пройдены
        return {"valid": True, "email": email, "error": None}
    
    def validate_batch(self, emails):
        """
        Проверяет несколько email-адресов
        
        emails: список строк
        возвращает список результатов
        """
        results = []
        for email in emails:
            results.append(self.validate(email))
        return results
    
    def _domain_exists(self, domain):
        """
        Проверяет, существует ли домен
        """
        try:
            # Пытаемся получить IP-адрес домена
            socket.gethostbyname(domain)
            return True
        except socket.gaierror:
            return False


def main():
    """Консольный интерфейс"""
    validator = EmailValidator(check_domain=False)  # Отключаем DNS для скорости
    
    print("\n" + "=" * 40)
    print("ПРОВЕРКА EMAIL-АДРЕСОВ")
    print("=" * 40)
    print("Команды:")
    print("  check <email>  - проверить email")
    print("  batch          - проверить несколько email (по одному на строку)")
    print("  exit           - выход")
    print("=" * 40)
    
    while True:
        cmd = input("\n> ").strip()
        
        if cmd == "exit":
            print("До свидания!")
            break
        
        elif cmd == "batch":
            print("Введите email-адреса (по одному на строку, пустая строка - закончить):")
            emails = []
            while True:
                line = input("> ")
                if line == "":
                    break
                emails.append(line)
            
            if emails:
                results = validator.validate_batch(emails)
                print("\nРезультаты:")
                for r in results:
                    status = "✅" if r["valid"] else "❌"
                    print(f"{status} {r['email']}")
                    if r["error"]:
                        print(f"   Ошибка: {r['error']}")
        
        elif cmd.startswith("check "):
            email = cmd[6:].strip()
            if email:
                result = validator.validate(email)
                print("\nРезультат:")
                if result["valid"]:
                    print(f"✅ {result['email']} - ВАЛИДНЫЙ")
                else:
                    print(f"❌ {result['email']} - НЕВАЛИДНЫЙ")
                    print(f"   Причина: {result['error']}")
            else:
                print("Укажите email: check user@example.com")
        
        elif cmd == "help":
            print("  check <email>  - проверить email")
            print("  batch          - проверить несколько email")
            print("  exit           - выход")
        
        else:
            print("Неизвестная команда. Введите 'help' для справки.")


if __name__ == "__main__":
    main()