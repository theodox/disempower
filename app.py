from server import route, serve


@route("/test")
def test(request):
    result = []
    result.append("got request")
    result.append("url: {}".format(request['url']))
    result.append("query: {}".format(request.get('query', "")))

    return "<br>".join(result)


serve()
