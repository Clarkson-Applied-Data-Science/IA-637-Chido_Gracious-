from baseObject import baseObject

class loan(baseObject):
    def __init__(self):
        self.setup()

    def getAllLoans(self, order_by="Loan_ID"):
        self.data = []
        sql = "SELECT * FROM Loans"
        if order_by:
            sql += f" ORDER BY {order_by};"
        else:
            sql += ";"
        self.cur.execute(sql)
        for row in self.cur:
            self.data.append(row)

    def getLoanById(self, loan_id):
        self.data = []
        sql = "SELECT * FROM Loans WHERE Loan_ID = %s;"
        self.cur.execute(sql, [loan_id])
        for row in self.cur:
            self.data.append(row)

    def createLoan(self, status, loan_date, return_date, book_id, member_id, staff_id):
        d = {
            "Status": status,
            "Loan_Date": loan_date,
            "Return_Date": return_date,
            "Book_ID": book_id,
            "Member_ID": member_id,
            "Staff_ID": staff_id
        }
        self.set(d)
        self.insert()

    def updateLoan(self, loan_id, status, loan_date, return_date):
        self.getLoanById(loan_id)
        if not self.data:
            return False

        self.data[0]['Status'] = status
        self.data[0]['Loan_Date'] = loan_date
        self.data[0]['Return_Date'] = return_date
        self.update()
        return True

    def deleteLoan(self, loan_id):
        sql = "DELETE FROM Loans WHERE Loan_ID = %s;"
        self.cur.execute(sql, [loan_id])

    def getLoansDetailed(self):
        self.data = []
        sql = """
            SELECT 
                l.Loan_ID,
                l.Status,
                l.Loan_Date,
                l.Return_Date,
                b.Book_ID,
                t.Title_Name,
                u.name AS MemberName
            FROM Loans l
            JOIN Books b ON l.Book_ID = b.Book_ID
            JOIN Titles t ON b.Title_ID = t.Title_ID
            JOIN Users u ON l.Member_ID = u.user_id
            ORDER BY l.Loan_ID;
        """
        self.cur.execute(sql)
        for row in self.cur:
            self.data.append(row)

    # ✅ THIS MUST BE INSIDE THE CLASS
    def getLoanDetailedById(self, loan_id):
        self.data = []
        sql = """
            SELECT 
                l.Loan_ID,
                l.Status,
                l.Loan_Date,
                l.Return_Date,
                u.name AS MemberName,
                t.Title_Name
            FROM Loans l
            JOIN Users u ON l.Member_ID = u.user_id
            JOIN Books b ON l.Book_ID = b.Book_ID
            JOIN Titles t ON b.Title_ID = t.Title_ID
            WHERE l.Loan_ID = %s;
        """
        self.cur.execute(sql, [loan_id])
        for row in self.cur:
            self.data.append(row)
