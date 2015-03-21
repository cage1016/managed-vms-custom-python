Managed vms custom runtime
==========================

####Developing code for custom runtimes

[Building Custom Runtimes - Google App Engine — Google Cloud Platform](https://cloud.google.com/appengine/docs/managed-vms/custom-runtimes)

There are few notice mentioned in offical documentation you have to manual setup if you want to use custom managed vms runtime. 1) listen to part 8080 2) start and stop requests 3) health requests check.

the following demo is a simple go througth to show how to build a custom managed vms runtime.

#####standard VM runtimes
######app.yaml
```yaml
application: <your application id>
module: <your module name>
version: 1
runtime: python27
api_version: 1
threadsafe: yes
vm: true

...
```

When you use `gcloud` to run or deploy a managed VM application based on a standard runtime (in this case Python27), the SDK will create a minimal Dockerfile using the standard runtime as a base image. You'll find this `Dockerfile` in your project directory:

######Dockerfile
```dockerfile
# Dockerfile extending the generic Python image with application files for a
# single application.
FROM google/appengine-python27

ADD . /app
```

#####custom VM runtimes:app.yaml

To create a custom VM runtime application, you have to modify `app.yaml` configuration file with following settings:

######app.yaml
```yaml
runtime: custom
vm: true
```

You can reuse `Dockerfile` that SDK created for you or create your new one. Here, we will use `google/python` base image and extend custom VM runtimes Dockerfile


######Dockerfile
```dockerfile
FROM google/python

RUN apt-get update && apt-get install -y -q --no-install-recommends

WORKDIR /app
RUN virtualenv /env

ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN /env/bin/pip install -r requirements.txt

# Adds the rest of the application source
ADD . /app

ENTRYPOINT ["/env/bin/python", "/app/main.py"]
```
######requirements.txt
```text
WebOb
Paste
webapp2
```

As mentioned before. we have to listen port 8080 and manual setup `start`, `stop` and `health` requests in main.py file

######main.py
```python
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
```


####Reference

- [Managed VMs - Google App Engine — Google Cloud Platform](https://cloud.google.com/appengine/docs/managed-vms/)
- [Quick start (to use webapp2 outside of App Engine) — webapp2 v2.5.1 documentation](https://webapp-improved.appspot.com/tutorials/quickstart.nogae.html)

