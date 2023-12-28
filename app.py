# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import joblib


# Load the trained Logistic Regression model
model = joblib.load(
    "C:/Users/hp/Desktop/SEM6/Thesis/logistic_regression_model.joblib")

# Initialize Flask application
app = Flask(__name__)

app.secret_key = 'your_secret_key_here'




@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('register'))

# Define a route for the registration page


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration logic here

        # Redirect to the login page after registration
        return redirect(url_for('login'))

    return render_template('register.html')

# Define a route for the login page


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Add your login logic here
        # For simplicity, I'm using a session variable to store the username
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    return render_template('login.html')  # Create this HTML file


# Define a route to handle the form submission
# Define a route to handle the form submission
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Get user input from the form
        quantity = float(request.form['quantity'])
        transaction_amount = float(request.form['transaction_amount'])
        rate = float(request.form['rate'])
        num_of_ratings = int(request.form['num_of_ratings'])
        avg_cost = float(request.form['avg_cost'])
        online_order = request.form['online_order']
        table_booking = request.form['table_booking']
        type_of_food = request.form['type_of_food']
        restaurant_type = request.form['restaurant_type']
        area = request.form['area']
        local_address = request.form['local_address']

        # Convert 'online_order' and 'table_booking' to numerical values
        online_order_numeric = 1 if online_order.lower() == 'yes' else 0
        table_booking_numeric = 1 if table_booking.lower() == 'yes' else 0

        # Create a DataFrame with user input
        user_input = pd.DataFrame({
            'quantity': [quantity],
            'transaction_amount': [transaction_amount],
            'rate (out of 5)': [rate],
            'num of ratings': [num_of_ratings],
            'avg cost (two people)': [avg_cost],
            'online_order': [online_order_numeric],
            'table booking': [table_booking_numeric],
            'Type of Food': [type_of_food],
            'restaurant type': [restaurant_type],
            'area': [area],
            'local address': [local_address]
        })

        # One-hot encode categorical features in user input
        user_input_encoded = pd.get_dummies(
            user_input, columns=['Type of Food', 'restaurant type', 'area', 'local address'])

        # Use the feature names provided during training for one-hot encoded columns
        one_hot_columns = ['quantity', 'transaction_amount', 'rate (out of 5)', 'num of ratings',
                           'avg cost (two people)', 'online_order', 'table booking',
                           'Type of Food_Beverages', 'restaurant type_Beverage Shop',
                           'restaurant type_Beverage Shop, Dessert Parlor',
                           'restaurant type_Delivery', 'restaurant type_Food Court',
                           'restaurant type_Food Court, Beverage Shop',
                           'restaurant type_Quick Bites', 'area_Banashankari',
                           'area_Bannerghatta Road', 'area_Basavanagudi', 'area_Bellandur',
                           'area_Brigade Road', 'area_Brookefield',
                           'area_Byresandra,Tavarekere,Madiwala', 'area_Electronic City',
                           'area_Indiranagar', 'area_Jayanagar', 'area_Kalyan Nagar',
                           'area_Kammanahalli', 'area_Koramangala 5th Block',
                           'area_Koramangala 7th Block', 'area_Lavelle Road', 'area_Malleshwaram',
                           'area_Marathahalli', 'area_New BEL Road', 'local address_BTM',
                           'local address_Banaswadi', 'local address_Bannerghatta Road',
                           'local address_Brookefield', 'local address_Electronic City',
                           'local address_HSR', 'local address_Indiranagar',
                           'local address_Jayanagar', 'local address_Kaggadasapura',
                           'local address_Koramangala', 'local address_Koramangala 5th Block',
                           'local address_Koramangala 8th Block', 'local address_Malleshwaram',
                           'local address_Nagawara', 'local address_Residency Road',
                           'local address_Sahakara Nagar', 'local address_Seshadripuram',
                           'local address_Whitefield', 'local address_Yeshwantpur'
                           # Add other one-hot encoded columns here
                           ]

        user_input_encoded = user_input_encoded.reindex(
            columns=one_hot_columns, fill_value=0)

        # Make prediction using the trained model
        prediction = model.predict(user_input_encoded)

        # Provide waste-reduction ideas based on the prediction (you can customize this part)
        waste_reduction_ideas = get_waste_reduction_ideas(prediction[0])

        return render_template('result.html', prediction=prediction[0], ideas=waste_reduction_ideas)

# Define a function to provide waste-reduction ideas based on predictions


def get_waste_reduction_ideas(prediction):
    # Implement your logic here based on the predicted class
    # For example, you can have predefined messages for each class
    if prediction == 0:
        return "Consider reducing portion sizes to minimize food waste."
    else:
        return "Encourage customers to take leftovers or implement a donation program for excess food."

# Set the secret key for the Flask application
app.secret_key = 'my_secret_key_123'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
