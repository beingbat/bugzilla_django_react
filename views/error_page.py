

def page_not_found(request, exception=None):
    return render(request, "errors/generic.html", {'title': "Page not found. 404", 'exception':exception})

def permission_denied(request, exception=None):
    return render(request, "errors/generic.html", {'title': "Permission Denied. 403", 'exception':exception})

def bad_request(request, exception=None):
    return render(request, "errors/generic.html", {'title': "Bad Request. 400", 'exception':exception})

def server_error(request, exception=None):
    return render(request, "errors/generic.html", {'title': "Server Error. 500", 'exception':exception})

