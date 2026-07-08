from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)


@api_bp.route("/hello", methods=["GET"])
def hello_world():
    """
    A simple endpoint that returns a greeting message.
    """
    return jsonify(message="Hello from your Flask API!")


# You can add more endpoints here
# @api_bp.route('/data', methods=['POST'])
# def post_data():
#     # Handle POST request
#     pass
