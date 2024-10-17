from flask import Flask, jsonify, abort, request

from data_model import Package
from connect_connector import SessionMaker

app = Flask(__name__)

session_maker = SessionMaker()

# standard http handlers
@app.route('/discovery', methods=['GET'])
def discovery():
    return jsonify({
        "name": "shipping",
        "version": "1.0",
        "owners": ["ameerabbas", "janedoe"],
        "organization": "acme"
    })

# create a /liveness and /readiness endpoints that return status, code and timestamps
@app.route('/liveness', methods=['GET'])
def liveness():
    return jsonify({"status": "live", "code": 200, "timestamp": "2023-04-27T12:00:00Z"})

@app.route('/readiness', methods=['GET'])
def readiness():
    return jsonify({"status": "ready", "code": 200, "timestamp": "2023-04-27T12:00:00Z"})
# End of standard http handlers

# get a package from CloudSQL database
# Endpoint that retrieves package details based on the provided product ID
@app.route('/packages/<int:product_id>', methods=['GET'])
def get_package(product_id):
    """
    Get information about a package.

    This endpoint retrieves package details based on the provided product ID.

    :param product_id: The ID of the product.
    :return: JSON response containing package information or 404 if not found.
    """
    session = session_maker
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
        abort(404, description="The product_id was not found")

# create a new package in the CloudSQL database
# Endpoint that creates a new package in the database.
@app.route('/packages', methods=['POST'])
def create_package():
    """
    Create a new package in the database.

    This endpoint allows creating a new package with specified details.

    :return: JSON response with the created package ID or 400 if invalid data.
    """
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

        session = session_maker
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
def update_package(package_id):
    """
    Update an existing package in the database.

    This endpoint allows updating the details of an existing package.

    :param package_id: The ID of the package to update.
    :return: JSON response with updated package information or 404 if not found.
    """
    data = request.get_json()
    if not data:
        abort(400, description="Missing JSON data in request body")

    session = session_maker
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
def delete_package(package_id):
    """
    Delete an existing package from the database.

    This endpoint allows deleting a package based on its ID.

    :param package_id: The ID of the package to delete.
    :return: 204 (No Content) if successful, 404 if not found.
    """
    session = session_maker
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
