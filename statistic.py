import pytest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def get_user_statistic():
   '''Получаем общие статистические данные о пользователе'''

   # Ожидаем загрузки элемента со статистикой страницы пользователя
   element = WebDriverWait(pytest.driver, 10).until(
   EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4.left")))

   # Сохраняем имя пользователя в переменную username,
   # а статистические данные по странице пользователя в словарь user_statistic
   user_statistic = pytest.driver.find_element(By.CSS_SELECTOR, '.\\.col-sm-4.left').text.split('\n')
   username = user_statistic.pop(0)
   user_statistic = dict(subString.split(":") for subString in user_statistic)

   # Преобразуем показатели счетчиков в тип int
   for count in user_statistic.keys():
      user_statistic[count] = int(user_statistic[count])

   return username, user_statistic


def get_pet_count():
   '''Получаем количество питомцев пользователя'''
   _, user_statistic = get_user_statistic()
   pet_count = user_statistic['Питомцев']
   return pet_count


def get_friend_count():
   '''Получаем количество друзей пользователя'''
   _, user_statistic = get_user_statistic()
   friend_count = user_statistic['Друзей']
   return friend_count

def get_message_count():
   '''Получаем количество сообщений пользователя'''
   _, user_statistic = get_user_statistic()
   message_count = user_statistic['Сообщений']
   return message_count