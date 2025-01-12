from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fothebys.db'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)


class AuctionLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_number = db.Column(db.String(10), nullable=False, unique=True)
    artist = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    subject_classification = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    estimated_price = db.Column(db.Float, nullable=False)
    auction_date = db.Column(db.DateTime, nullable=True)
    image = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    archived = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<AuctionLot {self.lot_number}>'


@app.route('/')
def index():
    lots = AuctionLot.query.filter_by(archived=False).all()
    return render_template('index.html', lots=lots)


@app.route('/lot/<int:lot_id>')
def auction_lot(lot_id):
    lot = AuctionLot.query.get_or_404(lot_id)
    return render_template('auction_lot.html', lot=lot)


@app.route('/admin')
def admin():
    lots = AuctionLot.query.all()
    return render_template('admin.html', lots=lots)


@app.route('/add', methods=['GET', 'POST'])
def add_lot():
    if request.method == 'POST':
        lot_number = request.form['lot_number']
        artist = request.form['artist']
        year = request.form['year']
        category = request.form['category']
        subject_classification = request.form['subject_classification']
        description = request.form['description']
        estimated_price = request.form['estimated_price']
        auction_date = request.form['auction_date']

        new_lot = AuctionLot(
            lot_number=lot_number,
            artist=artist,
            year=year,
            category=category,
            subject_classification=subject_classification,
            description=description,
            estimated_price=estimated_price,
            auction_date=datetime.strptime(auction_date, '%Y-%m-%d') if auction_date else None
        )

        db.session.add(new_lot)
        db.session.commit()
        flash('Auction lot added successfully!', 'success')
        return redirect(url_for('admin'))

    return render_template('add_lot.html')


@app.route('/edit/<int:lot_id>', methods=['GET', 'POST'])
def edit_lot(lot_id):
    lot = AuctionLot.query.get_or_404(lot_id)
    if request.method == 'POST':
        lot.lot_number = request.form['lot_number']
        lot.artist = request.form['artist']
        lot.year = request.form['year']
        lot.category = request.form['category']
        lot.subject_classification = request.form['subject_classification']
        lot.description = request.form['description']
        lot.estimated_price = request.form['estimated_price']
        auction_date = request.form['auction_date']
        lot.auction_date = datetime.strptime(auction_date, '%Y-%m-%d') if auction_date else None

        db.session.commit()
        flash('Auction lot updated successfully!', 'success')
        return redirect(url_for('admin'))

    return render_template('edit_lot.html', lot=lot)


@app.route('/delete/<int:lot_id>')
def delete_lot(lot_id):
    lot = AuctionLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    flash('Auction lot deleted successfully!', 'success')
    return redirect(url_for('admin'))


@app.route('/archive/<int:lot_id>')
def archive_lot(lot_id):
    lot = AuctionLot.query.get_or_404(lot_id)
    lot.archived = True
    db.session.commit()
    flash('Auction lot archived successfully!', 'success')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)