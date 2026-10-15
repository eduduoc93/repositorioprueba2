#!/usr/bin/env python3

import json
import requests
from faker import Faker

APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"


def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(f"{APIHOST}/api/v1/loginViaBasic", auth=authCreds)
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(
            f"Status code {r.status_code} and text {r.text}, while trying to Auth."
        )


def addBook(book, apiKey):
    r = requests.post(
        f"{APIHOST}/api/v1/books",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": apiKey,
        },
        data=json.dumps(book),
    )

    if r.status_code in (200, 201):
        return r.json() if r.text else book
    else:
        raise Exception(
            f"Error code {r.status_code} y texto '{r.text}' al intentar agregar el libro ID {book['id']}."
        )


def main():
    # 1. Obtener el token de autenticación
    apiKey = getAuthToken()
    fake = Faker()

    created_books = []

    # Ajuste: Comenzar desde el ID 8 y generar 50 libros (IDs del 8 al 57)
    start_id = 8
    total_books = 50

    print(
        f"Agregando {total_books} libros a la biblioteca (del ID {start_id} al {start_id + total_books - 1})...\n"
    )

    for i in range(start_id, start_id + total_books):
        book = {
            "id": i,
            "title": fake.catch_phrase(),
            "author": fake.name(),
            "isbn": fake.isbn13(),
        }

        created_book = addBook(book, apiKey)
        created_books.append(book)
        print(
            f"Agregado ID {i}: '{book['title']}' por {book['author']} (ISBN: {book['isbn']})"
        )

    # 2. Listar la totalidad de los 50 libros creados
    print("\n" + "=" * 60)
    print("TOTALIDAD DE LOS 50 LIBROS CREADOS")
    print("=" * 60)

    for b in created_books:
        print(f"ID:     {b['id']}")
        print(f"Título: {b['title']}")
        print(f"Autor:  {b['author']}")
        print(f"ISBN:   {b['isbn']}")
        print("-" * 40)


if __name__ == "__main__":
    main() 
