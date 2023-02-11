from flask import Flask

from .blueprints import chat

app = Flask(__name__)
app.register_blueprint(chat.blueprint)


@app.route("/status")
def status():
    return {"status": "ok"}
