from tenable.base import APISession
from .agent_config import AgentConfigAPI
from .agent_exclusions import AgentExclusionsAPI
from .agent_groups import AgentGroupsAPI
from .agents import AgentsAPI
from .assets import AssetsAPI
from .audit_log import AuditLogAPI
from .editor import EditorAPI
from .exclusions import ExclusionsAPI
from .exports import ExportsAPI
from .file import FileAPI
from .filters import FiltersAPI
from .folders import FoldersAPI
from .groups import GroupsAPI
from .permissions import PermissionsAPI
from .plugins import PluginsAPI
from .policies import PoliciesAPI
from .scanner_groups import ScannerGroupsAPI
from .scanners import ScannersAPI
from .scans import ScansAPI
from .server import ServerAPI
from .session import SessionAPI
from .target_groups import TargetGroupsAPI
from .users import UsersAPI
from .workbenches import WorkbenchesAPI


class TenableIO(APISession):
    '''
    The Tenable.io object is the primary interaction point for users to
    interface with Tenable.io via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        access_key (str):
            The user's API access key for Tenable.io
        secret_key (str):
            The user's API secret key for Tenable.io
        url (str, optional):
            The base URL that the paths will be appended onto.  The default
            is ``https://cloud.tenable.com`` 
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``0.1`` seconds.
    '''
    
    _tzcache = None
    _url = 'https://cloud.tenable.com'

    @property
    def agent_config(self):
        '''
        An object for interfacing to the agent configurations API.  See the
        :doc:`agent_config documentation <io.agent_config>` 
        for full details.
        '''
        return AgentConfigAPI(self)

    @property
    def agent_groups(self):
        '''
        An object for interfacing to the agent groups API.  See the
        :doc:`agent_groups documentation <io.agent_groups>` 
        for full details.
        '''
        return AgentGroupsAPI(self)

    @property
    def agent_exclusions(self):
        '''
        An object for interfacing to the agent exclusions API.  See the
        :doc:`agent_exclusions documentation <io.agent_exclusions>` 
        for full details.
        '''
        return AgentExclusionsAPI(self)

    @property
    def agents(self):
        '''
        An object for interfacing to the agents API.  See the
        :doc:`agents documentation <io.agents>` 
        for full details.
        '''
        return AgentsAPI(self)

    @property
    def assets(self):
        '''
        An object for interfacing to the assets API.  See the
        :doc:`assets documentation <io.assets>` 
        for full details.
        '''
        return AssetsAPI(self)

    @property
    def audit_log(self):
        '''
        An object for interfacing to the audit log API.  See the
        :doc:`audit_log documentation <io.audit_log>` 
        for full details.
        '''
        return AuditLogAPI(self)

    @property
    def editor(self):
        '''
        An object for interfacing to the editor API.  See the
        :doc:`editor documentation <io.editor>` 
        for full details.
        '''
        return EditorAPI(self)

    @property
    def exclusions(self):
        '''
        An object for interfacing to the exclusions API.  See the
        :doc:`exclusions documentation <io.exclusions>` 
        for full details.
        '''
        return ExclusionsAPI(self)

    @property
    def exports(self):
        '''
        An object for interfacing to the exports API.  See the
        :doc:`exports documentation <io.exports>` 
        for full details.
        '''
        return ExportsAPI(self)

    @property
    def file(self):
        '''
        An object for interfacing to the file API.  See the
        :doc:`file documentation <io.file>` 
        for full details.
        '''
        return FileAPI(self)

    @property
    def filters(self):
        '''
        An object for interfacing to the filters API.  See the
        :doc:`filters documentation <io.filters>` 
        for full details.
        '''
        return FiltersAPI(self)

    @property
    def folders(self):
        '''
        An object for interfacing to the folders API.  See the
        :doc:`folders documentation <io.folders>` 
        for full details.
        '''
        return FoldersAPI(self)

    @property
    def groups(self):
        '''
        An object for interfacing to the groups API.  See the
        :doc:`groups documentation <io.groups>` 
        for full details.
        '''
        return GroupsAPI(self)

    @property
    def permissions(self):
        '''
        An object for interfacing to the permissions API.  See the
        :doc:`permissions documentation <io.permissions>` 
        for full details.
        '''
        return PermissionsAPI(self)

    @property
    def plugins(self):
        '''
        An object for interfacing to the plugins API.  See the
        :doc:`plugins documentation <io.plugins>` 
        for full details.
        '''
        return PluginsAPI(self)

    @property
    def policies(self):
        '''
        An object for interfacing to the policies API.  See the
        :doc:`policies documentation <io.policies>` 
        for full details.
        '''
        return PoliciesAPI(self)

    @property
    def scanner_groups(self):
        '''
        An object for interfacing to the scanner groups API.  See the
        :doc:`scanner_groups documentation <io.scanner_groups>` 
        for full details.
        '''
        return ScannerGroupsAPI(self)

    @property
    def scanners(self):
        '''
        An object for interfacing to the scanners API.  See the
        :doc:`scanners documentation <io.scanners>` 
        for full details.
        '''
        return ScannersAPI(self)

    @property
    def scans(self):
        '''
        An object for interfacing to the scans API.  See the
        :doc:`scans documentation <io.scans>` 
        for full details.
        '''
        return ScansAPI(self)

    @property
    def server(self):
        '''
        An object for interfacing to the server API.  See the
        :doc:`server documentation <io.server>` 
        for full details.
        '''
        return ServerAPI(self)

    @property
    def session(self):
        '''
        An object for interfacing to the session API.  See the
        :doc:`session documentation <io.session>` 
        for full details.
        '''
        return SessionAPI(self)

    @property
    def target_groups(self):
        '''
        An object for interfacing to the target groups API.  See the
        :doc:`target_groups documentation <io.target_groups>` 
        for full details.
        '''
        return TargetGroupsAPI(self)

    @property
    def users(self):
        '''
        An object for interfacing to the users API.  See the
        :doc:`users documentation <io.users>` 
        for full details.
        '''
        return UsersAPI(self)

    @property
    def workbenches(self):
        '''
        An object for interfacing to the workbenches API.  See the
        :doc:`workbenches documentation <io.workbenches>` 
        for full details.
        '''
        return WorkbenchesAPI(self)

    @property
    def _tz(self):
        '''
        As we will be using the timezone listing in a lot of parameter checking,
        we should probably cache the response as a private attribute to speed 
        up checking times.
        '''
        if not self._tzcache:
            self._tzcache = self.scans.timezones()
        return self._tzcache

    def __init__(self, access_key, secret_key, url=None, retries=None, backoff=None):
        self._access_key = access_key
        self._secret_key = secret_key
        APISession.__init__(self, url, retries, backoff)

    def _retry_request(self, response, retries, kwargs):
        '''
        If the call is retried, we will need to set some additional headers
        '''
        if 'headers' not in kwargs:
            kwargs['headers'] = dict()

        if 'X-Request-Uuid' in response.headers:
            # if the request uuid exists in the response, then we will sent the
            # uuid back so that there is solid requesty chain in any subsiquent
            # logs.
            kwargs['headers']['X-Tio-Last-Request-Uuid'] = response.headers['X-Request-Uuid']

        # We also need to return the number of times that we have attempted to
        # retry this call.
        kwargs['headers']['X-Tio-Retry-Count'] = retries
        return kwargs


    def _build_session(self):
        '''
        Build the session and add the API Keys into the session
        '''
        APISession._build_session(self)
        self._session.headers.update({
            'X-APIKeys': 'accessKey={}; secretKey={};'.format(
                self._access_key, self._secret_key)
        })
