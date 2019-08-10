from gevent import monkey; monkey.patch_all()
from flask import Flask, request, jsonify
from bert_serving.client import ConcurrentBertClient
from service_streamer import RedisStreamer


app = Flask(__name__)


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

model = BertModel()
streamer = RedisStreamer()

if __name__ == '__main__':
    pass
    
    # app.run(host="0.0.0.0", port=5000, debug=False)

    # from gevent.pywsgi import WSGIServer
    # WSGIServer(("0.0.0.0", 5000), app).serve_forever()
