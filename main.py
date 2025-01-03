from fastapi import FastAPI,status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List

app= FastAPI()

books=[
    {"id":1, "title":"The Da Vinci Code", "author":"Dan Brown",
     "publisher":"Doubleday", "published_date":"2003-03-18", 
     
     "page_count":1234,
     "language":"English"},
     {
            "id":2, "title":"The Alchemist", "author":"Paulo Coelho",
            "publisher":"HarperTorch", "published_date":"1988-01-01",
            "page_count":208,
            "language":"English"
     },
        {
                "id":3, "title":"The Little Prince", "author":"Antoine de Saint-Exupéry",
                "publisher":"Reynal & Hitchcock", "published_date":"1943-04-06",
                "page_count":96,
                "language":"French"
        },
        {
                "id":4, "title":"The Hobbit", "author":"J.R.R. Tolkien",
                "publisher":"Allen & Unwin", "published_date":"1937-09-21",
                "page_count":310,
                "language":"English"
        },
        {
                "id":5, "title":"Harry Potter and the Philosopher's Stone", "author":"J.K. Rowling",
                "publisher":"Bloomsbury", "published_date":"1997-06-26",
                "page_count":223,
                "language":"English"
        }
    
]



class Book(BaseModel):
    id:int
    title:str
    author:str
    publisher:str
    published_date:str
    page_count:int
    language:str


class BookUpdateModel(BaseModel):  
    title:str
    author:str
    publisher:str 
    page_count:int
    language:str


@app.get('/books' , response_model=List[Book])
async def get_all_books():
    return books

# create 
@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_data:Book)->dict:
    new_book = book_data.model_dump()

    books.append(new_book)
    return new_book

    


# read 
@app.get('/book/{book_id}')
async def get_book(book_id:int)->dict:
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Book Not Found")




# update 
@app.patch('/book/{book_id}')
async def update_book(book_id:int, book_update_data:BookUpdateModel)->dict:
    for book in books:
        if book['id'] == book_id:
            book['title']= book_update_data.title
            book['author']= book_update_data.author
            book['publisher']= book_update_data.publisher
            book['page_count']= book_update_data.page_count
            book['language']= book_update_data.language


            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Book Not Found")    



# delete 
@app.delete('/book/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                         detail="Book Not Found")   


