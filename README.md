# Library

## System Description

System manager for libraryIn the system:

- Managing the books.
- Managing the Library members.
- The system store data in tables in MySql.
- The connection to the DataBases is done by FastAPI.
- The system allows amount of actions, like full CRUD, and more.

## MySql & Docker instructions.

### Connection to MySql

```bash
docker run --name library-sql -e MYSQL_ROOT_PASSWORD=root -d -p 3310:3306 mysql:latest
```

### Connection Info

- Host= localhost
- Port= 3310
- DataBase= library_db
- User= root
- Password= root

## Folders & Files structure

```bash
│
├── app/
│   ├── main.py
│   ├── database/
│   │   ├── db_connection.py
│   │   ├── book_db.py
│   │   └── member_db.py
│   ├── routes/
│   │   ├── book_routes.py
│   │   ├── member_routes.py
│   │   └── report_routes.py
│   └── logs/
│       └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore

```

## Tables structure

### books

- id= PK auto_increment.
- title= book title max 50 chars must value.
- author= author name max 50 chars must value.
- genre= must values(Fiction | Non-Fiction | Science | History | Other).
- is_available= boolean if the book available.
- borrowed_by_member_id= hold the member id who borrow the book.

### members

- id= PK auto_increment.
- name= member name max 50 chars must value.
- email= unique mail adders max 50 chars must value.
- is_active= boolean if the member active (if not the member cannot borrow book).
- total_borrows= sum the amount of borrows.

## System rules

### Create book

User send title/author/genre,
The system adding is_available=True, borrowed_by=NULL.

### genre

Must be Fiction / Non-Fiction / Science / History / Other,
Other value return error,
Must to check when POST or PATCH.

### Creating member

User send name/email,
The system adding is_active=True, total_borrows=0.

### email

Must be unique,
if already exist return error.

### Inactive member

If member is inactive he cannot borrow a book.

### Book is unavailable

Cannot borrow book that is unavailable.

### Max books

Member can borrow max 3 books.

### Return borrow book

Member can return book only if he borrowed it.

## Endpoints list

### Books

| Method | Endpoint                       | Description             |
| ------ | ------------------------------ | ----------------------- |
| POST   | /books                         | Creating book           |
| GET    | /books                         | Show all books          |
| GET    | /books/{id}                    | Show book by ID         |
| PUT    | /books/{id}                    | Update Book info        |
| PUT    | /books/{id}/borrow/{member_id} | Borrow book to member   |
| PUT    | /books/{id}/return/{member_id} | return book from member |

### Members

| Method | Endpoint                 | Description        |
| ------ | ------------------------ | ------------------ |
| POST   | /members                 | Creating member    |
| GET    | /members                 | Show all members   |
| GET    | /members/{id}            | Show member by ID  |
| PUT    | /members/{id}            | Update member info |
| PUT    | /members/{id}/deactivate | Deactivate member  |
| PUT    | /members/{id}/activate   | Activate member    |

### Reports

| Method | Endpoint                | Description                    |
| ------ | ----------------------- | ------------------------------ |
| GET    | /reports/summary        | General report                 |
| GET    | /reports/books-by-genre | Books by genre                 |
| GET    | /reports/top-member     | The member who borrow the most |

## System Flow

## Run instruction

### Option 1

Run main.py file,  
In the CLI press on the URL or copy it and pase it in the browser.

### Option 2

Paste it in the CLI

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```
