# Запуск в терминале командой:
# python -m pytest -v --driver Chrome --driver-path /chromedriver.exe tests/tests_my_pets.py

import pytest
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from statistic import get_pet_count


def test_all_my_pets_are_present(get_my_pets):
    '''Проверяем, что на странице со списком моих питомцев присутствуют все питомцы'''

    # Ожидаем загрузки элементов карточек питомцев
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем в переменную pets элементы карточек питомцев и считаем количество карточек на странице
    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets tbody tr')
    number_of_pets = len(pets)

    # Получаем количество питомцев из блока статистики пользователя
    pet_count = get_pet_count()

    # Проверяем что количество питомцев из блока статистики совпадает с количеством карточек питомцев
    assert pet_count == number_of_pets, '\nКоличество карточек питомцев на странице не совпадает с счетчиком'
    print(f'\nКоличество карточек питомцев: {number_of_pets}')
    print(f'Счетчик питомцев: {pet_count}')


def test_most_pets_have_photo(get_my_pets):
    '''Поверяем, что на странице со списком моих питомцев хотя бы у половины питомцев есть фото'''

    # Ожидаем загрузки элементов карточек питомцев
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем в переменную images элементы с атрибутом img
    images = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover img')

    # Получаес количество питомцев
    pet_count = get_pet_count()

    # Находим количество питомцев с фотографией
    photo_count = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            photo_count += 1

    # Проверяем, что количество питомцев с фотографией больше или равно половине количества питомцев пользователя
    assert photo_count >= pet_count/2, 'Меньше половины карточек питомцев имеют фото'
    print(f'\nКоличество фото: {photo_count}')
    print(f'Количество питомцев: {pet_count}')


def test_no_empty_fields_in_pet_cards(get_my_pets):
    '''Поверяем, что у всех питомцев есть имя, возраст и порода'''

    # Ожидаем загрузки элементов карточек питомцев
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем имена, породу и возраст все питомцев в отдельные массивы
    names = pytest.driver.find_elements(By.XPATH, f'//div[@id="all_my_pets"]//tbody/tr/td[1]')
    breeds = pytest.driver.find_elements(By.XPATH, f'//div[@id="all_my_pets"]//tbody/tr/td[2]')
    age = pytest.driver.find_elements(By.XPATH, f'//div[@id="all_my_pets"]//tbody/tr/td[3]')

    # Перебираем данные каждого питомца для проверки, что поля не пустые
    for i in range(len(names)):
       assert names[i].text != '', f'Не заполнено поле "Имя" в карточке питомца с индексом {i}'
       assert breeds[i].text != '', f'Не заполнено поле "Порода" в карточке питомца с индексом {i}'
       assert age[i].text != '', f'Не заполнено поле "Возраст" в карточке питомца с индексом {i}'



def test_all_pets_have_different_names(get_my_pets):
    '''Поверяем что на странице со списком моих питомцев, у всех питомцев разные имена'''

    # Ожидаем загрузки элементов карточек питомцев
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем имена питомцев в массив
    names = pytest.driver.find_elements(By.XPATH, f'//div[@id="all_my_pets"]//tbody/tr/td[1]')
    pet_names = [i.text for i in names]

    # Перебираем имена и если имя повторяется то прибавляем к счетчику единицу, дубликат записываем в словарь
    dubl = {}
    cnt = 0
    for i in range(len(pet_names)):
        if pet_names.count(pet_names[i]) > 1:
            cnt += 1
            dubl[pet_names[i]] = cnt

    # Проверяем, если cnt == 0 то повторяющихся имен нет.
    assert len(dubl) == 0, f'Эти имена повторяются: {dubl}'


def test_no_pet_dublicates(get_my_pets):
    '''Проверяем, что на странице со списком моих питомцев нет дубликатов питомцев'''

    # Ожидаем загрузки элементов карточек питомцев
    element = WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))

    # Сохраняем в переменную pets элементы карточек питомцев и считаем количество карточек на странице
    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '#all_my_pets tbody tr')
    pets_data = [pet.text.replace('\n', '').replace('×', '') for pet in pets]

    # Перебираем карточки питомцев и если данные прибавляются, то прибавляем к счетчику единицу,
    # дубликат записываем в словарь
    dubl = {}
    cnt = 0
    for pet in pets_data:
        if pets_data.count(pet) > 1:
            cnt += 1
            dubl[pet] = cnt

    # Проверяем, если cnt == 0 то повторяющихся имен нет.
    assert len(dubl) == 0, f'Карточки этих питомцев повторяются: {dubl}'