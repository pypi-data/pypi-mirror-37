import base64
import json
import logging
import sys

import requests

from org.openbaton.cli.errors.errors import WrongCredential, NfvoException

logger = logging.getLogger("org.openbaton.cli.RestClient")
WRONG_STATUS = [500, 400, 404, 405, 422]


def _expired_token(content):
    if content is not None:
        if "error" in content:
            try:
                return json.loads(content).get("error") is not None and json.loads(content).get(
                    "error") == "invalid_token"
            except AttributeError:
                return False
    return False


def get_content_type(body):
    if not body or isinstance(body, dict) or (
                isinstance(body, str) and (body.startswith('{') or body.endswith('{'))):
        return "application/json"
    return "text/plain"


class RestClient(object):
    def __init__(self, nfvo_ip="localhost", nfvo_port="8080", https=False, version=1, username=None, password=None,
                 project_id=None):

        if https:
            self.base_url = "https://%s:%s/" % (nfvo_ip, nfvo_port)
        else:
            self.base_url = "http://%s:%s/" % (nfvo_ip, nfvo_port)

        self.ob_url = "%sapi/v%s/" % (self.base_url, version)

        self.project_id = project_id
        self.token = None
        self.username = username
        self.password = password
        # print "user %s" % username

    def get(self, url):
        if self.token is None:
            self.token = self._get_token()
        headers = {
            "Authorization": "Bearer %s" % self.token,
            "accept": "application/json",
        }
        if self.project_id is not None:
            headers["project-id"] = self.project_id
        final_url = self.ob_url + url
        logger.debug("executing get on url %s, with headers: %s" % (final_url, headers))
        response = requests.get(final_url, headers=headers, verify=False)
        result = response.text
        # logger.debug(response.text)
        if _expired_token(result):
            self.token = self._get_token()
            self.get(url)
        if result == "":
            result = '{"error":"Not found"}'
        self.check_answer(response)
        return result

    def post(self, url, body, headers=None):
        if self.token is None:
            self.token = self._get_token()
        if headers is None:
            headers = {
                "content-type": get_content_type(body),
                # "accept": "application/json"
            }
        if self.project_id is not None:
            headers["project-id"] = self.project_id

        headers["Authorization"] = "Bearer %s" % self.token
        logger.debug("executing POST on url %s, with headers: %s" % (self.ob_url + url, headers))
        logger.debug("With body: %s" % body)
        response = requests.post(self.ob_url + url, data=body, headers=headers, verify=False)

        if _expired_token(response.text):
            self.token = self._get_token()
            self.post(url, body, headers=headers)
        self.check_answer(response)
        return response.text

    def post_file(self, url, _file, headers=None):
        if self.token is None:
            self.token = self._get_token()
        if headers is None:
            headers = {
                "Authorization": "Bearer %s" % self.token,
                # "accept": "application/json",
                "project-id": self.project_id
            }
        files = {'file': ('file', _file, "multipart/form-data")}

        ses = requests.session()
        logger.debug("executing POST on url %s, with headers: %s" % (self.ob_url + url, headers))
        response = ses.post(self.ob_url + url, files=files, headers=headers, verify=False)
        self.check_answer(response)
        return response.text

    def put(self, url, body, headers=None):
        if self.token is None:
            self.token = self._get_token()
        if headers is None:
            headers = {"content-type": get_content_type(body)}
        if self.project_id is not None:
            headers["project-id"] = self.project_id
        headers["Authorization"] = "Bearer %s" % self.token
        logger.debug("executing PUT on url %s, with headers: %s" % (self.ob_url + url, headers))
        response = requests.put(self.ob_url + url, data=body, headers=headers, verify=False)
        if _expired_token(response.text):
            self.token = self._get_token()
            self.put(url, body=body, headers=headers)
        self.check_answer(response)
        return response.text

    def put_file(self, url, body, headers=None):
        if self.token is None:
            self.token = self._get_token()
        if headers is None:
            headers = {"content-type": "text/plain"}
        if self.project_id is not None:
            headers["project-id"] = self.project_id
        headers["Authorization"] = "Bearer %s" % self.token
        logger.debug("executing PUT on url %s, with headers: %s" % (self.ob_url + url, headers))
        response = requests.put(self.ob_url + url, data=body, headers=headers, verify=False)
        if _expired_token(response.text):
            self.token = self._get_token()
            self.put(url, body=body, headers=headers)
        self.check_answer(response)
        return response.text

    def delete(self, url):
        if self.token is None:
            self.token = self._get_token()
        headers = {}
        if self.project_id is not None:
            headers = {"project-id": self.project_id}
        headers["Authorization"] = "Bearer %s" % self.token
        logger.debug("executing DELETE on url %s, with headers: %s" % (self.ob_url + url, headers))
        content = requests.delete(self.ob_url + url, headers=headers, verify=False)
        if _expired_token(content):
            self.token = self._get_token()
            self.delete(url)
        self.check_answer(content)
        return content

    def _get_token(self):
        # logger.debug("Executing post: %s" % (self.base_url + "oauth/token"))
        if sys.version_info > (2, 7):  # python 3.X
            h = {
                "Authorization": "Basic %s" % base64.b64encode(b"openbatonOSClient:secret").decode("utf-8"),
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        else:  # python 2.7
            h = {
                "Authorization": "Basic %s" % base64.b64encode("openbatonOSClient:secret"),
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        # logger.debug("Headers are: %s" % h)
        response = requests.post(self.base_url + "oauth/token",
                                 headers=h,
                                 data="username=%s&password=%s&grant_type=password" % (
                                     self.username, self.password), verify=False)
        # logger.debug(response.text)
        res_dict = json.loads(response.text)
        token = res_dict.get("value") or res_dict.get("access_token")
        logger.debug("Got token %s" % token)
        if token is None:
            if res_dict.get("detailMessage") is not None:
                raise WrongCredential("Invalid credential!")
        return token

    def check_answer(self, result):
        logger.debug("Response status is: %s" % result.status_code)
        logger.debug("Reason: %s" % result.reason)
        content = None
        if result.status_code in WRONG_STATUS:
            message = None
            try:
                content = result.content
                try:
                    content = content.decode('utf-8')
                except:
                    pass
                content = json.loads(content)
                logger.debug("Content is: \n\n%s" % json.dumps(content, indent=2))
                message = content.get('message') or content

            except:
                logger.warning("Not able to parse json")
                logger.debug("Content is: \n\n%s" % content)
            raise NfvoException(message or content or result.reason)
