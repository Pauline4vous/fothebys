from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fothebys.db'  # SQLite database
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Replace with a secure key
db = SQLAlchemy(app)

# Database Model for Auction Lots
class AuctionLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each lot
    lot_number = db.Column(db.String(10), nullable=False, unique=True)  # Lot number
    artist = db.Column(db.String(100), nullable=False)  # Artist's name
    year = db.Column(db.Integer, nullable=False)  # Year of creation
    category = db.Column(db.String(50), nullable=False)  # Category (e.g., Painting, Sculpture)
    description = db.Column(db.Text, nullable=False)  # Description of the lot
    estimated_price = db.Column(db.Float, nullable=False)  # Estimated price
    image = db.Column(db.String(100), nullable=True)  # Image filename (optional)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp of creation
    archived = db.Column(db.Boolean, default=False)  # Whether the lot is archived

# Routes

# Home Page: Displays all active (non-archived) auction lots
@app.route('/')
def index():
    lots = AuctionLot.query.filter_by(archived=False).all()  # Get all non-archived lots
    return render_template('index.html', lots=lots)


# Lot Details Page: Displays details of a specific lot
@app.route('/lot/<int:lot_id>')
def auction_lot(lot_id):
    lot = AuctionLot.query.get_or_404(lot_id)  # Get the lot or return a 404 error
    return render_template('auction_lot.html', lot=lot)


# Admin Panel: Lists all auction lots and provides management options
@app.route('/admin')
def admin():
    lots = AuctionLot.query.all()  # Get all lots (including archived ones)
    return render_template('admin.html', lots=lots)


# Add New Auction Lot: Display form and handle POST submission
@app.route('/add', methods=['GET', 'POST'])
def add_lot():
    if request.method == 'POST':
        # Collect form data
        lot_number = request.form['lot_number']
        artist = request.form['artist']
        year = request.form['year']
        category = request.form['category']
        description = request.form['description']
        estimated_price = request.form['estimated_price']
        # Create a new AuctionLot object
        new_lot = AuctionLot(
            lot_number=lot_number,
            artist=artist,
            year=year,
            category=category,
            description=description,
            estimated_price=estimated_price,
        )
        try:
            db.session.add(new_lot)  # Add to database
            db.session.commit()  # Commit changes
            flash('Auction lot added successfully!', 'success')
            return redirect(url_for('admin'))  # Redirect to admin panel
        except Exception as e:
            flash(f'Error: {e}', 'danger')  # Display error message
            return redirect(url_for('add_lot'))
    return render_template('add_lot.html')  # Render add form


# Edit Auction Lot: Display form with existing data and handle POST submission
@app.route('/edit/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    lot = AuctionLot.query.get_or_404(lot_id)  # Get the lot or return a 404 error
    if request.method == 'POST':
        # Update lot with form data
        lot.lot_number = request.form['lot_number']
        lot.artist = request.form['artist']
        lot.year = request.form['year']
        lot.category = request.form['category']
        lot.description = request.form['description']
        lot.estimated_price = request.form['estimated_price']
        try:
            db.session.commit()  # Commit changes
            flash('Auction lot updated successfully!', 'success')
            return redirect(url_for('admin'))  # Redirect to admin panel
        except Exception as e:
            flash(f'Error: {e}', 'danger')  # Display error message
            return redirect(url_for('edit_lot', lot_id=lot.id))
    return render_template('edit_lot.html', lot=lot)  # Render edit form


# Delete Auction Lot: Remove a lot from the database
@app.route('/delete/<int:lot_id>')
def delete_lot(lot_id):
    lot = AuctionLot.query.get_or_404(lot_id)  # Get the lot or return a 404 error
    try:
        db.session.delete(lot)  # Delete the lot
        db.session.commit()  # Commit changes
        flash('Auction lot deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')  # Display error message
    return redirect(url_for('admin'))  # Redirect to admin panel


# Archive Auction Lot: Marks a lot as archived
@app.route('/archive/<int:lot_id>')
def archive_lot(lot_id):
    lot = AuctionLot.query.get_or_404(lot_id)  # Get the lot or return a 404 error
    lot.archived = True  # Mark as archived
    try:
        db.session.commit()  # Commit changes
        flash('Auction lot archived successfully!', 'success')
    except Exception as e:
        flash(f'Error: {e}', 'danger')  # Display error message
    return redirect(url_for('admin'))  # Redirect to admin panel


# Run the application
if __name__ == '__main__':
    db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)  # Run the app in debug mode