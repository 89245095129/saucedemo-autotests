import pytest
import allure
from src.pages.login_page import LoginPage
from src.utils.config import TestConfig
from src.utils.driver_manager import DriverManager


@allure.epic("Авторизация")
@allure.feature("Функциональность входа")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogin:
    """
    Тесты для проверки функциональности авторизации на SauceDemo.
    Покрывает позитивные и негативные сценарии.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self, request):
        """
        Фикстура настройки тестов.
        
        Args:
            request: Объект запроса pytest для получения имени теста
        """
        self.config = TestConfig()
        self.driver = DriverManager.get_driver()
        self.login_page = LoginPage(self.driver, timeout=self.config.timeout)
        self.test_name = request.node.name
        
        allure.dynamic.title(f"Тест: {self.test_name}")
        
        yield
        
        # Если тест упал, делаем скриншот
        if request.node.rep_call.failed:
            self.login_page.take_screenshot(f"FAILED_{self.test_name}.png")
            
        # Закрываем драйвер после каждого теста
        DriverManager.quit_driver()
    
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """
        Хук для получения результатов выполнения теста.
        """
        outcome = yield
        rep = outcome.get_result()
        setattr(item, "rep_" + rep.when, rep)
    
    @allure.id("TC-001")
    @allure.story("Позитивные сценарии")
    @allure.title("Успешный вход с валидными данными")
    @allure.description("""
    Цель: Проверить возможность успешного входа с корректными учетными данными.
    
    Шаги:
    1. Открыть страницу логина
    2. Ввести логин standard_user
    3. Ввести пароль secret_sauce
    4. Нажать кнопку Login
    
    Ожидаемый результат:
    - Происходит переход на страницу инвентаря (/inventory.html)
    - Отображаются товары в каталоге
    """)
    def test_successful_login(self):
        """Тест успешного входа."""
        with allure.step("Открыть страницу логина"):
            self.login_page.open()
            assert self.login_page.is_logo_displayed(), "Логотип не отображается"
            
        with allure.step("Ввести валидные учетные данные"):
            self.login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Проверить успешный вход"):
            assert "/inventory.html" in self.driver.current_url, \
                f"Ожидался переход на /inventory.html, но текущий URL: {self.driver.current_url}"
                
        with allure.step("Проверить отсутствие ошибок"):
            assert not self.login_page.is_error_displayed(), \
                "Отображается сообщение об ошибке при успешном входе"
    
    @allure.id("TC-002")
    @allure.story("Негативные сценарии")
    @allure.title("Вход с неверным паролем")
    @allure.description("""
    Цель: Проверить обработку неверного пароля.
    
    Шаги:
    1. Открыть страницу логина
    2. Ввести логин standard_user
    3. Ввести неверный пароль wrong_password
    4. Нажать кнопку Login
    
    Ожидаемый результат:
    - Отображается сообщение об ошибке
    - Не происходит переход на страницу инвентаря
    """)
    def test_login_with_wrong_password(self):
        """Тест входа с неверным паролем."""
        expected_error = "Epic sadface: Username and password do not match any user in this service"
        
        with allure.step("Открыть страницу логина"):
            self.login_page.open()
            
        with allure.step("Ввести корректный логин и неверный пароль"):
            self.login_page.login("standard_user", "wrong_password")
            
        with allure.step("Проверить сообщение об ошибке"):
            error_text = self.login_page.get_error_message()
            assert error_text == expected_error, \
                f"Ожидалась ошибка: '{expected_error}', получено: '{error_text}'"
            
        with allure.step("Проверить, что остались на странице логина"):
            assert "saucedemo.com" in self.driver.current_url, \
                "Произошел переход со страницы логина при ошибке"
    
    @allure.id("TC-003")
    @allure.story("Негативные сценарии")
    @allure.title("Вход заблокированным пользователем")
    @allure.description("""
    Цель: Проверить обработку попытки входа заблокированным пользователем.
    
    Шаги:
    1. Открыть страницу логина
    2. Ввести логин locked_out_user
    3. Ввести пароль secret_sauce
    4. Нажать кнопку Login
    
    Ожидаемый результат:
    - Отображается сообщение о блокировке пользователя
    - Не происходит переход на страницу инвентаря
    """)
    def test_login_locked_out_user(self):
        """Тест входа заблокированным пользователем."""
        expected_error = "Epic sadface: Sorry, this user has been locked out."
        
        with allure.step("Открыть страницу логина"):
            self.login_page.open()
            
        with allure.step("Попытаться войти как заблокированный пользователь"):
            self.login_page.login("locked_out_user", "secret_sauce")
            
        with allure.step("Проверить сообщение о блокировке"):
            error_text = self.login_page.get_error_message()
            assert error_text == expected_error, \
                f"Ожидалась ошибка: '{expected_error}', получено: '{error_text}'"
    
    @allure.id("TC-004")
    @allure.story("Негативные сценарии")
    @allure.title("Вход с пустыми полями")
    @allure.description("""
    Цель: Проверить валидацию пустых полей.
    
    Шаги:
    1. Открыть страницу логина
    2. Не заполняя поля, нажать кнопку Login
    
    Ожидаемый результат:
    - Отображается сообщение о необходимости заполнить поле username
    - Не происходит переход на страницу инвентаря
    """)
    def test_login_with_empty_fields(self):
        """Тест входа с пустыми полями."""
        expected_error = "Epic sadface: Username is required"
        
        with allure.step("Открыть страницу логина"):
            self.login_page.open()
            
        with allure.step("Нажать кнопку логина без ввода данных"):
            self.login_page.click_login()
            
        with allure.step("Проверить сообщение о пустом поле"):
            error_text = self.login_page.get_error_message()
            assert error_text == expected_error, \
                f"Ожидалась ошибка: '{expected_error}', получено: '{error_text}'"
    
    @allure.id("TC-005")
    @allure.story("Специальные сценарии")
    @allure.title("Вход пользователем с задержкой performance_glitch_user")
    @allure.description("""
    Цель: Проверить обработку пользователя с возможными задержками.
    
    Шаги:
    1. Открыть страницу логина
    2. Ввести логин performance_glitch_user
    3. Ввести пароль secret_sauce
    4. Нажать кнопку Login
    5. Дождаться загрузки (возможны задержки)
    
    Ожидаемый результат:
    - Происходит переход на страницу инвентаря, несмотря на задержки
    - Страница полностью загружается
    """)
    @pytest.mark.timeout(60)  # Увеличиваем таймаут для этого теста
    def test_login_performance_glitch_user(self):
        """Тест входа пользователем с задержками."""
        with allure.step("Открыть страницу логина"):
            self.login_page.open()
            
        with allure.step("Ввести данные пользователя с возможными задержками"):
            self.login_page.login("performance_glitch_user", "secret_sauce")
            
        with allure.step("Ожидать загрузки страницы инвентаря (с увеличенным таймаутом)"):
            # Используем явное ожидание с увеличенным временем
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            
            # Ожидаем элемент на странице инвентаря
            inventory_wait = WebDriverWait(self.driver, 30)
            inventory_wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "inventory_list"))
            )
            
        with allure.step("Проверить успешный вход"):
            assert "/inventory.html" in self.driver.current_url, \
                f"Не произошел переход на страницу инвентаря. Текущий URL: {self.driver.current_url}"
            
        with allure.step("Проверить отображение товаров"):
            inventory_items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")
            assert len(inventory_items) > 0, "Товары не отображаются на странице инвентаря"


@allure.epic("Авторизация")
@allure.feature("Дополнительные проверки")
class TestLoginAdditional:
    """
    Дополнительные тесты для проверки элементов страницы логина.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Настройка для дополнительных тестов."""
        self.driver = DriverManager.get_driver()
        self.login_page = LoginPage(self.driver)
        yield
        DriverManager.quit_driver()
    
    @allure.id("TC-006")
    @allure.title("Проверка элементов страницы логина")
    def test_login_page_elements(self):
        """Проверка наличия всех элементов на странице логина."""
        with allure.step("Открыть страницу логина"):
            self.login_page.open()
            
        with allure.step("Проверить наличие поля username"):
            assert self.login_page.driver.find_element(*LoginPage.USERNAME_FIELD).is_displayed()
            
        with allure.step("Проверить наличие поля password"):
            assert self.login_page.driver.find_element(*LoginPage.PASSWORD_FIELD).is_displayed()
            
        with allure.step("Проверить наличие кнопки логина"):
            assert self.login_page.driver.find_element(*LoginPage.LOGIN_BUTTON).is_displayed()
            
        with allure.step("Проверить наличие логотипа"):
            assert self.login_page.is_logo_displayed()
