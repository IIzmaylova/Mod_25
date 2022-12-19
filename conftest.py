import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import email, password, user

@pytest.fixture(autouse=True)
def testing():
   pytest.driver = webdriver.Chrome('chromedriver.exe')
   pytest.driver.implicitly_wait(10)
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends.skillfactory.ru/login')

   yield

   pytest.driver.quit()



@pytest.fixture()
def get_my_pets():
   # Ожидаем загрузки поля email
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'email')))


   # Вводим email
   pytest.driver.find_element(By.ID, 'email').send_keys(email)

   # Ожидаем загрузки поля пароль
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.ID, 'pass')))
   # Вводим пароль
   pytest.driver.find_element(By.ID, 'pass').send_keys(password)

   # Ожидаем загрузки кнопки входа в аккаунт
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

   # Ожидаем загрузки кнопки перехода на страницу "Мои питомцы"
   element = WebDriverWait(pytest.driver, 10).until(
      EC.presence_of_element_located((By.LINK_TEXT, 'Мои питомцы')))
   # Переходим на страницу Мои питомцы
   pytest.driver.find_element(By.LINK_TEXT, 'Мои питомцы').click()

   # Проверяем, что мы оказались на главной странице пользователя
   if pytest.driver.find_element(By.TAG_NAME, 'h2').text == user:
      pytest.driver.save_screenshot('my_pets_petfriends.png')
   else:
      raise Exception('error loading the "My pets" page')
