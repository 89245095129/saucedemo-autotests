# 🧪 SauceDemo Automated Tests

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.15-green)
![Docker](https://img.shields.io/badge/Docker-✓-blue)
![Allure](https://img.shields.io/badge/Allure_Reports-✓-orange)

Автоматизированные тесты для проверки функциональности авторизации на [saucedemo.com](https://www.saucedemo.com/).

## 🚀 Быстрый старт

### Вариант 1: Запуск через Docker (рекомендуется)

```bash
# Клонировать репозиторий
git clone https://github.com/ваш-username/saucedemo-autotests.git
cd saucedemo-autotests

# Запустить все тесты в контейнере
docker-compose up --build

# Или только тесты
docker-compose run tests

# С доступом к Allure отчету
docker-compose up --build && docker-compose logs -f allure
