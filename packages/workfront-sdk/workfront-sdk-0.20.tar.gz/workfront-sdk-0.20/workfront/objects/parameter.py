from workfront.objects.codes import WFObjCode
from workfront.objects.generic_objects import WFObject
from workfront.exceptions import WFException


def get_parameter_by_name(wf, name):
    '''
    @return a WFParamenter object which name is the one given
    '''
    r = wf.search_objects(WFObjCode.parameter, {"name": name}, ["ID", "name"])
    if len(r.json()["data"]) < 1:
        raise WFException("No parameter found with name %s" % name)
    parameter = WFParamenter.create_from_js(wf, r.json()["data"][0])
    return parameter


class WFParamenter(WFObject):

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of the parameter
        '''
        super(WFParamenter, self).__init__(wf, WFObjCode.parameter, idd)

    def get_value_options(self):
        '''
        @return: A list of values that the parameter accepts
        '''
        data = self.get_fields(["parameterOptions:*"])
        return [po["value"] for po in data["parameterOptions"]]

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF PARAMETER from the API.
        It should at least have the "ID" field.
        '''
        p = WFParamenter(wf, js["ID"])
        p._init_fields(js)
        return p
