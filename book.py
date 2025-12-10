from baseObject import baseObject

class book(baseObject):
    def __init__(self):
        self.setup()

    # Get all books with title info
    def getAllBooks(self):
        self.data = []
        sql = """
            SELECT
                b.Book_ID,
                t.Title_Name,
                t.Author,
                t.Isbn,
                t.Category,
                b.Condition,
                b.availability_status,
                b.Date_Added
            FROM Books b
            JOIN Titles t ON b.Title_ID = t.Title_ID
            ORDER BY b.Book_ID;
        """
        self.cur.execute(sql)
        for row in self.cur:
            self.data.append(row)

    # Get book by ID with title details
    def getBookById(self, book_id):
        self.data = []
        sql = """
            SELECT
                b.Book_ID,
                t.Title_Name,
                t.Author,
                t.Isbn,
                b.Condition,
                b.availability_status,
                b.Date_Added,
                b.Title_ID
            FROM Books b
            JOIN Titles t ON b.Title_ID = t.Title_ID
            WHERE b.Book_ID = %s;
        """
        self.cur.execute(sql, [book_id])
        for row in self.cur:
            self.data.append(row)

    # Update condition & availability
    def updateBook(self, book_id, condition, status):
        self.getById(book_id)
        if not self.data:
            return False

        self.data[0]['Condition'] = condition
        self.data[0]['availability_status'] = status
        self.update()
        return True

    # Borrow book
    def borrowBook(self, book_id):
        sql = """
            UPDATE Books
            SET availability_status = 'On Loan'
            WHERE Book_ID = %s AND availability_status = 'Available';
        """
        self.cur.execute(sql, [book_id])
        return self.cur.rowcount > 0

    # Add new book
    def addBook(self, condition, availability_status, date_added, title_id):
        d = {
            "Condition": condition,
            "availability_status": availability_status,
            "Date_Added": date_added,
            "Title_ID": title_id
        }
        self.set(d)
        self.insert()

    # Delete book
    def deleteBook(self, book_id):
        self.deleteById(book_id)
