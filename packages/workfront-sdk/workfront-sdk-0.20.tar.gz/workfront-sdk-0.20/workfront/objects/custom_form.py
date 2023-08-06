from workfront.objects.codes import WFObjCode
from workfront.objects.generic_objects import WFObject
from workfront.objects.parameter import WFParamenter
from workfront.exceptions import WFException


def get_custom_forms(wf, filter_dic={}):
    '''
    @param wf: Worfront service object
    @param filter_dic : filter dictionary. Like {"isActive" : True} ; to only
    get active portfolios.
    @return a list of dictionaries where each dict has:
    - ID : wf id of the portfolio
    - name : name of the portfolio
    - isActive : Boolean indicating if the portfolio is active or not
    '''
    r = wf.search_objects(WFObjCode.category, filter_dic, ["ID", "name",
                                                           "isActive"])
    return r.json()["data"]


def get_custom_form_by_name(wf, name):
    '''
    @param wf: Worfront service object
    @param name: of the custom form (category)
    '''
    r = wf.search_objects(WFObjCode.category, {"name": name}, ["ID", "name"])
    if len(r.json()["data"]) < 1:
        raise WFException("No Custom Form found with name %s" % name)
    cf = WFCustomForm.create_from_js(wf, r.json()["data"][0])
    return cf


class WFCustomForm(WFObject):

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of the custom form (category)
        '''
        super(WFCustomForm, self).__init__(wf, WFObjCode.category, idd)

    def get_parameters(self):
        '''
        @return: a list of WFParameter objects that belongs to the current
        custom form.
        '''
        data = self.get_fields(["categoryParameters:parameter:*"])
        parameters = []
        for cat_param in data["categoryParameters"]:
            param = cat_param["parameter"]
            parameter_obj = WFParamenter.create_from_js(self.wf, param)
            parameters.append(parameter_obj)
        return parameters

    def get_parameters_by_name(self):
        '''
        @return: A dictionary keyed by parameter name which values are the
        corresponding WFParamenter objects.
        '''
        p_by_name = {}
        for p in self.get_parameters():
            p_by_name[p.name] = p
        return p_by_name

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF CATEGORY from the API.
        It should at least have the "ID" field.
        '''
        cf = WFCustomForm(wf, js["ID"])
        cf._init_fields(js)
        return cf
