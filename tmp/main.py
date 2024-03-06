from flask import Flask, request, jsonify

from data_model import Package
from connect_connector import SessionMaker

app = Flask(__name__)

session_maker = SessionMaker()

@app.route("/packages/<int:product_id>", methods=["GET"])
def get_package(product_id):
  """Get information about a package."""

  session = session_maker

  package = session.query(Package).filter(Package.product_id == product_id).first()

  if package is None:
    return jsonify({"message": "Package not found."}), 404

  return jsonify(
      {
          "height": package.height,
          "width": package.width,
          "depth": package.depth,
          "weight": package.weight,
          "special_handling_instructions": package.special_handling_instructions,
      }
  ), 200

if __name__ == "__main__":
  app.run(host="0.0.0.0")

