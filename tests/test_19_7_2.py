import json

from project_19_7_2 import PetFriends
from settings import user_email, user_pass
import os

pf = PetFriends()



def test_1_get_api_key_for_valid_user(email=user_email, password=user_pass):
    """ Проверяем, что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_2_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(user_email, user_pass)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_3_add_new_pet_with_valid_data(name='Пёсель', animal_type='собака',
                                     age='444', pet_photo='images\\dog.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(user_email, user_pass)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_4_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(user_email, user_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "КотЭ", "кот", "333", "images\\cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_5_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(user_email, user_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# тест 1
def test_6_add_new_simple_pet_with_valid_data(name='Кеша', animal_type='попугай',
                                     age='22'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(user_email, user_pass)

    # Добавляем питомца
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# тест 2
def test_7_add_new_photo_for_pet(pet_id="", pet_photo='images\\dog.jpg'):
    """Проверяем что можно добавить фото для питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(user_email, user_pass)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_simple_pet(auth_key, "<Безликий>", "мираж", "777")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Добавляем фото для первого питомца из списка
    pet_id = my_pets['pets'][0]['id']
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert 'data:image' in result['pet_photo']

# тест 3
def test_8_get_api_key_for_random_user(email='random', password='random'):
    """ Проверяем, что запрос api ключа c некорректными данными пользователя
    возвращает статус 403 и результат запроса равен 'Forbidden'"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'Forbidden' in result

# тест 4
def test_9_delete_self_pet_with_notvalid_id():
    """Проверяем возможность удаления питомца c некорректным id"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(user_email, user_pass)


    # В качестве id возьмём некорретное значение и отправляем запрос на удаление
    pet_id = 'not_valid_id'
    status, result = pf.delete_pet(auth_key, pet_id)

    assert status != 200
    # тест отрицательный, так как приложение возвращает код 200, не смотря на то,
    # что питомца с таким id не существует

# тест 5
def test_10_add_new_simple_pet_with_notvalid_data(name=3454, animal_type='попугай',
                                                age='возраст'):
    """Проверяем, что нельзя добавить питомца без фото с некорректными данными. Код 400 по документации"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(user_email, user_pass)

    # Добавляем питомца
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # тест отрицательный, так как приложение создаёт питомца с заведомо некорректными данными

# тест 6
def test_11_add_new_pet_with_notvalid_data(name='12345', animal_type='собака',
                                     age='abc', pet_photo='images\\dog.jpg'):
    """Проверяем, что невозможно добавить питомца с некорректными данными. Код 400 по документации"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(user_email, user_pass)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
    # тест отрицательный, так как приложение создаёт питомца с заведомо некорректными данными

# тест 7
def test_12_add_new_photo_for_notvalid_pet_id(pet_id='not_valid_id', pet_photo='images\\dog.jpg'):
    """Проверяем что можно добавить фото для питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(user_email, user_pass)

    # Добавляем фото для питомца c указанным id
    status, result = pf.add_pet_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400
   #тест отрицательный, так как по документации при некорректных данных должен быть результат с кодом 400

# тест 8
def test_13_update_self_pet_info_with_not_valid_id(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем невозможность обновления информации о несуществующем питомце - Код 400 по документации"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(user_email, user_pass)

    # Пробуем отправить данные (имя, тип и возраст) для несуществующего id
    status, result = pf.update_pet_info(auth_key, 'not_valid_pet_id', name, animal_type, age)

    # Проверяем что статус ответа = 400
    assert status == 400

# тест 9
def test_14_update_self_pet_info_with_not_valid_auth_key(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем невозможность обновления информации о питомце
    для несуществующего пользователя - Код 403 по документации"""

    # Создаём переменную auth_key с некорректным значением
    auth_key={'key': 'not_valid_auth_key'}

    # Пробуем отправить данные (имя, тип и возраст) для несуществующего пользователя
    status, result = pf.update_pet_info(auth_key, '123456', name, animal_type, age)

    # Проверяем что статус ответа = 403
    assert status == 403

# тест 10
def test_15_add_new_simple_pet_with_notvalid_auth_key(name="Кеша", animal_type='попугай', age=12):
    """Проверяем, что нельзя добавить питомца без фото с несуществующим пользователем. Код 403 по документации"""

    # Создаём переменную auth_key с некорректным значением
    auth_key = {'key': 'not_valid_auth_key'}

    # Добавляем питомца
    status, result = pf.add_new_simple_pet(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 403


