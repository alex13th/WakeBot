import flask
import telebot
import json


app = flask.Flask(__name__)


@app.route("/form")
def hello():
    return flask.url_for('static', filename='form.html')


@app.route("/bot", methods=["POST"])
def post_bot():
    json_string = flask.request.data.decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    return json.dumps({"phone": update.message.contact.phone_number})


if __name__ == "__main__":
    app.run(host='0.0.0.0')
