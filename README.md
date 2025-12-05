# Library Management System
# Final Project – IA 637 / Clarkson University

Group Members

Chido Mbuwayesango

Gracious Chigome

---
## Overview
This project is a Library Management System and it lets library staff and customers work with the same central database of users and books, but with different levels of access.

## Features

### Customer (Patron)

Customers can create an account, log in, and then:
- Browse the library’s collection
- See whether a book is available, reserved or checked out
- View details like author, title, year and condition of the book
- Manage their own profile information


### Administrator (Librarian)

Administrators have extra tools to keep the collection and users up to date. They can:
- Add new books to the system and edit existing records
- Adjust the number of copies and availability of each title
- Create and manage user accounts and roles
- Review basic information about who is using the system
- Edit book details such as title, author, year, and ISBN 

### Analytics Dashboard

Provides a simple overview of library activity, including:

- Total number of registered users  
- Total number of books in the catalogue  
- Quick view of books with no available copies  
- Basic counts of users by role (admin vs. customer)

These summaries help librarians keep the catalogue upto date, see which books are heavily used, understand how the system is being used and quickly spot records that may need attention.

## System Technologies

| Layer              | Technology                                      |
|--------------------|-------------------------------------------------|
| Backend            | Python + Flask                                  |
| Frontend           | HTML, CSS, Jinja2 templates          |
| Database           | MySQL (`ia637` database; tables for users/books/loans/titles)|
| Data Access Layer  | Shared `baseObject` framework and entity classes|


## Database Schema

The system uses four core tables:

**`Users`**
- Stores user credentials, contact information, and role (`admin` or `customer`)
  
**`Books`**
- Tracks individual book records, including copy counts, date added and availability
  
**`Titles`**
- Stores title-level information such as title, author, ISBN, and category
  
**`Loans`**
- Records which user borrowed which book copy and the loan/return dates

Together these tables implement a simple library workflow from user registration → browsing titles → borrowing books → tracking returns.

---
