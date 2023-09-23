import json

from flask import Flask, redirect
from flask import request, jsonify
from Code import connect
app = Flask(__name__)

# Connect to MongoDB
client = connect.main() # Returns the connection from connect File
db = client["database"]  # connect to a MongoDB database
netflix_collection = db["netflix"] # connect a MongoDB collection for movies and shows


@app.route('/')
def hello_world():  # Default url redirecting to /netflix
    return redirect('/netflix')


# 1. Insert a new movie or show
@app.route('/netflix', methods=['POST'])
def insert_movie_or_show():
    data = request.get_json()
    result = netflix_collection.insert_one(data)
    return jsonify({"message": "Movie/Show added successfully", "id": str(result.inserted_id)}), 201

# 2. Update movie or show information by title
@app.route('/netflix/<string:title>', methods=['PATCH'])
def update_movie_or_show(title):
    data = request.get_json()
    result = netflix_collection.update_one({"title": title}, {"$set": data})
    if result.modified_count > 0:
        return jsonify({"message": "Movie/Show updated successfully"})
    else:
        return jsonify({"message": "Movie/Show not found"}), 404

# 3. Delete a movie or show by title
@app.route('/netflix/<string:title>', methods=['DELETE'])
def delete_movie_or_show(title):
    result = netflix_collection.delete_one({"title": title})
    if result.deleted_count > 0:
        return jsonify({"message": "Movie/Show deleted successfully"})
    else:
        return jsonify({"message": "Movie/Show not found"}), 404

# 4. Retrieve all movies and shows in the database
@app.route('/netflix', methods=['GET'])
def get_all_movies_and_shows():
    data = list(netflix_collection.find())
    return json.dumps(data,default=str)

# 5. Display movie or show details by title
@app.route('/netflix/<string:title>', methods=['GET'])
def get_movie_or_show(title):
    data = netflix_collection.find_one({"title": title})
    if data:
        return json.dumps(data,default=str)
    else:
        return jsonify({"message": "Movie/Show not found"}), 404

if __name__ == '__main__':
    app.run()
