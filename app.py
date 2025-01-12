from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fothebys.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'  # Required for session management and flash messages
db = SQLAlchemy(app)

# Database model
class AuctionLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_number = db.Column(db.String(10), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    subject_classification = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    estimated_price = db.Column(db.Float, nullable=False)
    auction_date = db.Column(db.DateTime, nullable=False)
    archived = db.Column(db.Boolean, default=False)

ADMIN_USERNAME = "polya"
ADMIN_PASSWORD = generate_password_hash("polya1606")  

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    # Get search and filter parameters from the request
    search_term = request.args.get('search', '') 
    category_filter = request.args.get('category', '')
    year_filter = request.args.get('year', '')

    query = AuctionLot.query.filter_by(archived=False)

    if search_term:
        query = query.filter(
            (AuctionLot.artist.ilike(f'%{search_term}%')) | 
            (AuctionLot.description.ilike(f'%{search_term}%'))
        )

    if category_filter:
        query = query.filter(AuctionLot.category == category_filter)

    if year_filter:
        query = query.filter(AuctionLot.year == int(year_filter))

    lots = query.all()

    categories = [lot.category for lot in AuctionLot.query.distinct(AuctionLot.category).all()]
    years = [lot.year for lot in AuctionLot.query.distinct(AuctionLot.year).all()]

    return render_template('index.html', lots=lots, categories=categories, years=years)

@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect(url_for('login'))
    lots = AuctionLot.query.all()
    return render_template('admin.html', lots=lots)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        lot = AuctionLot(
            lot_number=request.form['lot_number'],
            artist=request.form['artist'],
            year=request.form['year'],
            category=request.form['category'],
            subject_classification=request.form['subject_classification'],
            description=request.form['description'],
            estimated_price=request.form['estimated_price'],
            auction_date=datetime.strptime(request.form['auction_date'], '%Y-%m-%d'),
        )
        db.session.add(lot)
        db.session.commit()
        flash('Auction lot added successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('add_lot.html')

@app.route('/unarchive/<int:lot_id>', methods=['POST'])
def unarchive(lot_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    lot = AuctionLot.query.get_or_404(lot_id)
    lot.archived = False  
    db.session.commit()
    flash('Auction lot unarchived successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/edit/<int:lot_id>', methods=['GET', 'POST'])
def edit(lot_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    lot = AuctionLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.lot_number = request.form['lot_number']
        lot.artist = request.form['artist']
        lot.year = request.form['year']
        lot.category = request.form['category']
        lot.subject_classification = request.form['subject_classification']
        lot.description = request.form['description']
        lot.estimated_price = request.form['estimated_price']
        lot.auction_date = datetime.strptime(request.form['auction_date'], '%Y-%m-%d')
        db.session.commit()
        flash('Auction lot updated successfully!', 'success')
        return redirect(url_for('admin'))
    return render_template('edit_lot.html', lot=lot)

@app.route('/delete/<int:lot_id>', methods=['POST'])
def delete(lot_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    lot = AuctionLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    flash('Auction lot deleted successfully!', 'success')
    return redirect(url_for('admin'))

@app.route('/archive/<int:lot_id>', methods=['POST'])
def archive(lot_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    lot = AuctionLot.query.get_or_404(lot_id)
    lot.archived = True
    db.session.commit()
    flash('Auction lot archived successfully!', 'success')
    return redirect(url_for('admin'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD, password):
            session['user'] = username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)