from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import allure
import time


class LoginPage:
    """
    Page Object Model для страницы авторизации SauceDemo.
    Инкапсулирует все элементы и действия на странице логина.
    """
    
    # Локаторы элементов
    USERNAME_FIELD = (By.ID, 'user-name')
    PASSWORD_FIELD = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login-button')
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')
    LOGO = (By.CLASS_NAME, 'login_logo')
    BOT_COLUMN = (By.CLASS_NAME, 'bot_column')
    
    def __init__(self, driver, timeout=10):
        """
        Инициализация страницы.
        
        Args:
            driver: Экземпляр WebDriver
            timeout: Время ожидания элементов (секунды)
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        
    @allure.step("Открыть страницу логина")
    def open(self, url="https://www.saucedemo.com/"):
        """Открывает страницу логина."""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located(self.LOGO))
        return self
        
    @allure.step("Ввести имя пользователя: '{username}'")
    def enter_username(self, username):
        """Вводит имя пользователя в поле."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.USERNAME_FIELD)
        )
        element.clear()
        element.send_keys(username)
        return self
        
    @allure.step("Ввести пароль: '{password}'")
    def enter_password(self, password):
        """Вводит пароль в поле."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.PASSWORD_FIELD)
        )
        element.clear()
        element.send_keys(password)
        return self
        
    @allure.step("Нажать кнопку логина")
    def click_login(self):
        """Нажимает кнопку входа."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        element.click()
        return self
        
    @allure.step("Выполнить вход с данными: {username}/{password}")
    def login(self, username, password):
        """
        Полный процесс входа.
        
        Args:
            username: Имя пользователя
            password: Пароль
            
        Returns:
            self или InventoryPage в зависимости от результата
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
        return self
        
    @allure.step("Получить текст ошибки")
    def get_error_message(self):
        """
        Получает текст сообщения об ошибке.
        
        Returns:
            str: Текст ошибки или None, если сообщение не найдено
        """
        try:
            error_element = self.wait.until(
                EC.visibility_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except TimeoutException:
            return None
            
    @allure.step("Проверить наличие ошибки")
    def is_error_displayed(self):
        """Проверяет, отображается ли сообщение об ошибке."""
        try:
            return self.driver.find_element(*self.ERROR_MESSAGE).is_displayed()
        except NoSuchElementException:
            return False
            
    @allure.step("Проверить отображение логотипа")
    def is_logo_displayed(self):
        """Проверяет, отображается ли логотип."""
        try:
            return self.driver.find_element(*self.LOGO).is_displayed()
        except NoSuchElementException:
            return False
            
    @allure.step("Очистить поля формы")
    def clear_form(self):
        """Очищает все поля формы."""
        self.driver.find_element(*self.USERNAME_FIELD).clear()
        self.driver.find_element(*self.PASSWORD_FIELD).clear()
        return self
        
    @allure.step("Получить текущий URL")
    def get_current_url(self):
        """Возвращает текущий URL."""
        return self.driver.current_url
        
    @allure.step("Сделать скриншот страницы")
    def take_screenshot(self, filename="login_page.png"):
        """Делает скриншот текущей страницы."""
        screenshot_path = f"/app/results/screenshots/{filename}"
        self.driver.save_screenshot(screenshot_path)
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=filename,
            attachment_type=allure.attachment_type.PNG
        )
        return screenshot_path
