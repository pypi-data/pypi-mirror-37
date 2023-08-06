from workfront.objects.fields import user as user_fields
from workfront.objects.codes import WFObjCode
from workfront.objects.generic_objects import WFObject


def from_id(wf, idd):
    '''
    @summary: Construct a WFUser object from a valid workfront user id.
    @param wf: A Workfront service object
    @param idd: workfront id of the existing user
    '''
    r = wf.search_objects(WFObjCode.user, {"ID": idd}, user_fields)
    return WFUser.create_from_js(wf, r.json()["data"][0])


def from_email(wf, email):
    '''
    @summary: Construct a WFUser object from a workfront user that has the
    given email.
    @param wf: A Workfront service object
    @param email: email of an existing workfront user
    '''
    r = wf.search_objects(WFObjCode.user, {"emailAddr": email}, user_fields)
    return WFUser.create_from_js(wf, r.json()["data"][0])


class WFUser(WFObject):
    '''
    @summary: a Workfront user helper class
    '''

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param js: a  json object representing a workfront user.
        '''
        super(WFUser, self).__init__(wf, WFObjCode.user, idd)
        self.wf = wf
        self._emailAddr = None

    def _update_fields(self, data):
        super(WFUser, self)._update_fields(data)
        self._emailAddr = data.get("emailAddr")

    def _get_update_fields(self):
        fields = super(WFUser, self)._get_update_fields()
        fields.append("emailAddr")
        return fields

    @property
    def emailAddr(self):
        if self._emailAddr is None:
            self._emailAddr = self.get_fields(["emailAddr"])["emailAddr"]
        return self._emailAddr

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF USER from the API.
        It should at least have the "ID" field.
        '''
        u = WFUser(wf, js["ID"])
        u._init_fields(js)
        return u
