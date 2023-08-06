from workfront.objects.codes import WFObjCode
from workfront.objects.generic_object_param_value import WFParamValuesObject


class WFTemplateTask(WFParamValuesObject):

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of a template task
        '''
        super(WFTemplateTask, self).__init__(wf, WFObjCode.templat_task, idd)

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF TEMPLATE TASK from the API.
        It should at least have the "ID" field.
        '''
        tt = WFTemplateTask(wf, js["ID"])
        tt._init_fields(js)
        return tt
