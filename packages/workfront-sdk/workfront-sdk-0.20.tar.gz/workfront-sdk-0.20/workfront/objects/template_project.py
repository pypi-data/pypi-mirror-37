from workfront.objects.codes import WFObjCode
from workfront.objects.generic_object_param_value import WFParamValuesObject
from workfront.exceptions import raise_if_not_ok, WFException


class WFTemplateProject(WFParamValuesObject):

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of a template project
        '''
        super(WFTemplateProject, self).__init__(wf, WFObjCode.templat_project,
                                                idd)

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF TEMPLATE PROJECT from the API.
        It should at least have the "ID" field.
        '''
        tp = WFTemplateProject(wf, js["ID"])
        tp._init_fields(js)
        return tp

    @staticmethod
    def from_name(wf, name):
        '''
        @param wf: A Workfront service object
        @param name: A json object of a WF TEMPLATE TASK from the API.
        It should at least have the "ID" field.
        '''
        r = wf.search_objects(WFObjCode.templat_project, {"name": name})
        raise_if_not_ok(r, WFObjCode.templat_project)

        data = r.json()["data"]
        if len(data) == 0:
            raise WFException("Template Project not found for name %s" % name)
        return WFTemplateProject.create_from_js(wf, data[0])
