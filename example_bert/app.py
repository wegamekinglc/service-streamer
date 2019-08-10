# from gevent import monkey; monkey.patch_all()
# import multiprocessing as mp

# mp.freeze_support()
# mp.set_start_method("spawn", force=True)

import numpy as np
from flask import Flask, request, jsonify
from bert_serving.client import ConcurrentBertClient
from service_streamer import ThreadedStreamer

app = Flask(__name__)


class BertModel:
    def __init__(self):
        # self.bc = ConcurrentBertClient(max_concurrency=128)
        pass

    def predict(self, batch):
        # batch_outputs = self.bc.encode(batch)
        # return batch_outputs
        return np.array([[1.0, 0.0]])


model = BertModel()
streamer = ThreadedStreamer(model.predict, batch_size=256, max_latency=0.1)


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
    app.run(host="0.0.0.0", port=5000, debug=False)
    #from gevent.pywsgi import WSGIServer
    # server = WSGIServer(("0.0.0.0", 5000), app).serve_forever()