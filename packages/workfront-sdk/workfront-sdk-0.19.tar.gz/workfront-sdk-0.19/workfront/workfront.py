from __future__ import absolute_import

from collections import OrderedDict

from requests import session
from workfront.exceptions import WFException
import datetime as dt
from urllib import urlencode as urlencode


class WFEventType:
    CREATE = "CREATE"
    DELETE = "DELETE"
    UPDATE = "UPDATE"
    SHARE = "SHARE"


class Workfront(object):
    '''
    @summary: A workfront service object that is used to interact with the
    Workfront API.
    '''
    def_wf_domain = "thebridgecorp.my.workfront.com"

    def __init__(self, user, passw, wf_domain=def_wf_domain):
        '''
        @param user: user used to login into WF (probably email)
        @param passw: password for the given user
        @param wf_domain: domain of the workfront instance. Probably something
        like corporation.my.workfront.com
        '''
        self.sess = session()
        self.user = user
        self.passw = passw
        self._wf_last_connect = dt.datetime.now() - dt.timedelta(weeks=65)
        self.sess_id = None
        self.url_base = "https://{}/attask/api/v7.0/".format(wf_domain)

    def get_api_url(self):
        return self.url_base

    @property
    def sess_id(self):
        # Force the service to reconnect after 25 minutes to avoid expired
        # sessions
        tdiff = dt.datetime.now() - self._wf_last_connect
        if tdiff > dt.timedelta(minutes=25) or self._sess_id is None:
            self.login()
        return self._sess_id

    @sess_id.setter
    def sess_id(self, value):
        self._sess_id = value

    def login(self):
        '''
        @summary: login against the WF API and save the session id for future
        requests
        '''
        url = self.url_base + "login?username=%s&password=%s"
        r = self.sess.post(url % (self.user, self.passw))
        if r.status_code is not 200:
            e = "Could not log in to Workfront: {}".format(r.json())
            raise WFException(e)
        self.sess_id = r.json()["data"]["sessionID"]
        self._wf_last_connect = dt.datetime.now()

    def logout(self):
        '''
        @summary: logout, invalidating the current session id
        '''
        u = self.url_base + "logout"
        self.sess.get(u)
        self.sess_id = None

    def _post(self, url, js):
        '''
        @param url: url part of the object being posted (not the url base)
        @param js: json body to be send
        '''
        u = self.url_base + url
        hs = {"SessionID": self.sess_id}
        r = self.sess.post(u, json=js, headers=hs)
        return r

    def _put(self, url, **kwargs):
        '''
        @param url: url part of the object being put (not the url base)
        '''
        u = self.url_base + url
        hs = {"SessionID": self.sess_id}
        r = self.sess.put(u, headers=hs, **kwargs)
        return r

    def _get(self, url):
        '''
        @param url: url part of the object being get (not the url base)
        '''
        u = self.url_base + url
        hs = {"SessionID": self.sess_id}
        r = self.sess.get(u, headers=hs)
        return r

    def _delete(self, url):
        '''
        @param url: url part of the object being put (not the url base)
        '''
        u = self.url_base + url
        hs = {"SessionID": self.sess_id}
        r = self.sess.delete(u, headers=hs)
        return r

    def search_objects(self, obj, param_dict, fields=[], order_by=None, from_index=None, limit=None):
        """
        @summary: Do a search of the objects restricted by the fields given in
        the param_dict

        @param obj: object code being searched
        @param param_dict: dictionary of query strings (key = value)
        @param fields: fields being retrieved for the object

        @type  order_by: OrderedDict
        @param order_by: Order by parameters. The order insertion determines the order by priority.
        (default: {"entryDate":"desc"})
            Ex: order = OrderedDict()
                order["name"] = "asc"
                order["entryDate"] = "desc"
                the order priority will be: by name asc and then entryDate desc

        @type from_index: int
        @param from_index: specify the first result index that should be returned (start at 0)

        @type limit: int
        @param limit: specify the maximum amount results that should be returned

        @rtype: dict
        @return: A dictionary with WF Projects
        """

        parameters = param_dict.copy()

        if from_index is not None and limit is not None:
            parameters.update({"$$FIRST": from_index, "$$LIMIT": limit})

        if isinstance(order_by, OrderedDict):
            index = 0
            for key, value in order_by.iteritems():
                index += 1
                parameters[key + "_" + str(index) + "_Sort"] = value

        url = "%s/search" % obj

        if len(parameters) > 0:
            # TODO: bug if a parameter contains "&"
            qs = ["{}={}".format(k, v) for k, v in parameters.items()]

            if len(fields) > 0:
                # TODO: bug if a parameter contains "&"
                qs.append("fields={}".format(",".join(fields)))

            qs = "&".join(qs)
            url = url + "?" + qs

        return self._get(url)

    def count_objects(self, obj, filters):
        """
        @summary: Do a count of the objects restricted by the fields given in
        the filters dictionary
        
        @param obj: object code being searched
        @param filters: dictionary of filter for query
        """

        url = "%s/count" % obj
        if len(filters) > 0:
            qs = urlencode(filters.items())
            url = url + "?" + qs

        return self._get(url)

    def get_object(self, obj, idd, fields=[]):
        '''
        @param obj: object code being retrieved
        @param idd: WF id of the object
        @param fields: list of fields being retrieved for the given object. If
        not given, the fields retrieved will be the custom one.
        '''
        url = "%s/%s" % (obj, idd)
        if len(fields):
            url = url + "?fields=%s" % ",".join(fields)
        return self._get(url)

    def put_object(self, obj, idd, param_dict={}):
        '''
        @summary: Do a put object
        @param obj: obj code
        @param idd: WF id of the object being put
        @param param_dict: dictionary of query strings (key = value)
        '''
        url = "%s/%s" % (obj, idd)
        qs = urlencode(param_dict.items())
        url = url + "?" + qs
        return self._put(url)

    def post_object(self, obj, param_dict={}):
        '''
        @summary: Do a post object
        @param obj: obj code
        @param param_dict: dictionary of query strings (key = value)
        '''
        return self._post(obj, param_dict)

    def action(self, obj, idd, action, param_dict):
        '''
        @summary: Perform an action for the object given.
        @param obj: obj code
        @param idd: WF id of the object being put
        @param action: action being done for the given object
        @param param_dict: dictionary of query strings (key = value)
        '''
        param_dict["action"] = action
        return self.put_object(obj, idd, param_dict)

    def bulk_action(self, obj, action, param_dict):
        '''
        @summary: Perform an action for the object given.
        @param obj: obj code
        @param action: action being done for the given type of object
        @param param_dict: json with fields required by the action
        '''
        url = "{}?action={}".format(obj, action)
        return self._put(url, json=param_dict)

    def get_api_key(self):
        '''
        @summary: Get a Workfront API key.
        '''
        u = self.url_base + "USER?action=getApiKey&username=%s&password=%s"
        u = u % (self.user, self.passw)
        hs = {"SessionID": self.sess_id}
        return self.sess.put(u, hs).json()["data"]["result"]

    def gen_api_key(self):
        '''
        @summary: Generate a Workfront API key.
        '''
        u = self.url_base + "USER/generateApiKey?username=%s&password=%s"
        u = u % (self.user, self.passw)
        hs = {"SessionID": self.sess_id}
        return self.sess.put(u, hs).json()["data"]["result"]
