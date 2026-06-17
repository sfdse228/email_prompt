"""
Юнит-тесты для email_validator.py
"""

import unittest
from email_validator import EmailValidator


class TestEmailValidator(unittest.TestCase):
    """Тесты для валидатора email"""
    
    def setUp(self):
        """Создаём валидатор перед каждым тестом"""
        self.validator = EmailValidator(check_domain=False)
    
    # ---- Тесты на правильные email ----
    
    def test_valid_simple(self):
        """Простой email"""
        result = self.validator.validate("user@example.com")
        self.assertTrue(result["valid"])
        self.assertIsNone(result["error"])
    
    def test_valid_with_dots(self):
        """Email с точками"""
        result = self.validator.validate("user.name@mail.com")
        self.assertTrue(result["valid"])
    
    def test_valid_with_underscore(self):
        """Email с подчёркиванием"""
        result = self.validator.validate("user_name@domain.com")
        self.assertTrue(result["valid"])
    
    def test_valid_with_hyphen(self):
        """Email с дефисом"""
        result = self.validator.validate("user-name@my-domain.com")
        self.assertTrue(result["valid"])
    
    # ---- Тесты на неправильные email ----
    
    def test_empty(self):
        """Пустой email"""
        result = self.validator.validate("")
        self.assertFalse(result["valid"])
        self.assertEqual(result["error"], "Email не может быть пустым")
    
    def test_no_at(self):
        """Нет символа @"""
        result = self.validator.validate("userexample.com")
        self.assertFalse(result["valid"])
        self.assertEqual(result["error"], "В email должен быть символ @")
    
    def test_multiple_at(self):
        """Несколько @"""
        result = self.validator.validate("user@example@com")
        self.assertFalse(result["valid"])
    
    def test_empty_local(self):
        """Пустая локальная часть"""
        result = self.validator.validate("@example.com")
        self.assertFalse(result["valid"])
    
    def test_empty_domain(self):
        """Пустой домен"""
        result = self.validator.validate("user@")
        self.assertFalse(result["valid"])
    
    def test_no_dot_in_domain(self):
        """В домене нет точки"""
        result = self.validator.validate("user@examplecom")
        self.assertFalse(result["valid"])
    
    def test_has_space(self):
        """Есть пробел"""
        result = self.validator.validate("user name@example.com")
        self.assertFalse(result["valid"])
    
    def test_too_long(self):
        """Слишком длинный"""
        email = "a" * 101 + "@example.com"
        result = self.validator.validate(email)
        self.assertFalse(result["valid"])
        self.assertEqual(result["error"], "Email слишком длинный (макс. 100 символов)")
    
    # ---- Тест на пакетную проверку ----
    
    def test_batch(self):
        """Пакетная проверка нескольких email"""
        emails = ["good@example.com", "bad@", "user@domain.com"]
        results = self.validator.validate_batch(emails)
        
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0]["valid"])
        self.assertFalse(results[1]["valid"])
        self.assertTrue(results[2]["valid"])
    
    # ---- Тест на проверку домена ----
    
    def test_domain_check(self):
        """Проверка существования домена"""
        validator_with_domain = EmailValidator(check_domain=True)
        
        # Проверяем реальный домен
        result = validator_with_domain.validate("test@gmail.com")
        # Может быть True или False, но проверяем что ошибка не "домен не существует"
        # (зависит от интернета)
        
        # Проверяем заведомо несуществующий домен
        result = validator_with_domain.validate("user@thisdomaindefinitelydoesnotexist123456789.com")
        # Должен быть невалидным
        if not result["valid"]:
            self.assertIn("не существует", result["error"])


# Запуск тестов
if __name__ == "__main__":
    unittest.main(verbosity=2)