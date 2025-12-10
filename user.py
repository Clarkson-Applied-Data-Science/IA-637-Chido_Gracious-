from baseObject import baseObject
import hashlib

class user(baseObject):
    def __init__(self):
        self.setup()
        self.roles = [
            {"value": "admin", "text": "admin"},
            {"value": "customer", "text": "customer"},
        ]

    def hashPassword(self, pw):
        pw = pw + "xyz"
        return hashlib.md5(pw.encode("utf-8")).hexdigest()

    def role_list(self):
        return [r["value"] for r in self.roles]

    def verify_new(self):
        self.errors = []
        d = self.data[0]

        if "email" not in d or "@" not in d["email"]:
            self.errors.append("Email must contain @")

        u = user()
        u.getByField("email", d["email"])
        if len(u.data) > 0:
            self.errors.append(f"Email address is already in use. ({d['email']})")

        if len(d.get("password", "")) < 3:
            self.errors.append("Password should be greater than 3 chars.")
        if d.get("password") != d.get("password2"):
            self.errors.append("Retyped password must match.")

        d["password"] = self.hashPassword(d["password"])
        if "password2" in d:
            del d["password2"]

        if d.get("role") not in self.role_list():
            self.errors.append(f"Role must be one of {self.role_list()}")

        return len(self.errors) == 0

    def verify_update(self):
        self.errors = []
        d = self.data[0]

        # Validate email
        if "email" not in d or "@" not in d["email"]:
            self.errors.append("Email must contain @")

        # Check if email already exists for a different user
        u = user()
        u.getByField("email", d["email"])
        if len(u.data) > 0 and u.data[0][u.pk] != d[self.pk]:
            self.errors.append(f"Email address is already in use. ({d['email']})")

        # Handle optional password change
        pw = d.get("password")
        pw2 = d.get("password2")

        if pw2 and len(pw2) > 0:
            # Validating password update
            if not pw or len(pw) < 3:
                self.errors.append("Password should be greater than 3 characters.")
            if pw != pw2:
                self.errors.append("Retyped password must match.")
            else:
                d["password"] = self.hashPassword(pw)
        else:
            # Remove empty password fields so DB is not updated incorrectly
            d.pop("password", None)
            d.pop("password2", None)

        # Validate role
        if d.get("role") not in self.role_list():
            self.errors.append(f"Role must be one of {self.role_list()}")

        return len(self.errors) == 0


    def tryLogin(self, un, pw):
        pw = self.hashPassword(pw)
        self.data = []
        sql = f"SELECT * FROM `{self.tn}` WHERE `email` = %s AND `password` = %s;"
        self.cur.execute(sql, [un, pw])
        for row in self.cur:
            self.data.append(row)
        return len(self.data) == 1

    def all(self):
        sql = f"SELECT * FROM `{self.tn}` ORDER BY user_id ASC"
        self.cur.execute(sql)
        self.data = self.cur.fetchall()
        return self.data


    def getById(self, user_id):
        sql = f"SELECT * FROM `{self.tn}` WHERE user_id = %s"
        self.cur.execute(sql, (user_id,))
        self.data = self.cur.fetchall()
