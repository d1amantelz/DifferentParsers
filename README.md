
## Реализованные парсеры:

1. Синхронный парсер
2. Мультипроцессорный парсер
3. Многопоточный парсер
4. Асинхронный парсер
5. Асинхронный парсер (4-й), обернутый в FastAPI


## Задача:

> Реализовать парсеры с сайта:<br> https://jsonplaceholder.typicode.com/ <br>
Объекты albums/ и photos/: <br>
https://jsonplaceholder.typicode.com/albums/<br>
https://jsonplaceholder.typicode.com/photos/<br>
Скачиваем все альбомы и фотографии, кладем их по папкам: <br>/альбом/название_фотографии<br><br>
**Требования:**
Парсер реализовать на ООП, соблюдая SOLID.<br>
Для соединения по http можно использовать https://docs.python-requests.org/en/latest/<br>
Необходимо реализовать декоратор, для замерки работы времени всего скрипта, необходимо реализовать декоратор для замерки времени метода, который скачивает.


## Установка и Использование

1. *Клонирование репозитория*:

```bash
git clone https://github.com/d1amantelz/DifferentParsers.git
```

2. *Установка виртуального окружения*:


```bash
# Linux
python3 -m venv venv

# Windows
python -m venv venv
```

3. *Активация виртуального окружения*:


```bash
# Linux
source venv/bin/activate

# Windows
.\venv\Scripts\activate
```

4. *Установка пакетов*:



```bash
# Linux
python3 -m pip install -r requirements.txt

# Windows
python -m pip install -r requirements.txt
```

5. *На данном шаге нужно создать папку для альбомов в папке проекта с названием*: **albums**

6. *Запуск парсеров (с 1-4)*:

Необходимо просто раскомментировать нужный:
```python
@script_timer
def main():
    session = requests.Session()

    # Синхронный парсер
    # first_parser = SyncParser(session)
    # first_parser.download_content(num_albums=4)

    # Мультипроцессорный парсер
    # multi_parser = MultiProcessorParser(session)
    # multi_parser.download_content(num_albums=4, num_processes=4)

    # Многопоточный парсер
    # threaded_parser = MultiThreadedParser(session)
    # threaded_parser.download_content(num_albums=4)

    # Асинхронный парсер
    async def run_async_parser():
        async with aiohttp.ClientSession() as aio_session:
            async_parser = AsyncParser(aio_session)
            await async_parser.download_content(num_albums=4)

    asyncio.run(run_async_parser())


if __name__ == "__main__":
    main()

```

***ПРИМЕЧАНИЕ:*** Можно запускать несколько парсеров в одном программе. Также, выбирать определенное кол-во альбомов для скачивания. Для скачивания всех необходимо убрать **num_albums** в вызове класса.

7. *Запуск 5-го парсера (FastAPI)*:

В консоли виртуального окружения: 

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Далее переходим в браузер на адрес: http://127.0.0.1:8000/parse/3, где вместо 3 пишем кол-во альбомов для скачивания. 

8. *Деактивация виртуального окружения*:

```bash
deactivate
```
