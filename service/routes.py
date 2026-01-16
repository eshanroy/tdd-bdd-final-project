"""
Product Store Service Routes

Implements REST API endpoints for Product resources.
"""

from flask import jsonify, request, abort, url_for
from service.models import Product, Category
from service.common import status
from . import app


######################################################################
# HEALTH
######################################################################
@app.route("/health")
def healthcheck():
    """Health check endpoint"""
    return jsonify(status=200, message="OK"), status.HTTP_200_OK


######################################################################
# HOME
######################################################################
@app.route("/")
def index():
    """Root endpoint"""
    return app.send_static_file("index.html")


######################################################################
# UTILITY
######################################################################
def check_content_type(content_type):
    """Verify request Content-Type"""
    if "Content-Type" not in request.headers:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    if request.headers["Content-Type"] != content_type:
        abort(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


######################################################################
# CREATE
######################################################################
@app.route("/products", methods=["POST"])
def create_products():
    """Create a Product"""
    check_content_type("application/json")
    data = request.get_json()

    product = Product()
    product.deserialize(data)
    product.create()

    location_url = url_for("get_product", product_id=product.id, _external=True)
    return jsonify(product.serialize()), status.HTTP_201_CREATED, {
        "Location": location_url
    }


######################################################################
# READ
######################################################################
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """Read a Product"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND)

    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE
######################################################################
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    """Update a Product"""
    check_content_type("application/json")

    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND)

    product.deserialize(request.get_json())
    product.id = product_id
    product.update()

    return jsonify(product.serialize()), status.HTTP_200_OK


######################################################################
# DELETE
######################################################################
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a Product"""
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND)

    product.delete()
    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIST + FILTERS
######################################################################
@app.route("/products", methods=["GET"])
def list_products():
    """List Products with optional filters"""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        products = Product.find_by_category(Category[category])
    elif available:
        products = Product.find_by_availability(available.lower() == "true")
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK
