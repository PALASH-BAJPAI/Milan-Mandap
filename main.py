from flask import Flask, request, jsonify
from database import db
from models import User
from schemas import is_valid_email
from city_to_state import city_to_state

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#Database initialization
with app.app_context():
    db.create_all()

# Site Entry point
@app.route('/')
def hello_users():
    return "<h1>Namaste 🙏</h1> <br/> <h2> Welcome to Milan Mandap </h2>"

# user end point
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    if not is_valid_email(data.get('email')):
        return jsonify({"error": "Invalid email address"}), 400

    new_user = User(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        email=data['email'],
        city=data['city'],
        interests=data['interests']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# Fetch all users endpoint
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'age': user.age,
        'gender': user.gender,
        'email': user.email,
        'city': user.city,
        'interests': user.interests
    } for user in users])


# Read User by ID Endpoint
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found in database"}), 404
    return jsonify({
        'id': user.id,
        'name': user.name,
        'age': user.age,
        'gender': user.gender,
        'email': user.email,
        'city': user.city,
        'interests': user.interests
    })

# Update User Endpoint
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if data.get('email') and not is_valid_email(data['email']):
        return jsonify({"error": "Invalid email address"}), 400

    user.name = data.get('name', user.name)
    user.age = data.get('age', user.age)
    user.gender = data.get('gender', user.gender)
    user.email = data.get('email', user.email)
    user.city = data.get('city', user.city)
    user.interests = data.get('interests', user.interests)

    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# Delete User Endpoint
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

#get state from city using dictionary
def get_state(city):
    if city in city_to_state.keys():
        return city_to_state[city]

# Find Matches Endpoint
@app.route('/users/<int:user_id>/matches', methods=['GET'])
def find_matches(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Fetch the state of the user's city
    user_state = "get_state(user.city)"

    # Match opposite gender only
    matches = User.query.filter(
        User.id != user.id,  
        User.gender != user.gender 
    ).all()

    #Can change priority given based on filters applied by users
    # Priority based match ( out of 100)
    potential_matches = []
    for match in matches:
        priority = 10         #default prioirty for being different gender

        # Priority 1: Common interests
        if set(user.interests.split(",")).intersection(set(match.interests.split(","))):
            priority += 30

        # Priority 2: Same city or same state
        match_state = get_state(match.city)
        if user.city == match.city:
            priority += 20
        elif user_state and match_state and user_state == match_state:
            priority += 10

        # Priority 3: Age range (+-2 years)
        if abs(user.age - match.age) <= 2:
            priority += 30

        potential_matches.append({
            'priority': priority,
            'id': match.id,
            'name': match.name,
            'age': match.age,
            'gender': match.gender,
            'email': match.email,
            'city': match.city,
            'interests': match.interests
        })
    potential_matches.sort(key=lambda x: x['priority'], reverse=True)
    return jsonify(potential_matches)


if __name__ == '__main__':
    app.run(debug=True)
