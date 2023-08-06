from workfront.exceptions import raise_if_not_ok


class WFObject(object):

    def __init__(self, wf, obj_code, idd):
        self.wf = wf
        self.wf_id = idd
        self.obj_code = obj_code
        self._name = None

    def _init_fields(self, data):
        self._update_fields(data)

    def _raise_if_not_ok(self, resp):
        raise_if_not_ok(resp, self.obj_code, self.wf_id)

    def to_json(self):
        js = {
              "objCode": "PRJ",
              "ID": self.wf_id,
              "name": self.name,
        }
        return js

    def get_fields(self, fields):
        '''
        @return: Perform a HTTP GET to the current object and return what it is
        inside the 'data' json field.
        @param fields: list of fields to be retrieve for the current object.
        The comodin '*' can be used here.
        '''
        fls = fields[:]
        fls.extend(self._get_update_fields())
        r = self.wf.get_object(self.obj_code, self.wf_id, set(fls))
        self._raise_if_not_ok(r)
        self._update_fields(r.json()["data"])
        return r.json()["data"]

    def set_fields(self, fields):
        '''
        @summary: Perform a HTTP PUT to the current object.
        @param fields: dictionary of fields being added/modified.
        '''
        r = self.wf.put_object(self.obj_code, self.wf_id, fields)
        self._raise_if_not_ok(r)

    def delete(self, force=True):
        url = "%s/%s" % (self.obj_code, self.wf_id)
        if force:
            url = url + "?force=true"
        r = self.wf._delete(url)
        self._raise_if_not_ok(r)

    def _update_fields(self, data):
        '''
        @param data: dictionary with fields belonging to this object; typically
        from a get_fields request data object.
        When a request is made to get fields for this object, some fields are
        updated on this object at the same. This is make in order to save
        request to the WF API.
        '''
        self._name = data.get("name")

    def _get_update_fields(self):
        '''
        @return: a list of fields to be used in this object to any call make in
        order to get fields.
        '''
        return ["name"]

    @property
    def name(self):
        if self._name is None or self._name == "UNKNOWN":
            try:
                self._name = self.get_fields(["name"])["name"]
            except Exception:
                self._name = "UNKNOWN"
        return self._name

    def __repr__(self):
        return "{} - {} - {} - {}".format(type(self).__name__, self.obj_code,
                                          self.name, self.wf_id)
