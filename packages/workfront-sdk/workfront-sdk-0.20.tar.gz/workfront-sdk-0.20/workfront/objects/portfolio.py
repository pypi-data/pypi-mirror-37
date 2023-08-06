from workfront.objects.codes import WFObjCode
from workfront.objects.generic_object_param_value import WFParamValuesObject


def get_all_portfolios(wf, filter_dic={}):
    '''
    @param filter_dic : filter dictionary. Like {"isActive" : True} ; to only
    get active portfolios.
    @return a list of dictionaries where each dict has:
    - ID : wf id of the portfolio
    - name : name of the portfolio
    - isActive : Boolean indicating if the portfolio is active or not
    '''
    r = wf.search_objects(WFObjCode.portfolio, filter_dic, ["ID", "name",
                                                            "isActive"])
    return r.json()["data"]


class WFPortfolio(WFParamValuesObject):

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of the portfolio
        '''
        super(WFPortfolio, self).__init__(wf, WFObjCode.portfolio, idd)

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF PORTFOLIO from the API.
        It should at least have the "ID" field.
        '''
        p = WFPortfolio(wf, js["ID"])
        p._init_fields(js)
        return p
