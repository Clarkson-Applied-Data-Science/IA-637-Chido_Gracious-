from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory
from flask_session import Session
from datetime import timedelta, date
import time
from flask import Flask, render_template, request, redirect, session, url_for, flash
from user import user
from book import book
from title import title
from loan import loan

app = Flask(__name__, static_url_path='')

app.config['SECRET_KEY'] = 'sdfvbgfdjeR5y5r'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=5)
sess = Session()
sess.init_app(app)


@app.route('/')
def home():
    return redirect('/login')


@app.context_processor
def inject_user():
    """Make current user available as 'me' in templates."""
    return dict(me=session.get('user'))


# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    un = request.form.get('email')
    pw = request.form.get('password')

    if un and pw:
        u = user()
        if u.tryLogin(un, pw):
            session['user'] = u.data[0]
            session['active'] = time.time()
            return redirect('/main')
        else:
            return render_template('login.html', msg='Incorrect email or password.')

    return render_template('login.html', msg='Welcome back')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


# ================= MAIN MENU =================
@app.route('/main')
def main():
    if not checkSession():
        return redirect('/login')
    return render_template('main.html')


#============Profile==========================

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not checkSession():
        return redirect('/login')

    u = user()
    u.getById(session['user']['user_id'])
    me = u.data[0]  # logged-in user

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        # Update phone
        if form_type == "phone":
            new_phone = request.form.get("phone")
            if new_phone:
                u.data[0]['phone'] = new_phone
                u.update()
                session['user']['phone'] = new_phone
                flash("Phone updated successfully!", "success")
            else:
                flash("Invalid phone number.", "danger")

        # Update password
        elif form_type == "password":
            current_pw = request.form.get("current_pw")
            new_pw = request.form.get("new_pw")
            confirm_pw = request.form.get("confirm_pw")

            hashed_current = u.hashPassword(current_pw)

            if hashed_current != me['password']:
                flash("Current password is incorrect.", "danger")
            elif new_pw != confirm_pw:
                flash("New passwords do not match.", "danger")
            elif len(new_pw) < 3:
                flash("Password must be at least 3 characters.", "danger")
            else:
                me['password'] = u.hashPassword(new_pw)
                u.update()
                flash("Password changed successfully!", "success")

        return redirect('/profile')

    return render_template('profile.html', user=me)

# ---------------- REGISTER ACCOUNT ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    u = user()

    if request.method == 'POST':
        d = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'role': 'customer',
            'phone': request.form.get('phone'),
            'join_date': date.today().strftime('%Y-%m-%d'),
            'password': request.form.get('password'),
            'password2': request.form.get('password2'),
        }

        u.set(d)
        if u.verify_new():
            u.insert()
            return render_template('ok_dialog.html',
                                   msg=f"User {u.data[0]['email']} registered.")
        else:
            return render_template('register.html', obj=u)

    # Display blank registration form
    u.createBlank()
    return render_template('register.html', obj=u)


#============ User management ==============

@app.route('/users/manage')
def manage_users():
    if not checkSession(): 
        return redirect('/login')
    if session['user']['role'] != 'admin': 
        return redirect('/main')

    u = user()
    users = u.all()
    return render_template('users.html', users=users)


#================= edit user =======================
@app.route('/users/edit/<int:user_id>', methods=['GET','POST'])
def edit_user(user_id):
    if not checkSession(): 
        return redirect('/login')
    if session['user']['role'] != 'admin': 
        return redirect('/main')

    u = user()
    u.getById(user_id)

    if request.method == 'POST':
        updated = {
            "user_id": user_id,
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "role": request.form.get("role"),
            "password": request.form.get("password"),
            "password2": request.form.get("password2")
        }
        u.set(updated)

        if u.verify_update():
            u.update()
            return redirect('/users/manage')
        else:
            return render_template('edit_user.html', user=u.data[0], errors=u.errors)

    return render_template('edit_user.html', user=u.data[0])

#================== add user =====================
@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if not checkSession(): 
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/main')

    if request.method == 'POST':
        u = user()
        d = request.form.to_dict()

        from datetime import date
        d["join_date"] = date.today().isoformat()

        u.set(d)
        if u.verify_new():
            u.insert()
            return redirect('/users/manage')
        else:
            return render_template("add_user.html", errors=u.errors, data=d)

    return render_template("add_user.html", errors=None, data={})

# ================= BOOKS =================
@app.route('/books')
def books():
    if not checkSession():
        return redirect('/login')

    b = book()
    b.getAllBooks()

    return render_template('books.html', books=b.data)

#=================== edit books ===================
@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    if not checkSession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/books')

    b = book()
    b.getBookById(book_id)

    if not b.data:
        return redirect('/books')

    if request.method == 'POST':
        condition = request.form.get('Condition')
        status = request.form.get('availability_status')
        b.updateBook(book_id, condition, status)
        return redirect('/books')

    return render_template('edit_book.html', book=b.data[0])

#============== borrow books=================
@app.route('/books/<int:book_id>/borrow')
def borrow_book(book_id):
    if not checkSession():
        return redirect('/login')

    b = book()
    b.borrowBook(book_id)
    return redirect('/books')

#================ add new book ===========
@app.route('/books/new', methods=['GET', 'POST'])
def create_book():
    if not checkSession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/main')

    if request.method == 'POST':
        b = book()
        d = {
            "Title_ID": request.form['title_id'],
            "Condition": request.form['condition'],
            "availability_status": request.form['availability_status'],
            "Date_Added": request.form['date_added']
        }
        b.set(d)
        b.insert()
        return redirect('/books')

    t = title()
    t.getAllTitles()
    return render_template('create_book.html', titles=t.data)


# ================= TITLES =================
@app.route('/titles')
def titles():
    if not checkSession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/main')

    t = title()
    t.getAllTitles()
    return render_template('titles.html', titles=t.data)


@app.route('/titles/new', methods=['GET', 'POST'])
def create_title():
    if not checkSession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/main')

    if request.method == 'POST':
        t = title()
        t.addTitle(
            request.form['title_name'],
            request.form['author'],
            request.form['isbn'],
            request.form['category']
        )
        return redirect('/titles')

    return render_template('create_title.html')


@app.route('/titles/edit/<int:title_id>', methods=['GET', 'POST'])
def edit_title(title_id):
    if not checkSession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/main')

    t = title()
    t.getTitleById(title_id)

    if not t.data:
        return redirect('/titles')

    if request.method == 'POST':
        t.updateTitle(
            title_id,
            request.form['title_name'],
            request.form['author'],
            request.form['isbn'],
            request.form['category']
        )
        return redirect('/titles')

    return render_template('edit_title.html', title=t.data[0])


# ================= LOANS =================
@app.route('/loans')
def loans():
    if not checkSession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/main')

    l = loan()
    l.getLoansDetailed()

    return render_template('loans.html', loans=l.data)


@app.route('/loans/new', methods=['GET', 'POST'])
def new_loan():
    if not checkSession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/main')

    if request.method == 'POST':
        l = loan()
        l.createLoan(
            request.form['status'],
            request.form['loan_date'],
            request.form['return_date'],
            request.form['book_id'],
            request.form['member_id'],
            session['user']['user_id']
        )
        return redirect('/loans')

    # members dropdown
    u = user()
    u.cur.execute("SELECT user_id, name FROM Users")
    members = u.cur.fetchall()

    # books dropdown
    b = book()
    b.cur.execute("""
        SELECT b.Book_ID, t.Title_Name
        FROM Books b
        JOIN Titles t ON b.Title_ID = t.Title_ID
    """)
    books = b.cur.fetchall()

    return render_template('create_loan.html', members=members, books=books)


@app.route('/loans/edit/<int:loan_id>', methods=['GET', 'POST'])
def edit_loan(loan_id):
    if not checkSession(): return redirect('/login')
    if session['user']['role'] != 'admin': return redirect('/main')

    l = loan()
    l.getLoanDetailedById(loan_id)
    loan_data = l.data[0]  # loan row

    if request.method == 'POST':
        new_status = request.form['status']

        l.updateLoan(
            loan_id,
            new_status,
            request.form['loan_date'],
            request.form['return_date']
        )

        # -- Automatic Book Availability Fix --
        if new_status == 'Returned':
            # use the correct column from loan_data
            book_id = loan_data.get('book_id') or loan_data.get('Book_ID')

            if book_id:
                b = book()
                b.updateBook(
                    book_id,
                    condition=loan_data.get('Condition', 'Good'),
                    availability_status='Available'
                )

        return redirect('/loans')

    return render_template('edit_loan.html', loan=loan_data)


# ================= ANALYTICS =================
@app.route('/analytics')
def analytics():
    if not checkSession():
        return redirect('/login')
    if session['user']['role'] != 'admin':
        return redirect('/main')

    b = book()
    l = loan()
    t = title()

    # --- basic counts ---
    b.cur.execute("SELECT COUNT(*) AS total FROM Books")
    total_books = b.cur.fetchone()['total']

    b.cur.execute("SELECT COUNT(*) AS available FROM Books WHERE availability_status = 'Available'")
    available_books = b.cur.fetchone()['available']

    borrowed_books = total_books - available_books

    # --- monthly trend of loans ---
    l.cur.execute("""
        SELECT DATE_FORMAT(Loan_Date, '%Y-%m') AS month, COUNT(*) AS total
        FROM Loans
        GROUP BY month
        ORDER BY month
    """)
    loan_trend = l.cur.fetchall()
    loan_trend_labels = [row['month'] for row in loan_trend]
    loan_trend_values = [row['total'] for row in loan_trend]

    # --- category breakdown (from Titles) ---
    t.cur.execute("SELECT Category, COUNT(*) AS total FROM Titles GROUP BY Category")
    category_data = t.cur.fetchall()
    category_labels = [row['Category'] for row in category_data]
    category_values = [row['total'] for row in category_data]

    # --- top borrowed titles ---
    l.cur.execute("""
        SELECT t.Title_Name, COUNT(*) AS count
        FROM Loans l
        JOIN Books b ON l.Book_ID = b.Book_ID
        JOIN Titles t ON b.Title_ID = t.Title_ID
        GROUP BY t.Title_Name
        ORDER BY count DESC
        LIMIT 5
    """)
    top_titles = l.cur.fetchall()
    top_title_labels = [row['Title_Name'] for row in top_titles]
    top_title_values = [row['count'] for row in top_titles]

    return render_template(
        'analytics.html',
        total_books=total_books,
        available_books=available_books,
        borrowed_books=borrowed_books,
        # raw data (for map(attribute=...) if you use it)
        loan_trend=loan_trend,
        category_data=category_data,
        top_titles=top_titles,
        # flattened arrays (for direct JS use with |tojson)
        loan_trend_labels=loan_trend_labels,
        loan_trend_values=loan_trend_values,
        category_labels=category_labels,
        category_values=category_values,
        top_title_labels=top_title_labels,
        top_title_values=top_title_values,
    )


# ================= SESSION CHECK =================
def checkSession():
    """Return True if the session is still active, else False."""
    if 'active' in session:
        if time.time() - session['active'] > 1200:  # 20-minute timeout
            session.clear()
            return False
        session['active'] = time.time()
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True)
