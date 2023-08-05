from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response


def serve_example(content, host='localhost', port=8080):  # pragma: no cover
    @Request.application
    def application(request):
        return Response(str(content), mimetype='text/HTML')
    run_simple(host, port, application, use_reloader=True)