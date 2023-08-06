"""
Arkindex API Client
"""
import requests
import os
from six.moves.urllib.parse import urljoin
from arkindex import DEFAULT_HOST


class ArkindexAPI(object):

    def __init__(self, token=None, host=DEFAULT_HOST, verify_ssl=True):
        """
        :param token: An API token. If not specified, endpoints that require authentication will
            not be available until :meth:`ArkindexAPI.login` is called.
        :type token: str or None
        :param host: Hostname of the Arkindex server to use. Defaults to :data:`arkindex.DEFAULT_HOST`.
        :type host: str
        :param verify_ssl: Set to ``True`` or ``False`` to toggle HTTPS certificate checks.
            Set to a ``str`` value to set the path of a certificate bundle to use for HTTPS.
            See requests' ``request()`` method for more info.
        :type verify_ssl: str or bool
        """

        self.auth = ArkindexTokenAuth(token) if token else None
        """An instance of :class:`ArkindexTokenAuth` if there is a token available, or None."""

        self.base_url = 'https://{}/api/v1/'.format(host)
        """The API endpoints base URL to which endpoint names are appended."""

        if isinstance(verify_ssl, str):
            assert os.path.exists(verify_ssl)
        self.verify_ssl = verify_ssl
        """``str`` or ``bool`` to set requests' HTTPS certificate checking."""

    def get(self, endpoint, params={}, requires_auth=False):
        """
        Perform a GET request on an Arkindex API endpoint.

        :param endpoint: Endpoint to perform requests on, without ``/api/v1/``.
        :type endpoint: str
        :param params: GET parameters to send in the URL.
        :type params: dict
        :param requires_auth: Set to ``True`` to raise :class:`ArkindexAPIError` if the client
            does not have an available API token.
        :type requires_auth: bool
        :return: Parsed JSON data returned by the server.
        :rtype: Any type returned by ``json.loads``.
        :raises ArkindexAPIError: If ``requires_auth`` is set to True and the client is missing an API token.
        :raises HTTPError: If the request did not give a success HTTP status code (4xx or 5xx)
        """
        response = requests.get(
            urljoin(self.base_url, endpoint),
            params=params,
            auth=self._get_auth(requires_auth),
            verify=self.verify_ssl,
        )
        response.raise_for_status()
        return response.json()

    def post(self, endpoint, params=None, json=None, files=None, requires_auth=False):
        """
        Perform a POST request on an Arkindex API endpoint.

        :param endpoint: Endpoint to perform requests on, without ``/api/v1/``.
        :type endpoint: str
        :param params: GET parameters to send in the URL.
        :type params: dict or None
        :param json: Optional JSON body to send with the request.
        :param files: File-like objects to send with the request.
        :type files: dict(str, object) or None
        :param requires_auth: Set to ``True`` to raise :class:`ArkindexAPIError` if the client
            does not have an available API token.
        :type requires_auth: bool
        :return: Parsed JSON data returned by the server.
        :rtype: Any type returned by ``json.loads``.
        :raises ArkindexAPIError: If ``requires_auth`` is set to True and the client is missing an API token
            or if the response has a HTTP 400 code and has an error JSON body.
        :raises HTTPError: If the request did not give a success HTTP status code (4xx or 5xx)
        """
        response = requests.post(
            urljoin(self.base_url, endpoint),
            params=params,
            json=json,
            files=files,
            auth=self._get_auth(requires_auth),
            verify=self.verify_ssl,
        )
        if response.status_code == requests.codes.bad_request:
            try:
                self.bad_request_handler(response.json())
            except ArkindexAPIError:
                # Ignore everything but Arkindex exceptions from the custom handler
                raise
            except Exception:
                pass
        response.raise_for_status()
        return response.json()

    def bad_request_handler(self, json):
        """
        Custom handler for HTTP 400 Bad Request when the request has a JSON body.

        :param json: Parsed JSON data returned by the server.
        :raises ArkindexAPIError: Always raises, with a potentially easier to read error message.
        """
        if isinstance(json, list):
            raise ArkindexAPIError(' - '.join(json))
        elif isinstance(json, dict):
            if 'detail' in json:
                raise ArkindexAPIError(json['detail'])
            if len(json) == 1:
                # Handle dicts with a single key by handling the single value
                return self.bad_request_handler(next(iter(json)))
        raise ArkindexAPIError(json)

    def login(self, email, password):
        '''
        Login on an Arkindex server with an email and a password.
        This does not automatically save the API token.

        :param email str: The email address to login with.
        :param password str: The password to login with.
        :return: User information, including a ``auth_token`` key with the API token to use.
        :rtype: dict
        :raises ArkindexAPIError: The response has a HTTP 400 status code and a JSON error body.
        :raises HTTPError: The response has a HTTP 4xx or 5xx status code.
        '''
        return self.post('user/login/', json={
            'email': email,
            'password': password,
        })

    def whoami(self):
        """
        Fetch user information from the server.

        :return: User information, including a ``auth_token`` key with the API token to use.
        :rtype: dict
        :raises ArkindexAPIError: The API client does not have a valid API token.
        :raises HTTPError: The response has a HTTP 4xx or 5xx status code.
        """
        return self.get('user/', requires_auth=True)

    def get_elements(self, type='volume', corpus_id=None):
        """
        List all elements in a single corpus or all corpora by element type.

        :param type str: The element type (``volume``, ``page``, etc) to list.
        :param corpus_id: UUID of a corpus to filter on. If set to None, will list elements of all corpora.
        :type corpus_id: str or None
        :return: Generator yielding a ``dict`` for each element.
        :rtype: ResponsePaginator
        """
        return ResponsePaginator(self, 'elements/', params={'type': type, 'corpus': corpus_id})

    def get_related(self, id, type='page'):
        """
        List parent and children elements of a single element by ID, filtered by type.

        :param id str: UUID of the element to list related elements from.
        :param type str: Element type (``volume``, ``page``) to list.
        :return: Generator yielding a ``dict`` for each element.
        :rtype: ResponsePaginator
        """
        return ResponsePaginator(self, 'elements/{}/'.format(id), params={'type': type})

    def get_pages(self, id):
        """
        List all pages marked as children of a single element.

        :param id str: UUID of the element to find child pages on.
        :return: Generator yield a ``dict`` for each page.
        :rtype: ResponsePaginator
        """
        return ResponsePaginator(self, 'elements/{}/pages/'.format(id))

    def get_corpora(self):
        """
        List all available corpora with the available access rights.

        :return: List of corpora.
        :rtype: list(dict)
        """
        return self.get('corpus/')

    def create_transcription(self, **kwargs):
        r"""
        Create a single transcription.

        :param \**kwargs: Transcription data to send as a JSON body.
        :return: Parsed JSON data for the resulting created transcription.
        :raises ArkindexAPIError: If the client is missing a valid API token.
        """
        return self.post('transcription/', json=kwargs, requires_auth=True)

    def create_bulk_transcriptions(self, **kwargs):
        r"""
        Create multiple transcriptions at once.

        :param \**kwargs: Transcriptions data to send as a JSON body.
        :return: Parsed JSON data for the resulting created transcriptions.
        :raises ArkindexAPIError: If the client is missing a valid API token.
        """
        return self.post('transcription/bulk/', json=kwargs, requires_auth=True)

    def upload_file(self, corpus_id, file_path):
        """
        Upload a file to a corpus.

        :param corpus_id str: UUID of a corpus with write access to upload files on.
        :param file_path str: Path of a file to upload.
        :return: Parsed JSON data for the saved file.
        :raises ArkindexAPIError: If the client is missing a valid API token.
        """
        return self.post(
            'imports/upload/{}/'.format(corpus_id),
            files={'file': open(file_path, 'rb')},
            requires_auth=True,
        )

    def import_from_files(self, mode, file_ids):
        """
        Start an import process with some files.

        :param mode str: The import mode (``pdf`` or ``images``). Defaults to ``images``.
        :param file_ids: List of uploaded file UUIDs.
        :type file_ids: list(str)
        :return: Parsed JSON data for the started process.
        :rtype: dict
        :raises ArkindexAPIError: If the client is missing a valid API token.
        """
        return self.post(
            'imports/fromfiles/',
            json={'mode': mode, 'files': file_ids},
            requires_auth=True,
        )

    def _get_auth(self, requires_auth):
        if requires_auth and not self.auth:
            raise ArkindexAPIError(
                'This endpoint requires authentication, but no credentials have been provided')
        return self.auth


class ResponsePaginator(object):
    """
    A lazy generator to handle paginated Arkindex API endpoints.
    Does not perform any requests to the API until it is required.
    """

    def __init__(self, client, *request_args, **request_kwargs):
        r"""
        :param client ArkindexAPI: An API client to use to perform requests for each page.
        :param \*request_args: Arguments to send to :meth:`ArkindexAPI.get`.
        :param \**request_kwargs: Keyword arguments to send to :meth:`ArkindexAPI.get`.
        """
        assert isinstance(client, ArkindexAPI)
        self.client = client
        """The Arkindex API client used to perform requests on each page."""

        self.data = {}
        """Stored data from the last performed request."""

        self.results = []
        """Stored results from the last performed request."""

        self.request_args = request_args
        """Arguments to send to :meth:`ArkindexAPI.get` with each request."""

        self.request_kwargs = request_kwargs
        """
        Keyword arguments to send to :meth:`ArkindexAPI.get` with each request.
        ``['params']['page']`` is overriden to set the page number.
        """

        if "params" not in self.request_kwargs:
            self.request_kwargs['params'] = {}
        self.current_page = 0
        """The current page number. 0 if no pages have been requested yet."""

    def _fetch_page(self, page):
        self.request_kwargs['params']['page'] = page
        self.data = self.client.get(*self.request_args, **self.request_kwargs)
        self.results = self.data.get('results', [])
        self.current_page = page

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.results) < 1:
            if self.data and self.data.get('next') is None:
                raise StopIteration
            self._fetch_page(self.current_page + 1)
        return self.results.pop(0)

    def __len__(self):
        # Handle calls to len when no requests have been made yet
        if not self.data and self.current_page < 1:
            self._fetch_page(1)
        return self.data['count']


class ArkindexTokenAuth(requests.auth.AuthBase):
    """
    HTTP Authentication using a token.
    """

    def __init__(self, token):
        """
        :param token str: API token.
        """
        self.token = token
        """The API token."""

    def __call__(self, request):
        request.headers['Authorization'] = "Token {}".format(self.token)
        return request


class ArkindexAPIError(Exception):
    """
    Describes any handled error from the Arkindex API.
    """
