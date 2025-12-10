# Library Management System
# Final Project – IA 637 / Clarkson University

Group Members

Chido Mbuwayesango

Gracious Chigome

---
## Overview

This project is a Library Management System designed for a community library. It gives both staff and customers a simple way to interact with the same central database of users, titles, books, and loans, while enforcing different levels of access based on each user’s role.

The purpose of this Library Management System project is to digitize and streamline core library operations by providing a simple web-based platform for managing books, users, and loans. It allows patrons to search the catalogue, view book details, and manage their own borrowing, while giving librarians/administrators tools to create and update user accounts, maintain the book collection, and track check-outs and returns in real time. Overall, the system aims to replace manual, paper-based processes with an accurate, data-driven application that supports efficient day-to-day management of a community library.

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


### Analytics Summary View

![Analytics dashboard summary](images/analytics.png)

### Most Borrowed Titles View

![Most borrowed titles chart](images/mostborrowed.png)


## Key SQL and Analytical Queries

| Feature / Use Case | SQL Query (simplified) | Explanation |
|--------------------|------------------------|------------|
| User login | ```sql SELECT * FROM Users WHERE email = %s AND password = %s; ``` | Checks whether the entered email and password match a record in the `Users` table. Used on the login form to authenticate admins and customers. |
| List all users | ```sql SELECT user_id, name, email, role, phone, join_date FROM Users ORDER BY name; ``` | Returns the full list of registered users, sorted by name. Used on the admin “Users” page to view and manage members. |
| Library catalogue (books with titles) | ```sql SELECT b.Book_ID, t.Title_Name, t.Author, b.Condition, b.availability_status FROM Books b JOIN Titles t ON b.Title_ID = t.Title_ID ORDER BY t.Title_Name; ``` | Combines `Books` and `Titles` so the app can show each physical book copy together with its title and author. Used on the main catalogue/list of books. |
| Search by title or author | ```sql SELECT t.Title_Name, t.Author, t.ISBN, t.Category FROM Titles t WHERE t.Title_Name LIKE %s OR t.Author LIKE %s; ``` | Searches the `Titles` table using a keyword in either the title or author fields. Used on the customer search page. |
| Record a new loan | ```sql INSERT INTO Loans (Status, Loan_Date, Return_Date, Book_ID, Member_ID, Staff_ID) VALUES (%s, %s, %s, %s, %s, %s); ``` | Inserts a new row into `Loans` when a librarian checks out a book to a member. Tracks which user borrowed which copy and when it is due. |
| Update book availability | ```sql UPDATE Books SET availability_status = %s WHERE Book_ID = %s; ``` | Changes a book’s availability (for example from `available` to `checked out` or back again) when a loan is created or returned. |
| Total registered users (analytics) | ```sql SELECT COUNT(*) AS total_users FROM Users; ``` | Simple aggregate used on the Analytics Dashboard to show how many users are currently registered in the system. |
| Total books in catalogue (analytics) | ```sql SELECT COUNT(*) AS total_books FROM Books; ``` | Counts all book copies in the `Books` table. Displayed on the dashboard as “Total Books”. |
| Availability snapshot (available vs. not) | ```sql SELECT availability_status, COUNT(*) AS count FROM Books GROUP BY availability_status; ``` | Groups books by `availability_status` (e.g. `available`, `checked out`, `reserved`) to show how many copies are in each state. Used for the dashboard availability summary. |
| Daily loan count | ```sql SELECT Loan_Date, COUNT(*) AS daily_loans FROM Loans GROUP BY Loan_Date ORDER BY Loan_Date; ``` | Aggregates the number of loans per day. Used to understand busy vs. quiet days in the library. |
| Top borrowed titles (last 30 days) | ```sql SELECT t.Title_Name, COUNT(*) AS loans_last_30_days FROM Loans l JOIN Books b ON l.Book_ID = b.Book_ID JOIN Titles t ON b.Title_ID = t.Title_ID WHERE l.Loan_Date >= CURDATE() - INTERVAL 30 DAY GROUP BY t.Title_ID, t.Title_Name ORDER BY loans_last_30_days DESC LIMIT 5; ``` | Counts how many times each title has been borrowed in the last 30 days and returns the top 5. Used on the dashboard to highlight popular books. |
| Active borrowers (last 30 days) | ```sql SELECT COUNT(DISTINCT Member_ID) AS active_borrowers FROM Loans WHERE Loan_Date >= CURDATE() - INTERVAL 30 DAY; ``` | Counts distinct members who borrowed at least one book in the last 30 days. Used as an “Active Users” metric on the dashboard. |





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

## Relational Schema

![Library relational schema](images/schema.png)

---

## Test Login Credentials

### **Admin Account**

| Field    | Value           |
|--------- |-----------------|
| Email    | **alice@a.com** |
| Password | **123**         |
| Role     | **admin**       |

### **Customer Account**

| Field    | Value          |
|--------- |----------------|
| Email    | **john@a.com** |
| Password | **123**        |
| Role     | **customer**   |

---

## Setup Instructions

1. **Download or Clone the Project**  
   Clone this repository or download the project as a ZIP file and extract it to a folder on your machine.

2. **Configure the Database**  
   Open your MySQL / phpMyAdmin environment.  
   Create the database: `ia637_LibraryManagementSystem`.  
   Run the SQL script included with the project to create the `Users`, `Titles`, `Books`, and `Loans` tables and insert sample data.

3. **Add Your Database Credentials**  
   In the project folder, locate `config.example.yml`.  
   Make a copy and rename it: `config.yml`.  
   Then fill in your MySQL login details:

   ```yaml
   db:
     host: "your_local_host"
     user: "root"
     pw: "your_password"
     db: "your_database_name"

 4. **Run The Application**
    
    Open a terminal or command prompt, navigate to the project folder, and run: python app.py
    
    Then open your browser and go to: http://127.0.0.1:5000
    
    Log in using one of the test accounts listed in the Test Login Credentials section.

---

## Analytics Dashboard

Our system includes a simple **Analytics Dashboard** that gives the admins (librarians) a quick view of how the library collection is being used. These analytical queries are based on the `Users`, `Titles`, `Books`, and `Loans` tables.

1. **Daily Loan Count**  
   Shows how many books are checked out on each day.
    
   This helps the library understand busy vs. quiet days and plan staffing accordingly.

3. **Top Borrowed Titles (Last 30 Days)**  
   Lists the titles with the highest number of loans in the last month.  
   This highlights popular books and can inform purchasing decisions or additional copies.

4. **Active Borrowers**  
   Counts the number of distinct users who have borrowed at least one book within a chosen time period.  
   This metric shows how many members are actively using the library, not just registered.

5. **Book Availability Snapshot**  
   Calculates how many titles currently have at least one available copy versus those that are fully checked out.  
   This gives a quick sense of overall collection availability and potential bottlenecks in high-demand areas.

All queries are executed inside the Flask routes in `app.py` and the results are presented to librarians as simple tables and summary counts on the admin pages.

## Summary

In short, this project delivers a complete library workflow:

- Patrons discover and borrow books through a simple self-service interface.

- Admins maintain the catalogue, manage member accounts, and track loans/returns.

- All activity is stored in a central database, providing accurate, up-to-date information about the library’s collection and usage.



  

