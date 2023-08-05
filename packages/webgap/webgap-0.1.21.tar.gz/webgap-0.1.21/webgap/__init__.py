import uuid
import logging
import steov
import house

def canonicalize_header (name):
    return "-".join(map(str.capitalize, name.split("-")))

class Response:
    def __init__ (self, response):
        self.status = response.status_code
        self.message = response.reason
        self.headers = { canonicalize_header(k):v for k,v in response.headers.items() }
        self.body = response.content
        self._orig_response = response

    def __repr__ (self):
        return f"<webgap.Response [{self.status} {self.message}]>"

class RequestsWebGap:
    def __init__ (self, requests, session_factory=None, house=house.NoopHouse(), logger=None, censor={}):
        self._requests = requests
        self._session_factory = session_factory or self._requests.Session
        self._house = house
        self._logger = logger or logging.getLogger(__name__)
        self._censor = set(map(str.casefold, censor))

    def _log_call_request (self, id, request):
        self._logger.debug("call.request.start: %s", id)
        self._logger.debug("call.request.url: %s", request.url)
        self._logger.debug("call.request.method: %s", request.method)
        for k, v in request.headers.items():
            if k.casefold() in self._censor:
                v = "CENSORED"
            self._logger.debug("call.request.header.%s: %s", k, v)
        self._logger.debug("call.request.body.sha256: %s", self._house.persist(request.body))
        self._logger.debug("call.request.finish: %s", id)

    def _log_call_error (self, id, exception, stacktrace):
        self._logger.debug("call.error.start: %s", id)
        for k, v in getattr(exception, "__dict__", {}).items():
            self._logger.debug("call.error.exception.%s: %r", k, v)
        for line in stacktrace.splitlines(keepends=False):
            self._logger.debug("call.error.stacktrace.line: %s", line)
        self._logger.debug("call.error.finish: %s", id)

    def _log_call_response (self, id, response):
        self._logger.debug("call.response.start: %s", id)
        self._logger.debug("call.response.status: %s", response.status_code)
        self._logger.debug("call.response.message: %s", response.reason)
        for k, v in response.headers.items():
            self._logger.debug("call.response.header.%s: %s", k, v)
        self._logger.debug("call.response.body.sha256: %s", self._house.persist(response.content))
        self._logger.debug("call.response.elapsed: %s", response.elapsed.total_seconds())
        self._logger.debug("call.response.finish: %s", id)

    def call (self, url, method="GET", headers={}, body=None, timeout=None, verify=True):
        call_id = uuid.uuid4()
        self._logger.debug("call.start: %s", call_id)
        try:
            timeout_sec = None if timeout is None else timeout.total_seconds()
            self._logger.debug("call.timeout: %s", timeout_sec)
            self._logger.debug("call.verify: %s", verify)
            request = self._requests.Request(url=url, method=method, headers=headers, data=body)
            with self._session_factory() as session:
                prepared_request = session.prepare_request(request)
                self._log_call_request(call_id, prepared_request)
                try:
                    response = session.send(prepared_request, timeout=timeout_sec, verify=verify)
                except Exception as ex:
                    # TODO sometimes `ex` can hold a response object. log it?
                    self._log_call_error(call_id, ex, steov.format_exc())
                    raise
                for i, historical_response in enumerate([*response.history, response]):
                    if i > 0:
                        self._log_call_request(call_id, historical_response.request)
                    self._log_call_response(call_id, historical_response)
                return Response(response)
        finally:
            self._logger.debug("call.finish: %s", call_id)
