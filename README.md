<div id="user-content-toc">
  <ul align="center" style="list-style: none;">
    <summary>
      <h1>Milan-Mandap</h1> <br/>
      <h3>Modern Matchmaking Rooted in Tradition</h3> 
    </summary>
  </ul>
</div>


Milan-Mandap is a modern matchmaking backend application tailored to the needs of Indian users. It blends the beauty of tradition with modern matchmaking algorithms, ensuring personalized connections based on interests, location, and preferences.

---

## **Features**

1. **User Management**:
   - Create, update, retrieve, and delete user profiles.
   - Store information such as name, age, gender, city, email, and interests.

2. **Smart Matchmaking**:
   - Matches users based on:
     - **Common Interests** (highest priority).
     - **Same City or State** (prioritized for Indian users).
     - **Age Compatibility** (matches within a range of ±2 years).
   - Finds potential matches with a priority-based algorithm.

3. **Geolocation Integration**:
   - Fetch the state of a user's city using the **Geopy** library (OpenStreetMap API).

4. **Organized Backend Architecture**:
   - Clean and modularized code with components like models, schemas, and database management.

5. **JSON APIs**:
   - Provides RESTful APIs for all features, including user management and matchmaking.

---

## **How to Install and Run Locally**

Follow these steps to set up the project and get it running locally:

Clone the Repository
```bash
git clone https://github.com/PALASH-BAJPAI/Milan-Mandap.git
cd Milan-Mandap
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python main.py
```

The backend server will start on http://127.0.0.1:5000.

---

## Matchmaking algorithm
The matchmaking algorithm uses priority-based sorting to find the best potential matches for a user:
- **Priority 1: Common Interests**  
  Matches users with overlapping interests (e.g., "Reading" and "Traveling").  
  **Weight:** 1000.

- **Priority 2: Same City or State**  
  Matches users in the same city or state for proximity.  
  **Weight:**
  - Same City: 500.
  - Same State: 300.

- **Priority 3: Age Compatibility**  
  Matches users with an age difference of ±2 years.  
  **Weight:** 200.

- **Fallback: No Match on Above Criteria**  
  Shows matches in the same country, even if the above conditions aren't met.
## Endpoints

Retrieve all users
```bash
GET /users
```

Create User

```bash
  POST /users
```
```json
{
    "name": "Anusha",
    "age": 25,
    "gender": "Female",
    "email": "anusha12@gmail.com",
    "city": "Mumbai",
    "interests": "Dance,Reading,Traveling,Music"
}
```

Retrieve user by id

```bash
  GET /users/<user_id>
```

Update user

```bash
  PUT /users/<user_id> 
```

Delete user

```bash
  DELETE /users/<user_id>
```

Find Potential matches

```bash
  GET /users/<user_id>/matches
```
# Tools and Libraries

- **Flask**: For building the backend API.  
- **Flask-SQLAlchemy**: ORM for database interaction.  
- **SQLite**: File-based database for lightweight storage.   
- **Python**: Core programming language for the backend logic.  

# Potential Improvements

- Add authentication and authorization to protect user data.  
- Introduce a frontend UI for easier interaction with the backend.  
- Expand geolocation features to support cities and states globally.  
- Implement a messaging feature for matched users.  
- Optimize matchmaking using machine learning algorithms.  
- Add more data about user to better find matches.
