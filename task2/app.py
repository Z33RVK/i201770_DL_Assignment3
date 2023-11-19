from flask import Flask, render_template, request

app = Flask(__name__)

# Simple function to predict a product based on user input (Replace this with your actual prediction logic)
def predict_product(query):
    # Replace this logic with your machine learning model or prediction function
    products = {
        "revent 80 cfm": "homewerks bathroom fan ceiling mount exhaust ventilation sone cfm white",
        "lawnmower tires without rims": "zippity outdoor product zp premium vinyl privacy screen w x h unassembled white",
        "revent 80 cfm ": "delta electronics radl breezradiance cfm heaterfanlight combo white renewed preowned refurbished product professionally inspected tested work look like new product becomes part amazon renewed destination preowned refurbished product customer buy new product return trade newer different model product inspected tested work look like new amazonqualified supplier product sold amazon renewed product amazon satisfied purchase renewed product eligible replacement refund amazon renewed guarantee"
    }

    if query.lower() in products:
        return products[query.lower()]
    else:
        return "Product not found"

@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_product = None
    if request.method == 'POST':
        user_query = request.form['query']
        predicted_product = predict_product(user_query)

    return render_template('index.html', predicted_product=predicted_product)

if __name__ == '__main__':
    app.run(debug=True)
