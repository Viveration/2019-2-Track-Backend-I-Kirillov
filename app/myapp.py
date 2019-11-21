import datetime


def handler(environ, start_response):
    data = str(datetime.datetime.now()).encode('utf-8')
    headers = [('Content-Type', 'text/plain'),
                ('Content-Length', str(len(data)))]
    start_response('200 OK', headers)
    return [data]
