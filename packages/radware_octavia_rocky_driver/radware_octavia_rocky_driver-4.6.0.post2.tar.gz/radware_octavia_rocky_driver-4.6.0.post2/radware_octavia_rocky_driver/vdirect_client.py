import time
import json
import base64
import ssl
import platform
import sys
import os
import logging

ver = platform.python_version_tuple()
PY3 = int(ver[0]) >= 3
if PY3:
    import http.client as http
    import urllib.parse as urllib
else:
    import httplib as http
    import urllib


def _strict_status_codes(status_codes):
    sc = {}
    for key in status_codes.keys():
        if key not in sc.keys():
            sc[key] = []
        for code in status_codes[key]:
            if code / 100 not in [4, 5]:
                sc[key].append(code)
    return sc


def _non_strict_status_codes(status_codes):
    sc = {}
    for key in status_codes.keys():
        if key not in sc.keys():
            sc[key] = []
        for code in status_codes[key]:
           sc[key].append(code)
    return sc


STATUS_CODES = {
    'DELETE':[200,204,404,409],
    'GET':[200,400,404],
    'PUT':[200,204,400,404],
    'POST':[200,201,202,204, 400,404,409]
}

STRICT_STATUS_CODES = _strict_status_codes(STATUS_CODES)
NON_STRICT_STATUS_CODES = _non_strict_status_codes(STATUS_CODES)


RESP_STATUS = 0
RESP_REASON = 1
RESP_STR = 2
RESP_DATA = 3
RESP_CONTENT_TYPE = 4

_MOVED_PERMANENTLY = 301
_TEMPORARY_REDIRECT = 307
_REDIRECT_CODES = [_MOVED_PERMANENTLY,_TEMPORARY_REDIRECT]


class RestClientException(Exception):
    def __init__(self, status_code, failure_reason, http_verb, expected_codes = [], failure_msg = None, requested_url = None):
        self.status_code = status_code
        self.failure_reason = failure_reason
        self.http_verb = http_verb
        self.expected_codes = expected_codes
        self.failure_msg = failure_msg
        self.requested_url = requested_url
        try:
            if failure_msg:
                self.message = "Operation failed: " + json.loads(failure_msg)['message']
            else:
                self.message = "Operation failed: No failure message available"
        except Exception as e:
            self.message = "Operation failed (during RestClientException exception creation): " + str(e)

    def __str__(self):
        return '{}. Status code: {}. Expected codes: {}. HTTP verb: {}. Failure msg: {}. Requested url: {} '.\
            format(self.failure_reason, self.status_code,
                   self.expected_codes, self.http_verb,
                   self.failure_msg, self.requested_url)


class BadRequestException(RestClientException):
    def __init__(self, resource, failure_reason='', http_verb='GET'):
        super(BadRequestException, self).__init__(400, failure_reason, http_verb, requested_url=resource)


class UnauthorizedException(RestClientException):
    def __init__(self, resource, failure_reason='', http_verb='GET'):
        super(UnauthorizedException, self).__init__(401, failure_reason, http_verb, requested_url=resource)


class ForbiddenException(RestClientException):
    def __init__(self, resource,failure_reason='', http_verb='GET'):
        super(ForbiddenException, self).__init__(403, failure_reason, http_verb, requested_url=resource)


class NotFoundException(RestClientException):
    def __init__(self, resource, failure_reason='', http_verb='GET'):
        super(NotFoundException, self).__init__(404, failure_reason, http_verb, requested_url=resource)


class MethodNotAllowedException(RestClientException):
    def __init__(self, resource, failure_reason='', http_verb='GET'):
        super(MethodNotAllowedException, self).__init__(405, failure_reason, http_verb, requested_url=resource)


class NotAcceptableException(RestClientException):
    def __init__(self, resource, failure_reason='', http_verb='GET'):
        super(NotAcceptableException, self).__init__(406, failure_reason, http_verb, requested_url=resource)


class ConflictException(RestClientException):
    def __init__(self, resource, failure_reason='', http_verb='GET'):
        super(ConflictException, self).__init__(409, failure_reason, http_verb, requested_url=resource)


class UnsupportedMediaTypeException(RestClientException):
    def __init__(self, resource, failure_reason='', http_verb='GET'):
        super(UnsupportedMediaTypeException, self).__init__(415, failure_reason, http_verb, requested_url=resource)


class InternalServerErrorException(RestClientException):
    def __init__(self, resource, failure_reason='', http_verb='GET'):
        super(InternalServerErrorException, self).__init__(500, failure_reason, http_verb, requested_url=resource)


EXCEPTIONS_MAPPING = {
    400: 'BadRequestException',
    401: 'UnauthorizedException',
    403: 'ForbiddenException',
    404: 'NotFoundException',
    405: 'MethodNotAllowedException',
    406: 'NotAcceptableException',
    409: 'ConflictException',
    415: 'UnsupportedMediaTypeException',
    500: 'InternalServerErrorException'
}


class RestClient(object):
    """
    :param vdirect_ip: string The primary / standalone vDirect server IP
    :param vdirect_user: string The vDirect user name
    :param vdirect_password: string The vDirect user password
    :param wait: bool Wait for async operation to complete [True]
    :param secondary_vdirect_ip: string The secondary vDirect server IP [None]
    :param https_port: int The https vDirect port [2189]
    :param http_port: int The http vDirect port [2188]
    :param timeout: int How many seconds to wait for async operation [60]
    :param https: bool Use https [True]
    :param strict_http_results: bool Throw exception for status codes 4xx,5xx or not [False]
    :param verify: bool SSL context verification [True]
    :param fetch_result: bool Automatically fetch the result if resultUri exists [False]
    """
    def __init__(self, vdirect_ip=None, vdirect_user=None, vdirect_password=None,wait=None,
                       secondary_vdirect_ip=None,https_port=None,http_port=None,
                       timeout=None,https=None,strict_http_results=None,
                       verify=None,fetch_result=False):

        def _handle_string_input(field_name, field_value):
            if PY3:
                return field_value
            else:
                if isinstance(field_value, unicode):
                    import unicodedata
                    return unicodedata.normalize('NFKD', field_value).encode('ascii', 'ignore')
                elif isinstance(field_value, str):
                    return field_value
                else:
                    raise Exception('Unsupported data type %s for %s. Expected data type: [str,unicode]' %
                                    (type(field_value), field_name))

        self.vdirect_ip = _handle_string_input('vdirect_ip', self._handle_param(vdirect_ip,'VDIRECT_IP',None,True))
        self.vdirect_user = _handle_string_input('vdirect_user', self._handle_param(vdirect_user,'VDIRECT_USER',None,True))
        self.vdirect_password = _handle_string_input('vdirect_password', self._handle_param(vdirect_password,'VDIRECT_PASSWORD',None,True))
        self.secondary_vdirect_ip = _handle_string_input('secondary_vdirect_ip', self._handle_param(secondary_vdirect_ip,'VDIRECT_SECONDARY_IP',None)) if secondary_vdirect_ip else None
        self.https = self._handle_param(https,'VDIRECT_HTTPS',True,converter=self._str2bool)
        self.wait = self._handle_param(wait,'VDIRECT_WAIT',True,converter=self._str2bool)
        self.timeout= self._handle_param(timeout,'VDIRECT_TIMEOUT',60,converter=self._str2int)
        self.verify = self._handle_param(verify,'VDIRECT_VERIFY',True,converter=self._str2bool)
        self.https_port = self._handle_param(https_port,'VDIRECT_HTTPS_PORT',2189,converter=self._str2int)
        self.http_port = self._handle_param(http_port,'VDIRECT_HTTP_PORT',2188,converter=self._str2int)
        self.strict_http_results = self._handle_param(strict_http_results,'VDIRECT_STRICT_HTTP_RESULT',False,converter=self._str2bool)
        self.fetch_result = self._handle_param(fetch_result,'VDIRECT_FETCH_RESULT',False,converter=self._str2bool)
        self.depth = 0
        self.max_depth = 20
        self.base_uri = 'https://%s:%d/api/' % (self.vdirect_ip,self.https_port) if self.https else 'http://%s:%d/api/' % (self.vdirect_ip,self.http_port)
        if self.vdirect_user and self.vdirect_password:
            self.auth = '%s:%s' % (self.vdirect_user, self.vdirect_password)
            if PY3:
                 self.auth = base64.b64encode(self.auth.encode('utf-8'))
                 self.auth = self.auth.decode('utf-8').replace('\n','')
            else:
                self.auth = base64.encodestring(self.auth).replace('\n','')
        else:
            raise RuntimeError('No Username or Password were supplied')

        self.runnable = Runnable(self)
        self.tenant = Tenant(self)

    def _handle_param(self,value,env_variable_name,default_value,mandatory=False,converter=None):
        if value is not None:
            return value if converter is None else converter(value)
        else:
            envp = os.environ.get(env_variable_name)
            if not envp:
                if mandatory:
                    raise Exception('The argument %s is mandatory and must be set.' % env_variable_name)
                else:
                    return default_value
            else:
                return envp if converter is None else converter(envp)

    def _str2bool(self,value):
        if isinstance(value, int):
            return value
        return value == 'True'

    def _str2int(self,value):
        if isinstance(value, int):
            return value
        return int(value)

    def _inc_depth(self):
        self.depth += 1

    def _dec_depth(self):
        self.depth -= 1

    def get_api_meta(self):
        return self._call('GET', '', {})

    def _prepare_value(self, value):
        if PY3:
            return urllib.quote(value, safe='') if isinstance(value, str) else value
        else:
            return urllib.quote(value, safe='') if isinstance(value, basestring) else value

    def _call(self, action, resource,headers, wait=False, data=None, not_json=False):
        self._inc_depth()
        uri = resource if resource.startswith('http') else self.base_uri + resource
        body = data if not_json else json.dumps(data) if not isinstance(data,type(None)) else None
        if not headers:
            headers = {'Authorization': 'Basic %s' % self.auth}
        else:
            headers['Authorization'] = 'Basic %s' % self.auth
        if self.https:
            if not self.verify:
                # HTTPS certificate verification was cancelled in
                # configuration. If python version has context attribute,
                # switch the default context to unverified
                try:
                    _create_unverified_https_context =\
                        ssl._create_unverified_context
                except AttributeError:
                    # Legacy Python that doesn't verify HTTPS
                    # certificates by default
                    pass
                else:
                    # Handle target environment that doesn't
                    # support HTTPS verification
                    ssl._create_default_https_context =\
                        _create_unverified_https_context

            conn = http.HTTPSConnection(
                self.vdirect_ip, port=self.https_port, timeout=self.timeout)

            if conn is None:
                logging.error('vdirectRESTClient: Could not establish HTTPS '
                                     'connection')
                self._dec_depth()
                return 0, None, None, None
        else:
            conn = http.HTTPConnection(
                self.vdirect_ip, self.http_port, timeout=self.timeout)
            if conn is None:
                logging.error('vdirectRESTClient: Could not establish HTTP '
                                     'connection')
                self._dec_depth()
                return 0, None, None, None

        try:
            logging.debug('%s %s %s %s' % (action, uri, str(body), str(headers)))
            conn.request(action, uri, body, headers)
            response = conn.getresponse()
            if response.status in _REDIRECT_CODES:
                if not self.secondary_vdirect_ip:
                    raise Exception('Got redirect but secondary vDirect was not configured')
                peer = response.getheader('Location')
                start = peer.find('://')
                end = peer.rfind(':')
                peer = peer[start + 3:end]
                if peer != self.secondary_vdirect_ip:
                    raise Exception('Got redirect but secondary vDirect: %s is not the same as the peer: %s' % (self.secondary_vdirect_ip,peer))

            respstr = response.read()
            respdata = respstr
            try:
                respdata = json.loads(respstr.decode())
            except ValueError:
                # response was not JSON, ignore the exception
                pass
            ret = response.status, response.reason, respstr, respdata, self._get_content_type(response)
        except ssl.SSLError as sslerr:
            return -1, sslerr[1], 'Consider setting verify (VDIRECT_VERIFY environment variable) parameter to False in order to disable SSL certificates verification', None
        except Exception as e:
            log_dict = {'action': action, 'e': e}
            logging.error('vdirectRESTClient: %(action)s failure, %(e)r' %
                      log_dict)
            ret = -1, None, None, None, None
        conn.close()
        if ret[RESP_STATUS] in (0, -1):
            logging.warning('vDirect server is not responding (%s).' %
                self.vdirect_ip)
            ret = self._recover(action, resource,headers, wait, data, not_json)
        elif ret[RESP_STATUS] in _REDIRECT_CODES:
            logging.warning('vDirect server is not active (%s).' %
            self.vdirect_ip)
            ret = self._recover(action, resource,headers, wait, data, not_json)

        if self.wait and wait and ret[RESP_STATUS] == 202:
            complete = ret[RESP_DATA]['complete']
            if complete:
                self._dec_depth()
                if self.fetch_result and ret[RESP_DATA]['success'] and ret[RESP_DATA].get('resultUri'):
                    self._append_action_result(ret[RESP_DATA])
                return ret
            uri = ret[RESP_DATA]['uri']
            cnt = 0
            while cnt < self.timeout:
                time.sleep(1)
                cnt += 1
                ret = self._call('GET',uri,None,False)
                if ret[RESP_DATA]['complete']:
                    self._dec_depth()
                    if self.fetch_result and ret[RESP_DATA]['success'] and ret[RESP_DATA].get('resultUri'):
                        self._append_action_result(ret[RESP_DATA])
                    return ret
            if cnt <= self.timeout:
                            msg = 'Timeout %s seconds is over and action wasn\'t completed' % self.timeout
                            return -1, 'timeout', msg, msg
            self._dec_depth()
            return ret
        else:
            self._dec_depth()
            return ret

    def _get_content_type(self,response):
        if not response:
            return None
        headers = response.getheaders()
        if not headers:
            return None
        for h in headers:
            if h[0].lower() == 'content-type':
                return h[1]
        return None

    def _append_action_result(self,response):
        """ append the action result to the final result """
        url = response['resultUri']
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        if PY3:
            import urllib.request
            data = urllib.request.urlopen(url,context=ctx).read()
        else:
            import urllib2
            data = urllib2.urlopen(url,context=ctx).read()

        # data can be a string that represents a dict (or not)
        try:
            _data = json.loads(data)
            response['result'] = _data
        except Exception:
            response['result'] = data


    def _flip_servers(self):
        logging.warning('Fliping servers. Current is: {}, switching to {}'.format(self.vdirect_ip,self.secondary_vdirect_ip))
        self.vdirect_ip, self.secondary_vdirect_ip = self.secondary_vdirect_ip, self.vdirect_ip
        self.base_uri = 'https://%s:%d/api/' % (self.vdirect_ip,self.https_port) if self.https else 'http://%s:%d/api/' % (self.vdirect_ip,self.http_port)

    def _recover(self, action, resource,headers, wait, data, not_json):
        if self.vdirect_ip and self.secondary_vdirect_ip:
            if self.depth > self.max_depth:
                msg = 'Both vDirect servers: {} and {} are not responsive'.format(self.vdirect_ip,self.secondary_vdirect_ip)
                logging.error(msg)
                return -1, msg, None, None
            else:
                time.sleep(1)
                self._flip_servers()
                return self._call(action, resource,headers, wait, data, not_json)
        else:
            msg = 'REST client is not able to recover (since only one vDirect server is configured).'
            logging.error(msg)
            return -1, msg, None, None

    def _dict_to_query(self,d):
        query = ''
        for key in list(d.keys()):
            val = d.get(key)
            if val is not None:
                if isinstance(val, bool):
                    val = 'true' if val else 'false'
                query += key + '=' + urllib.quote(str(val), safe='') + "&"
        return query[:-1]

    def _make_final_args(self,path_args,query_args):
        if query_args:
            path_args = path_args[:-1] if path_args.endswith('/') else path_args
            return path_args + '?' + query_args
        else:
           return path_args

    def _handle_result(self,http_verb,result,resource):
        if self.strict_http_results:
            if result[RESP_STATUS] in STRICT_STATUS_CODES[http_verb]:
                return result
            else:
                exception_clazz_name = EXCEPTIONS_MAPPING.get(result[RESP_STATUS])
                if exception_clazz_name:
                    current_module = sys.modules[__name__]
                    clazz = getattr(current_module, exception_clazz_name)
                    raise clazz(resource, failure_reason=result[RESP_STR], http_verb=http_verb)
                else:
                    raise RestClientException(result[RESP_STATUS], result[RESP_REASON], http_verb,
                                              STRICT_STATUS_CODES[http_verb], requested_url=resource,
                                              failure_msg=result[RESP_STR])
        else:
            if result[RESP_STATUS] in NON_STRICT_STATUS_CODES[http_verb]:
                return result
            else:
                raise RestClientException(result[RESP_STATUS],result[RESP_REASON],http_verb,NON_STRICT_STATUS_CODES[http_verb],requested_url=resource, failure_msg=result[RESP_STR])


class Runnable:
    def __init__(self, client):
        self.client = client

    def get_available_actions(self,type,name):
        """
        :returns: application/json
        """
        final_path = 'runnable/%s/%s/' % (self.client._prepare_value(type),self.client._prepare_value(name))
        result = self.client._call('GET',final_path,{})
        return self.client._handle_result('GET',result,final_path)

    def get_action_info(self,type,name,action):
        """
        :returns: application/json
        """
        final_path = 'runnable/%s/%s/%s/' % (self.client._prepare_value(type),self.client._prepare_value(name),self.client._prepare_value(action))
        result = self.client._call('GET',final_path,{})
        return self.client._handle_result('GET',result,final_path)

    def run(self,data,type,name,action):
        """
        :returns: application/vnd.com.radware.vdirect.status+json
        """
        final_path = 'runnable/%s/%s/%s/' % (self.client._prepare_value(type),self.client._prepare_value(name),self.client._prepare_value(action))
        result = self.client._call('POST',final_path,{"Content-Type":"application/json"},wait=True ,data=data)
        return self.client._handle_result('POST',result,final_path)

    def get_types(self):
        """
        :returns: application/json
        """
        final_path = 'runnable/'
        result = self.client._call('GET',final_path,{})
        return self.client._handle_result('GET',result,final_path)

    def get_runnable_objects(self,type):
        """
        :returns: application/json
        """
        final_path = 'runnable/%s/' % (self.client._prepare_value(type))
        result = self.client._call('GET',final_path,{})
        return self.client._handle_result('GET',result,final_path)

    def get_catalog(self):
        """
        :returns: application/json
        """
        final_path = 'runnable/catalog/'
        result = self.client._call('GET',final_path,{})
        return self.client._handle_result('GET',result,final_path)


class Tenant:
    def __init__(self, client):
        self.client = client

    def create(self,data):
        """
        :returns: application/vnd.com.radware.vdirect.tenant+json
        """
        final_path = 'tenant/'
        result = self.client._call('POST',final_path,{"Content-Type":"application/vnd.com.radware.vdirect.tenant+json"},data=data)
        return self.client._handle_result('POST',result,final_path)

