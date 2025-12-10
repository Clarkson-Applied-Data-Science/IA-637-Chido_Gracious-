from user import user

u = user()
u.cur.execute("SET FOREIGN_KEY_CHECKS=0;")
u.truncate()
u.cur.execute("SET FOREIGN_KEY_CHECKS=1;")

seed_users = [
    {"name": "Alice", "email": "alice@a.com", "role": "admin"},
    {"name": "Brian", "email": "brian@a.com", "role": "admin"},
    {"name": "John", "email": "john@a.com", "role": "customer"},
    {"name": "Mary", "email": "mary@a.com", "role": "customer"},
    {"name": "Sam", "email": "sam@a.com", "role": "customer"},
    {"name": "Rita", "email": "rita@a.com", "role": "customer"},
]

for rec in seed_users:
    d = {
        "name": rec["name"],
        "email": rec["email"],
        "role": rec["role"],
        "password": "123",
        "password2": "123",
    }
    u.set(d)
    if u.verify_new():
        u.insert()
        print(f"Inserted {rec['name']} ({rec['email']}) as {rec['role']}")
    else:
        print(f"Error inserting {rec['email']}: {u.errors}")
