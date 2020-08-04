import flask
import aiogram
import json
from aiogram.utils import executor
import aiogram.types
from wakebot.processors import RuGeneral
from wakebot.processors.default import DefaultProcessor
from wakebot.processors.wake import WakeProcessor
from wakebot.adapters.data import MemoryDataAdapter
from wakebot.adapters.state import StateManager

app = flask.Flask(__name__)

bot = aiogram.bot.Bot("1371195308:AAH_7irqFywj5acLvGqpMwMdJUwH1jq-GIY")
dp = aiogram.Dispatcher(bot)

state_manager = StateManager(MemoryDataAdapter())
default_processor = DefaultProcessor(dp, RuGeneral)
wake_processor = WakeProcessor(dp, state_manager, RuGeneral)

@app.route("/form")
def hello():
    return flask.url_for('static', filename='form.html')

@app.route("/bot", methods=["POST"])
def post_bot():
    json_string = flask.request.data.decode("utf-8")
    result_json = json.loads(json_string)
    s = result_json.get("message")
    for update in result_json:
        print(update)
    # updates = [aiogram.types.Update(**update) for update in result_json]

    return json.dumps({"phone": "123"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
