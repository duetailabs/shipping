from flask import Flask, jsonify, abort, request
import requests, time
from data_model import Package
from connect_connector import SessionMaker

app = Flask(__name__)

# Create Acme Corp standard backend routes
# Acme Corp discovery backend route
@app.route('/discovery', methods=['GET'])
def discovery():
    return jsonify({
        "name": "shipping",
        "version": "1.0",
        "owners": ["ameerabb", "lonestar"],
        "team": "genAIs",
        "organization": "acme"
    })

# Acme Corp liveness backend route
@app.route('/liveness', methods=['GET'])
def liveness():
    return jsonify({"status": "live", "code": 200, "timestamp": time.time()})

# Acme Corp readiness backend route
@app.route('/readiness', methods=['GET'])
def readiness():
    return jsonify({"status": "ready", "code": 200, "timestamp": time.time()})
# End of Acme Corp standard backend routes

# function that returns the name and version of the app
def get_app_details():
    """Fetches app details from the /discovery endpoint."""
    try:
        response = requests.get('http://localhost:8000/discovery')  # Adjust URL if needed
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data.get('name', 'Unknown App'), data.get('version', 'Unknown Version')
    except requests.exceptions.RequestException as e:
        print(f"Error fetching app details: {e}")
        return "Unknown App", "Unknown Version"

# get a package from CloudSQL database
# Endpoint that retrieves package details based on the provided product ID
@app.route('/packages/<int:product_id>', methods=['GET'])
def acme_corp123_retrieve_package_by_product_id(product_id):
    """
    Get information about a package.
    This endpoint retrieves package details based on the provided product ID.
    :param product_id: The ID of the product.
    :return: JSON response containing package information or 404 if not found.
    """
    session = SessionMaker()
    package = session.query(Package).filter(Package.product_id == str(product_id)).first()
    session.close()

    if package:
        return jsonify({
            "height": package.height,
            "width": package.width,
            "depth": package.depth,
            "weight": package.weight,
            "special_handling_instructions": package.special_handling_instructions
        })
    else:
        app_name, app_version = get_app_details()
        abort(404, description={
            "message": "The product_id was not found",
            "timestamp": time.time(),
            "app_name": app_name,
            "version": app_version,
            "called_method": "get_package",
            "product_id": product_id
        })

# create a new package in the CloudSQL database
# Endpoint that creates a new package in the database.
@app.route('/packages', methods=['POST'])
def acme_corp123_create_new_package():
    data = request.get_json()
    if not data:
        abort(400, description="Missing JSON data in request body")
    try:
        product_id = data['product_id']
        height = data['height']
        width = data['width']
        depth = data['depth']
        weight = data['weight']
        special_handling_instructions = data.get('special_handling_instructions')
        session = SessionMaker()
        new_package = Package(
            product_id=product_id,
            height=height,
            width=width,
            depth=depth,
            weight=weight,
            special_handling_instructions=special_handling_instructions
        )
        session.add(new_package)
        session.commit()

        return jsonify({"package_id": new_package.id}), 201
    except KeyError as e:
        abort(400, description=f"Missing required field: {e}")
    except ValueError as e:
        abort(400, description=f"Invalid data: {e}")

# update an existing package in the CloudSQL database
# Endpoint that updates an existing package in the database.
@app.route('/packages/<int:package_id>', methods=['PUT'])
def acme_corp123_update_existing_package_by_id(package_id):
    """
    Update an existing package in the database.
    This endpoint allows updating the details of an existing package.
    :param package_id: The ID of the package to update.
    :return: JSON response with updated package information or 404 if not found.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Missing JSON data in request body")

    session = SessionMaker()
    package = session.query(Package).filter(Package.id == package_id).first()
    session.close()

    if package:
        try:
            package.height = data.get('height', package.height)
            package.width = data.get('width', package.width)
            package.depth = data.get('depth', package.depth)
            package.weight = data.get('weight', package.weight)
            package.special_handling_instructions = data.get('special_handling_instructions', package.special_handling_instructions)

            session = session_maker
            session.commit()
            session.close()

            return jsonify({
                "height": package.height,
                "width": package.width,
                "depth": package.depth,
                "weight": package.weight,
                "special_handling_instructions": package.special_handling_instructions
            })
        except KeyError as e:
            abort(400, description=f"Missing required field: {e}")
        except ValueError as e:
            abort(400, description=f"Invalid data: {e}")
    else:
        abort(404, description="The package_id was not found")

# delete a package in the CloudSQL database
# Endpoint that deletes an existing package from the database.
@app.route('/packages/<int:package_id>', methods=['DELETE'])
def acme_corp123_delete_package_by_id(package_id):
    session = SessionMaker()
    package = session.query(Package).filter(Package.id == package_id).first()
    session.close()

    if package:
        session = session_maker
        session.delete(package)
        session.commit()
        session.close()

        return '', 204
    else:
        abort(404, description="The package_id was not found")


# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
