from gevent import monkey; monkey.patch_all()


bind = '0.0.0.0:5000'
workers = 4
worker_class = 'gunicorn.workers.ggevent.GeventWorker'
time_out = 600
