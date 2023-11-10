import abc
import asyncio
import multiprocessing
import os
import threading
import time

import aiohttp
import requests


def load_state():
    try:
        with open("state.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


albums = requests.get("https://jsonplaceholder.typicode.com/albums").json()
album_index = load_state()


def save_state(album_index):
    with open("state.txt", "w") as f:
        f.write(str(album_index))


def create_album(album: dict) -> None:
    os.mkdir(f"albums/{album['title']}")


def get_albums(num_albums: int | None) -> list[dict]:
    global album_index

    if num_albums is None:
        save_state(0)
        return albums

    new_album_index = album_index + num_albums
    res = albums[album_index:new_album_index]
    album_index = new_album_index
    save_state(album_index)
    return res


def method_timer(method):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        method(*args, **kwargs)
        finish = time.perf_counter() - start

        class_name = args[0].__class__.__name__
        method_name = method.__name__

        print(
            f"[M] Метод {class_name}.{method_name}(...) выполнил работу за {finish:.3f}с."
        )

    return wrapper


def async_method_timer(async_method):
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        await async_method(*args, **kwargs)
        finish = time.perf_counter() - start

        class_name = args[0].__class__.__name__
        method_name = async_method.__name__

        print(
            f"[M] Асинхронный метод {class_name}.{method_name}(...) выполнил работу за {finish:.3f}с."
        )

    return wrapper


def script_timer(main_func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        main_func(*args, **kwargs)
        finish = time.perf_counter() - start

        print(f"[S] Программа была закончена за {finish:.3f}с.")

    return wrapper


class Parser(abc.ABC):
    def __init__(self, session):
        self.session = session

    @abc.abstractmethod
    def download_content(self) -> None:
        pass

    def get_photos_from_album(self, album: dict) -> list[dict]:
        return self.session.get(
            f'https://jsonplaceholder.typicode.com/photos?albumId={album["id"]}'
        ).json()

    def save_photos_to_album(self, album: dict, photos: list[dict]) -> None:
        for photo in photos:
            with open(f"albums/{album['title']}/{photo['title']}.png", "wb") as f:
                img_data = self.session.get(photo["url"]).content
                f.write(img_data)


class SyncParser(Parser):
    @method_timer
    def download_content(self, num_albums: int | None) -> None:
        albums = get_albums(num_albums)

        for album in albums:
            create_album(album)
            photos = self.get_photos_from_album(album)
            self.save_photos_to_album(album, photos)


class MultiProcessorParser(Parser):
    @method_timer
    def download_content(
        self, num_albums: int | None, num_processes: int | None
    ) -> None:
        albums = get_albums(num_albums)

        chunk_size = len(albums) // num_processes
        num_processes = num_processes if num_processes else 7
        album_chunks = [
            albums[i : i + chunk_size] for i in range(0, len(albums), chunk_size)
        ]

        with multiprocessing.Pool(processes=num_processes) as pool:
            pool.map(self.process_albums, album_chunks)

    def process_albums(self, albums: list[dict]):
        for album in albums:
            create_album(album)
            photos = self.get_photos_from_album(album)
            self.save_photos_to_album(album, photos)


class MultiThreadedParser(Parser):
    @method_timer
    def download_content(self, num_albums: int | None) -> None:
        albums = get_albums(num_albums)

        threads = []
        for album in albums:
            thread = threading.Thread(target=self.process_album, args=(album,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def process_album(self, album: dict) -> None:
        create_album(album)
        photos = self.get_photos_from_album(album)
        self.save_photos_to_album(album, photos)


class AsyncParser(Parser):
    @async_method_timer
    async def download_content(self, num_albums: int | None) -> None:
        albums = get_albums(num_albums)
        tasks = [self.process_album(album) for album in albums]
        await asyncio.gather(*tasks)

    async def process_album(self, album: dict) -> None:
        create_album(album)
        photos = await self.get_photos_from_album(album)

        for photo in photos:
            async with self.session.get(photo["url"]) as response:
                img_data = await response.read()
                with open(f"albums/{album['title']}/{photo['title']}.png", "wb") as f:
                    f.write(img_data)

    async def get_photos_from_album(self, album: dict) -> list[dict]:
        async with self.session.get(
            f'https://jsonplaceholder.typicode.com/photos?albumId={album["id"]}'
        ) as response:
            photos = await response.json()
            return photos


@script_timer
def main():
    # session = requests.Session()

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
