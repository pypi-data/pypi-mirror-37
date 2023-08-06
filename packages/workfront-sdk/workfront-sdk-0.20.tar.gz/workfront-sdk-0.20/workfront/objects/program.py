from workfront.objects.generic_object_param_value import WFParamValuesObject
import workfront.objects.portfolio
from workfront.objects.codes import WFObjCode


def create_new(wf, params={}):
    '''
    :param params: dict of details for new project (must have: name,
    portfolioID)
    :return: Object of the new program
    '''
    r = wf.post_object("program", params)
    p = WFProgram.create_from_js(wf, r.json()["data"])
    return p


class WFProgram(WFParamValuesObject):

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of the program
        '''
        super(WFProgram, self).__init__(wf, WFObjCode.program, idd)

    def get_portfolio(self):
        '''
        @return: the portfolio asociated with this program.
        '''
        r = self.wf.get_object(self.obj_code, self.wf_id, ["portfolio:ID"])
        self._raise_if_not_ok(r)

        portf = r.json()["data"]["portfolio"]
        return workfront.objects.portfolio.WFPortfolio.create_from_js(self.wf,
                                                                      portf)

    def get_projects(self):
        '''
        @return: A list of WFProject objects which belongs to this program
        '''
        r = self.wf.get_object(self.obj_code, self.wf_id, ["projects:ID"])
        self._raise_if_not_ok(r)

        projects = []
        for pdata in r.json()["data"]["projects"]:
            t = workfront.objects.project.WFProject.create_from_js(self.wf,
                                                                   pdata)
            projects.append(t)
        return projects

    def set_projects(self, projects=[]):
        '''
        Sets the projects under the program
        '''
        for p in projects:
            p.set_program(self)
        return

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF PROGRAM from the API.
        It should at least have the "ID" field.
        '''
        p = WFProgram(wf, js["ID"])
        p._init_fields(js)
        return p
