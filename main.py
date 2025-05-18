import json


from typing import Optional
from fastapi import FastAPI, HTTPException, Depends

from crud import BookCrud
from db import init_db
from models import BookCreate, Book, BookUpdate

from typing import Annotated


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()# только для разработки


@app.post("/create_in_db")
async def add_book(book: Annotated[BookCreate, Depends()]) -> list:
    book_id = await BookCrud.add(book)
    return book_id


@app.get("/get_db")
async def get_books() -> list[Book]:
    books = await BookCrud.find_all()

    return books


"""Здесь будут эндпоинты для хранения данных в JSON"""

curent_id = 1
new_list = []

@app.post("/create", tags=["Книги JSON"])
def create_book(new_book: BookCreate):
    global curent_id, new_list
    data = {
        "id": curent_id,
        "title": new_book.title,
        "author": new_book.author,
        "year": new_book.year,
        "genre": new_book.genre,
        "pages": new_book.pages,
        "availability": new_book.availability,
    }
    new_list.append(data)


    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(new_list, file, ensure_ascii=False, indent=4)
    curent_id += 1

    return {"success": True, "message": "Книга успешно добавлена"}


@app.get("/books", tags=["Книги JSON"], response_model=list[Book])
def get_books(title: Optional[str] = None,
    author: Optional[str] = None
    ):
    with open('data.json', 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
    filter = loaded_data

    if title:
        filter = [book for book in filter if title.lower() in book["title"].lower()]

    if author:
        filter = [book for book in filter if author.lower() in book["author"].lower()]

    return filter


@app.get("/book/{book_id}", tags=["Книги JSON"])
def get_book(book_id: int):
    with open('data.json', 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)

    book = [b for b in loaded_data if b["id"] == book_id]

    if book == []:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    return book


@app.delete("/book/delete/{book_id}", tags=["Книги JSON"])
def delete_book(book_id: int):
    with open('data.json', 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)

    book_index = next((index for index, book in enumerate(loaded_data) if book["id"] == book_id), None)

    if book_index == None:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    del loaded_data[book_index]

    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(loaded_data, file, ensure_ascii=False, indent=4)

    return loaded_data


@app.put("/book/update/{book_id}", tags=["Книги JSON"])
def update_book(book_id: int, update_data: BookUpdate):
    update_dict = update_data.dict(exclude_unset=True)

    with open('data.json', 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)

    for book in loaded_data:
        if book["id"] == book_id:
            for key, value in update_dict.items():
                book[key] = value

            with open('data.json', 'w', encoding='utf-8') as file:
                json.dump(loaded_data, file, ensure_ascii=False, indent=4)

    return loaded_data