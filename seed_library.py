from user import user

u = user()

u.cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
u.cur.execute("TRUNCATE TABLE Loans;")
u.cur.execute("TRUNCATE TABLE Books;")
u.cur.execute("TRUNCATE TABLE Titles;")
u.cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

titles = [
    ("The Quantum Library",              "Ada Lightman",   "9780000000010", "Science Fiction"),
    ("Data Science for Night Owls",      "Lin Zhao",       "9780000000027", "Non-Fiction"),
    ("Mystery of the Missing Semicolon", "Grace O'Connor", "9780000000034", "Mystery"),
    ("Dragons of Distributed Systems",   "Rahul Banerjee", "9780000000041", "Fantasy"),
    ("Love in the Time of Wi-Fi",        "Sofia Martinez", "9780000000058", "Romance")
]

books = [
    ("New",  "Available", "2025-09-15", 1),
    ("Good", "On Loan",   "2025-09-16", 1),
    ("New",  "Available", "2025-09-20", 2),
    ("Fair", "On Loan",   "2025-09-22", 3),
    ("Good", "Available", "2025-09-25", 3),
    ("New",  "Reserved",  "2025-09-28", 4),
    ("Good", "Available", "2025-10-01", 4),
    ("New",  "On Loan",   "2025-10-03", 5)
]

loans = [
    ("Returned", "2025-10-01", "2025-10-05", 2, 3, 1),
    ("On Loan",  "2025-10-10", "2025-10-20", 4, 4, 2),
    ("Overdue",  "2025-10-12", "2025-10-18", 8, 5, 1),
    ("On Loan",  "2025-10-15", "2025-10-25", 6, 3, 2),
    ("Returned", "2025-10-18", "2025-10-22", 1, 4, 1)
]

u.cur.executemany(
    "INSERT INTO Titles (Title_Name, Author, Isbn, Category) VALUES (%s,%s,%s,%s)",
    titles
)

u.cur.executemany(
    "INSERT INTO Books (`Condition`, `availability_status`, `Date_Added`, `Title_ID`) VALUES (%s,%s,%s,%s)",
    books
)

u.cur.executemany(
    "INSERT INTO Loans (Status, Loan_Date, Return_Date, Book_ID, Member_ID, Staff_ID) VALUES (%s,%s,%s,%s,%s,%s)",
    loans
)

u.conn.commit()

print("Inserted", len(titles), "titles")
print("Inserted", len(books), "books")
print("Inserted", len(loans), "loans")

