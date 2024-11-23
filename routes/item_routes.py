from flask import Blueprint, render_template, session, redirect, url_for, flash, jsonify, request
from services.verification import is_visible
from services.file_service import load_settings, save_settings
from services.lists_service import get_available_spouses, get_all_users, get_all_items
from services.item_functions.item_service import reserve_item, delete_item, edit_item, unreserve_item, toggle_buy_item, create_item
from services.file_service import load_item_file
from settings.tokens import *

item_blueprint = Blueprint("item", __name__, template_folder="templates")


@item_blueprint.route("/remove/<int:item_id>", methods=["POST"])
def remove_item_route(item_id):
    try:
        check = delete_item(item_id)
        if check:
            return jsonify({"success": True, "message": f"Item {item_id} removed successfully."})
        else:
            return jsonify({"success": False, "message": f"Unable to delete item {item_id}"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@item_blueprint.route("/reserve/<int:user_id>/<int:item_id>", methods=["POST"])
def reserve_item_route(user_id, item_id):
    try:
        reserved_item = reserve_item(user_id, item_id)
        if reserved_item:
            return jsonify({
                "success": True,
                "owner_id" : reserved_item[OWNER_ID],
                "item": {
                    "item_name": reserved_item["item_name"],
                    "item_description": reserved_item["item_description"],
                },
                "message": "Item reserved successfully."
            })
        else:
            return jsonify({"success": False, "message": "Failed to reserve item."}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@item_blueprint.route("/unreserve/<int:item_id>", methods=["POST"])
def unreserve_item_route(item_id):
    try:
        user_id = load_item_file(item_id)[RESERVED_BY]

        unreserved_item = unreserve_item(item_id)
        if unreserved_item:
            return jsonify({
                "success": True,
                "user_id": user_id,
                "item": {
                    "item_name": unreserved_item["item_name"],
                    "item_description": unreserved_item["item_description"],
                },
                "message": "Item unreserved successfully."
            })
        else:
            return jsonify({"success": False, "message": "Failed to unreserve item."}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500



@item_blueprint.route("/edit/<int:item_id>", methods=["POST"])
def edit_item_route(item_id):
    """Route to handle item editing."""
    try:
        data = request.get_json()
        new_name = data.get("new_name")
        new_description = data.get("new_description")

        if not new_name or not new_description:
            return jsonify({"success": False, "message": "Name and description are required."}), 400

        success = edit_item(item_id, new_name=new_name, new_description=new_description)
        if success:
            return jsonify({"success": True, "message": "Item updated successfully."})
        else:
            return jsonify({"success": False, "message": "Failed to update item."}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@item_blueprint.route("/toggle_buy/<int:item_id>", methods=["POST"])
def toggle_buy_route(item_id):
    try:
        new_status = toggle_buy_item(item_id)
        return jsonify({"success": True, "bought": new_status, "message": "Item status toggled successfully."})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@item_blueprint.route("/add", methods=["POST"])
def add_item_route():
    try:
        data = request.get_json()
        item_name = data.get("item_name")
        item_description = data.get("item_description", "")
        owner_id = data.get("owner_id")

        if not item_name or not owner_id:
            return jsonify({"success": False, "error": "Missing item name or owner ID."}), 400

        item = create_item(owner_id, {ITEM_NAME: item_name, ITEM_DESCRIPTION: item_description})
        print("finished creating new item")
        return jsonify({"success": True, "item": item})
    except Exception as e:
        print(f"Error adding item: {e}")
        return jsonify({"success": False, "error": str(e)}), 500