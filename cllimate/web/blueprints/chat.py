from flask import Blueprint

blueprint = Blueprint("chat", __name__)


@blueprint.route("/chat")
def chat():
    return "Hello!"
