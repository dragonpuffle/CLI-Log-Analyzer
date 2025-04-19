# CLI-Log-Analyzer

CLI-приложение на Python для анализа логов по HTTP-ручкам и уровням логирования.  

## Результат работы

![result](https://github.com/user-attachments/assets/1c7d387c-9a71-40ae-9374-2f491d65e1c8)

## Тесты и покрытие

![tests](https://github.com/user-attachments/assets/c5fe5924-6a0b-48e9-9515-523c5f2d79bb)

## Выполненые требования:

### Обязательные:
- Обработка лог-файлов из командной строки
- Поддержка указания типов отчета (пока есть `--report`) с проверкой допустимых значений
- Сбор статистики по `handlers` и уровням логирования (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- Обработка каждого файла по отдельности с последующим объединением в общий отчет
- Вывод результатов в виде отформатированной таблицы
- Подсчёт общего количества запросов
- Для функционала использовалась только стандартная библиотека
- Возможность обработки больших файлов (больше несколько гигабайт)
- Код содержит аннотации типов
- Код соответствует общепринятым стандартам стиля
- Код покрыт тестами `pytest`

### Дополнительные:
- Проверка на существование указанных лог-файлов
- Проверка допустимых значений отчёта через `argparse.choices`
- Простое масштабирование: чтобы добавить новый отчёт, достаточно реализовать отдельную функцию без изменения существующего кода (подробнее ниже)
- Есть возможность для обработки файлов параллельно (пока не имплементировано)
- Покрытие кода тестами > 90%

## Запуск:

### 1. Клонировать репозиторий

```bash
git clone https://github.com/dragonpuffle/CLI-Log-Analyzer
cd CLI-Log-Analyzer
```

### 2. Установить зависимости (опционально, только для тестов)

```bash
pip install -r requirements.txt
```

### 3. Запустить анализ логов

```python
python main.py logs/app1.log logs/app2.log logs/app3.log --report handlers
```

## Тестирование:

### Запуск тестов

```python
pytest
```

### Проверка покрытия

```python
coverage run -m pytest
coverage report -m
```

## Добавление нового отчета:

### В файле `file_analyzer.py` реализуйте функцию для нового типа отчета

### В файле `main.py` добавьте новый тип отчета в def parse_args_and_execute: 

```python
parser.add_argument('--report', choices=['handlers', 'NEW_TYPE], default='handlers', help='Type of the report')
```
### В файле `file_analyzer.py` добавьте запуск нового отчета в get_analysis: 

```python
    # if you would like to add new report type:
    # if report_type == 'another':
    #     another_analysis(file_gens)
```
