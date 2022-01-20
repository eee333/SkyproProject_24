lesson24_project
=========
"Функциональное программирование"
---------
Веб-сервер на flask, состоит из одного POST метода.

1. Доступен по пути /perform_query
2. Принимает 2 параметра: имя файла и запрос.
3. Метод обращается к файлу внутри директории data.
4. Обрабатывает файл, следуя написанному запросу, и возвращать ответ клиенту

Пример:

1. file_name=apache_logs.txt
query=filter:POST|sort:desc|map:0|unique|limit:5
2. file_name=apache_logs.txt
query=filter:GET|regex:images\/\w+\.jpg|sort:desc



