# CLI для парсинга данных из .pdf файла

## Справка:

```
positional arguments:
  filename        PDF Файл для парсинга

options:
  -h, --help      show this help message and exit
  --only_save_db  Позволяет сохранить данные из result.json в базу данных.
                  Использование возможно только в случае уже сгенерированного файла result.json
```

## Подробнее про аргумены:

- `filename` - Обязательный позиционный аргумент. Тип файла должен быть `.pdf`
- `--only_save_db` - Позволяет пропустить парсинг `.pdf` файла и сохранить данные из `results/result.json` в бд.
  **Важно!**
  Сохранит данные, только в случае уже сгенерированного `result.json`

## Подробнее по файлам проекта:

- `modules/database/models.py` - Хранит SqlAlchemy модель для базы данных
- `modules/database/service.py` - Сервис для работы с базой данных. Настроен для работы с `SQLITE`
- `modules/app.py` - Основное приложение. Регулирует запуск парсеров, а так же с ответами от пользователя
- `modules/pdf_parser.py` - Pdf парсер. Переводит pdf страницы в txt формат. Результат работы сохраняет
  в `temp/parsed.txt`. **Важно!** После завершения работы программы директория `temp` удаляется
- `modules/text_parser.py` - Text парсер. С помощью регулярных выражений `utils/patterns.py` производит парсинг
  текста `temp/parsed.txt`. Результат работы сохраняет в `results/result.json`
- `results/result.json` - Будет сгенерирован автоматически, после работы `TextParser`. Содержит результаты
  парсинга `temp/parsed.txt`
- `results/result.db` - Будет сгенерирован автоматически, в случае если пользователь согласился сохранить
  результаты `results/result.json` в базу данных или же запустил cli с флагом `--only_save_db`
- `utils/constants.py` - Основные константы (сообщения, ошибки с сообщениями...) для приложения
- `utils/exceptions.py` - Собственные исключения для приложения
- `utils/file_utils.py` - Утилиты для работы с файлами
- `utils/patterns.py` - Основные паттерны для парсинга. **Важно!** В случае если парсинг проходит не правильно, паттерны
  можно отредактировать под себя



