from sqlalchemy import select

from db import AsyncSessionLocal, BookRepository
from models import BookCreate, Book


class BookCrud:

    def __init__(self, title):
        self.title = title
    @classmethod
    async def add(cls, data: BookCreate):
        async with AsyncSessionLocal() as session:# Объявляем контекстный менеджер сессии
            book_dict = data.model_dump()
            book = BookRepository(**book_dict)
            session.add(book)
            await session.flush()  # Для получения первичного ключа
            await session.commit()  # Сохраняем в бд
            return book

    @classmethod
    async def find_all(cls) -> list[Book]:
        async with AsyncSessionLocal() as session:
            query = select(BookRepository)  # Запрос к бд
            result = await session.execute(query)  # Возвращаем результат запроса
            book_models = result.scalars().all()  # говорим чтобы нвм показали все возвращаеые объекты
            return book_models



