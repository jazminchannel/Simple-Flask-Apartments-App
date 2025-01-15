from flask import Flask, jsonify, request, render_template, abort, json

app = Flask(__name__)

# Mock data
apartments = [
    {'id': '1', 'name': 'Jefferson Lumen', 'price': 2575},
    {'id': '2', 'name': 'Cortland at Las Colinas', 'price': 2486},
    {'id': '3', 'name': "Ivy Broadway", 'price': 2183},
]

# Helper function to find an apartment by ID
def find_apartment(apartment_id):
    return next((apartment for apartment in apartments if apartment['id'] == apartment_id), None)

# Root endpoint: Display apartments in a simple UI
@app.route('/')
def home():
    return render_template('index.html', apartments=apartments)

# Get all apartments (JSON)
@app.route('/apartments')
def apartments_index():
    response = app.response_class(
        response=json.dumps(apartments, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response

# Get a single apartment by ID (JSON)
@app.route('/apartments/<apartment_id>', methods=['GET'])
def get_apartment(apartment_id):
    apartment = find_apartment(apartment_id)
    if not apartment:
        abort(404, description="Apartment not found")
    return jsonify(apartment)

# Create a new apartment
@app.route('/apartments', methods=['POST'])
def create_apartment():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        abort(400, description="Invalid input: 'name' and 'price' are required")
    
    new_apartment = {
        'id': str(len(apartments) + 1),
        'name': data['name'],
        'price': int(data['price'])
    }
    apartments.append(new_apartment)
    return jsonify({'message': 'Apartment created successfully', 'apartment': new_apartment}), 201

# Update an existing apartment
@app.route('/apartments/<apartment_id>', methods=['PATCH'])
def update_apartment(apartment_id):
    apartment = find_apartment(apartment_id)
    if not apartment:
        abort(404, description="Apartment not found")
    
    updates = request.get_json()
    if not updates:
        abort(400, description="Invalid input: No data provided")
    
    apartment.update(updates)
    return jsonify({'message': 'Apartment updated successfully', 'apartment': apartment})

# Delete an apartment
@app.route('/apartments/<apartment_id>', methods=['DELETE'])
def delete_apartment(apartment_id):
    apartment = find_apartment(apartment_id)
    if not apartment:
        abort(404, description="Apartment not found")
    
    apartments.remove(apartment)
    return jsonify({'message': 'Apartment deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)

