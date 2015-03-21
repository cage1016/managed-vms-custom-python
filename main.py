import webapp2


class HomeHandler(webapp2.RequestHandler):

    def get(self):
        self.response.out.write('work')


class HealthCheckHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('ok')


routes = [
    (r'/_ah/health', HealthCheckHandler),
    (r'/_ah/stop', HealthCheckHandler),
    (r'/_ah/start', HealthCheckHandler),
    (r'/.*', HomeHandler)
]

app = webapp2.WSGIApplication(routes,
                              debug=True)


def main():
    from paste import httpserver

    httpserver.serve(app, host='0.0.0.0', port='8080', start_loop=True)


if __name__ == '__main__':
    main()
