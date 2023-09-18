# port8-task

## Instructions

- Use Django
- Use version control GIT (the more commits, the better) – submit your work and send us a
  link to your repo

## Main Task - Strangling the monolith

**Problem:** How to migrate a legacy monolithic application to a microservice architecture?

**Assignment:** Implement a simple proxy service with which we can effectively apply a strangler
pattern to solve our problems during migration.

The idea of the service is that we control the traffic and where it goes. The routing rules can be
based on URI endpoint, HTTP headers or JSON-RPC fields. Each individual rule can be provided
via JSON (or Jsonnet) and stored in Redis. For simplicity and saving time, it’s okay to load this
configuration from disk and store it in Redis. Feel free to pick the most convenient data structure
and serialization format for storage. If the additional rules are loaded to Redis, service should
balance the in-flight requests correctly and drain the traffic before applying new rules (i.e. all
requests up to the point when new rules are applied should be routed by old rules).

The service should be able to proxy all HTTP requests, including HTTP v1.1 and 2.x. The SSL
termination will happen before requests enter the service, so handling any SSL related issues can
be considered out of scope for this assignment.

Please, implement at least one unit and one integration test in your solution.

**Bonus points:**

- Use Redis to implement externally controllable limiter for throttle control (do not let more than
  1M RPS into the system)
- Provide endpoint for Prometheus based metrics
- Provide status endpoints for readiness and liveness probes
- Execute the app as one or more stateless processes
- Store configuration in the environment
- Add request logging in JSON format
- Correctly handle panics and redirect them to stderr
- Implement request draining strategy on process shutdown

## Run the solution

```commandline
docker build -t <image_name> .
docker-compose up --build
```

### Usage

Sending request to `localhost:8000/api/users/` should redirect to 'legacy' endpoint `reqres.in`.
Sending request to `localhost:8000/weblog/` should redirect to 'modern' endpoint `www.djangoproject.com`.
To add/update rules, send post request to `localhost:8000/add-rule/` with data

```json
{
  "key": "key1",
  "value": "MODERN"
}
```

To access Prometheus:

`http://localhost:9090/targets`

RPS limiter is set to 1,000,000 requests per second, if value need to be changed it can be done in file `rps_limiter.py`
by setting `max_rps` to desired value.