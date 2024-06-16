from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:password@localhost/recipe'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Recipe model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)

def create_tables_and_sample_data():
    with app.app_context():
        db.create_all()
        if not Recipe.query.first():
            sample_recipes = [
                Recipe(name='Spaghetti Bolognese', ingredients='Spaghetti, ground beef, tomato sauce, garlic, onions, olive oil, salt, pepper', steps='1. Cook the spaghetti. 2. Prepare the sauce. 3. Mix spaghetti with sauce. 4. Serve hot.'),
                Recipe(name='Chicken Curry', ingredients='Chicken, curry powder, coconut milk, onions, garlic, ginger, salt, pepper', steps='1. Cook the chicken. 2. Prepare the curry sauce. 3. Mix chicken with sauce. 4. Serve hot with rice.'),
                Recipe(name='Vegetable Stir Fry', ingredients='Broccoli, bell peppers, soy sauce, garlic, onions, olive oil, salt, pepper', steps='1. Prepare the vegetables. 2. Stir fry the vegetables. 3. Add soy sauce. 4. Serve hot.')
            ]
            db.session.bulk_save_objects(sample_recipes)
            db.session.commit()

create_tables_and_sample_data()

@app.route('/')
def index():
    recipes = Recipe.query.all()
    return render_template('index.html', recipes=recipes)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit-recipe', methods=['GET', 'POST'])
def submit_recipe():
    if request.method == 'POST':
        new_recipe = Recipe(
            name=request.form['title'],
            ingredients=request.form['ingredients'],
            steps=request.form['steps']
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('submit.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
