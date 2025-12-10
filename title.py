
from baseObject import baseObject

class title(baseObject):
    def __init__(self):
        self.setup()

    # Return all titles
    def getAllTitles(self, order_by='Title_Name'):
        self.data = []
        sql = f"SELECT * FROM Titles"
        if order_by:
            sql += f" ORDER BY {order_by};"
        else:
            sql += ";"
        self.cur.execute(sql)
        for row in self.cur:
            self.data.append(row)

    # Get one title by ID
    def getTitleById(self, title_id):
        self.data = []
        sql = "SELECT * FROM Titles WHERE Title_ID = %s;"
        self.cur.execute(sql, [title_id])
        for row in self.cur:
            self.data.append(row)

    # Add new title
    def addTitle(self, title_name, author, isbn, category):
        d = {
            "Title_Name": title_name,
            "Author": author,
            "Isbn": isbn,
            "Category": category
        }
        self.set(d)
        self.insert()

    # Update title
    def updateTitle(self, title_id, title_name, author, isbn, category):
        self.getTitleById(title_id)
        if not self.data:
            return False

        self.data[0]['Title_Name'] = title_name
        self.data[0]['Author'] = author
        self.data[0]['Isbn'] = isbn
        self.data[0]['Category'] = category
        self.update()
        return True

    # Delete title
    def deleteTitle(self, title_id):
        sql = "DELETE FROM Titles WHERE Title_ID = %s;"
        self.cur.execute(sql, [title_id])
