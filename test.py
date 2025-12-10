from user import user

u = user()

u.cur.execute("SET FOREIGN_KEY_CHECKS = 0;")
u.cur.execute("TRUNCATE TABLE Users;")
u.cur.execute("SET FOREIGN_KEY_CHECKS = 1;")

users = [
    {
        'name': 'John',
        'email': 'john@a.com',
        'role': 'admin',
        'password': '123',
        'password2': '123',
        'phone': '555-0101',
        'join_date': '2025-09-20'
    },
    {
        'name': 'Bean',
        'email': 'bean@a.com',
        'role': 'admin',
        'password': '123',
        'password2': '123',
        'phone': '555-0102',
        'join_date': '2025-09-25'
    },
    {
        'name': 'Alice',
        'email': 'alice@a.com',
        'role': 'customer',
        'password': '123',
        'password2': '123',
        'phone': '555-0103',
        'join_date': '2025-10-05'
    },
    {
        'name': 'Bob',
        'email': 'bob@a.com',
        'role': 'customer',
        'password': '123',
        'password2': '123',
        'phone': '555-0104',
        'join_date': '2025-10-15'
    },
    {
        'name': 'Clara',
        'email': 'clara@a.com',
        'role': 'customer',
        'password': '123',
        'password2': '123',
        'phone': '555-0105',
        'join_date': '2025-10-25'
    }
]

for d in users:
    u.set(d)
    if u.verify_new():
        u.insert()
        print(f"ID {u.data[0][u.pk]} inserted for {u.data[0]['email']}")
    else:
        print(u.errors)

