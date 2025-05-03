from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/balance', methods=['GET'])
def get_balance():
    return jsonify({"balance": 2450.75})

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, request, jsonify
# from flask_cors import CORS, cross_origin

# app = Flask(__name__)
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

# # @app.route('/extract_embedding', methods=['POST'])
# # def extract_embedding():
# #     # Get the image file from the request
# #     image_file = request.files['image']
# #     # Extract features from the image
# #     feature_vector = extract_features(image_file)
# #     # Convert the feature vector to a list for JSON serialization
# #     feature_list = feature_vector.tolist()
# #     # Return the feature vector as JSON
# #     return jsonify({'embedding': feature_list})
# #     #feature_string = base64.b64encode(feature_vector.tobytes()).decode('utf-8')
# #     # Return the feature vector as a string
# #     #return jsonify({'embedding': feature_string})

# @app.route('/hello/<fishe>', methods=['GET'])
# @cross_origin()
# def hello(fishe):
#     return f"Hello fishe, {fishe}!"
#     # return jsonify({'products': similar_ids})


# if __name__ == '__main__':
#     app.run(debug=True)