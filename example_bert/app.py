import multiprocessing as mp
from flask import Flask, request, jsonify
from bert_serving.client import ConcurrentBertClient
from service_streamer import ThreadedStreamer

app = Flask(__name__)
model = None
streamer = None


class BertModel:
    def __init__(self):
        self.bc = ConcurrentBertClient(max_concurrency=128)

    def predict(self, batch):
        batch_outputs = self.bc.encode(batch)
        return batch_outputs


@app.route("/naive", methods=["POST"])
def naive_predict():
    inputs = request.form.getlist("s")
    outputs = model.predict(inputs)
    return jsonify(list(outputs[0].astype(float)))


@app.route("/stream", methods=["POST"])
def stream_predict():
    inputs = request.form.getlist("s")
    outputs = streamer.predict(inputs)
    return jsonify(list(outputs[0].astype(float)))


if __name__ == '__main__':
    mp.freeze_support()
    mp.set_start_method("spawn", force=True)
    model = BertModel()
    streamer = ThreadedStreamer(model.predict, batch_size=64, max_latency=0.1)

    app.run(port=5000, debug=False)
