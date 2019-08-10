from gevent import monkey; monkey.patch_all()

def post_fork(server, worker):
    from service_streamer import RedisStreamer
    import app
    app.streamer = RedisStreamer()

bind = '0.0.0.0:5000'
workers = 4
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
proc_name = "redis_streamer"
