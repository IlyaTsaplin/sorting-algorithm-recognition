# Инструкция для загрузки кодов решений со Stepik
Скрипт для загрузки: /utils/stepik_data_loading.py
1. Перейти на https://stepik.org/oauth2/applications
2. Добавить новое приложение со следующими параметрами
* Сlient type: confidential
* Authorization grant type: client credentials
3. Скопировать Client id и Client secret в соответствующие переменные CLIENT_ID и CLIENT_SECRET
4. Заполнить список в переменной STEP_ID_LIST значениями id степов, решения которых планируется скачать

После запуска скрипта будет создана папка data, в которой будут находиться все правильные решения на языке Python3 в виде файлов.
