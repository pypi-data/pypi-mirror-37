import json

from workfront.objects.codes import WFObjCode
from workfront.objects import user
from workfront.objects.generic_object_param_value import WFParamValuesObject
import workfront.objects.project
import workfront.objects.template_task
from workfront.objects.status import WFTaskStatus


class WFTask(WFParamValuesObject):
    '''
    @summary: A Workfront Task helper class
    '''

    def __init__(self, wf, idd):
        '''
        @param wf: A Workfront service object
        @param idd: worfront id of the task
        '''
        super(WFTask, self).__init__(wf, WFObjCode.task, idd)

    def set_status(self, status):
        '''
        @summary: Hit WF to set the status of the current task.
        @param status: one of the WFTaskStatus
        '''
        r = self.wf.put_object(WFObjCode.task, self.wf_id, {"status": status})
        self._raise_if_not_ok(r)

    def get_status(self):
        '''
        @return: the status of the current task ( can be one of the
        WFTaskStatus)
        '''
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["status"])
        return r.json()["data"]["status"]

    def assign_to_user(self, user):
        '''
        @summary: Assign the current task to the given user.
        @param user: an instance of WFUser
        '''
        params = {
            "objID": user.wf_id,
            "objCode": WFObjCode.user
        }
        r = self.wf.action(WFObjCode.task, self.wf_id, "assign", params)
        self._raise_if_not_ok(r)

    def unassign_from_user(self, user):
        params = {
            "userID": user.wf_id,
        }
        r = self.wf.action(WFObjCode.task, self.wf_id, "unassign", params)
        self._raise_if_not_ok(r)

    def get_assigned_user(self):
        '''
        @return: an instance of the user (WFUser object) that is assigned to
        the current task.
        '''
        r = self.get_fields(["assignedTo:*"])

        u = user.WFUser.create_from_js(self.wf, js=r["assignedTo"])
        return u

    def get_project(self):
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["project:ID"])
        self._raise_if_not_ok(r)

        data = r.json()["data"]["project"]
        return workfront.objects.project.WFProject.create_from_js(self.wf,
                                                                  data)

    def get_parent_id(self):
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["parent"])
        self._raise_if_not_ok(r)

        return r.json()["data"]["parent"]["ID"]

    def get_parent(self):
        '''
        @return: Parent Task object
        '''
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["parent"])
        self._raise_if_not_ok(r)
        return WFTask.create_from_js(self.wf, r.json()["data"]["parent"])

    def get_project_id(self):
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["project:ID"])
        self._raise_if_not_ok(r)
        return r.json()["data"]["project"]["ID"]

    def get_portfolio_id(self):
        r = self.wf.get_object(WFObjCode.project,
                               self.get_project_id(),
                               ["portfolio:ID"])
        self._raise_if_not_ok(r)

        return r.json()["data"]["portfolio"]["ID"]

    def get_successors(self):
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["successors:*"])
        self._raise_if_not_ok(r)

        successors = r.json()["data"]["successors"]
        return [s['successorID'] for s in successors]

    def get_handoff_date(self):
        r = self.wf.get_object(WFObjCode.task, self.wf_id, ["handoffDate"])
        self._raise_if_not_ok(r)

        return r.json()["data"]["handoffDate"]

    def get_template(self):
        '''
        @return: an instance of template task from where this task was created.
        '''
        data = self.get_fields(["templateTask:ID"])["templateTask"]
        tt = workfront.objects.template_task.WFTemplateTask.create_from_js(
            self.wf, data)
        return tt

    def get_children(self):
        '''
        @return A list of dictionaries where each one contains:
        - ID : of the child task
        - name : of the child task
        '''
        r = self.get_fields(['children:ID', "children:name"])
        return r["children"]

    def reset(self):
        '''
        @summary: Set status to new for this task. Also, if it is an automatic
        task (Has the 'Automation' custom form in it), put the notify backend
        to empty (from 'ready')
        '''
        self.set_status(WFTaskStatus.new)
        if self.is_automatic():
            self.__reset_automatic()

    def is_automatic(self):
        '''
        @return: True if the task has the 'Automation' custom form.
        '''
        for cf in self.get_custom_forms():
            if cf.name == 'Automation':
                return True
        return False

    def __reset_automatic(self):
        '''
        @summary: if 'Notify backend' field from the Automation custom form is
        set to 'ready'; then change it to empaty (uncheck it).
        @precondition: is_automatic must be True
        '''
        self.set_param_values({'Notify backend': ''})

    def start_automatic(self):
        '''
        @summary: Set 'Notify backend' field from the Automation custom form to
        'ready'.
        @precondition: is_automatic must be True
        '''
        self.set_param_values({'Notify backend': 'ready'})

    @staticmethod
    def create_from_js(wf, js):
        '''
        @param wf: A Workfront service object
        @param js: A json object of a WF TASK from the API.
        It should at least have the "ID" field.
        '''
        tsk = WFTask(wf, js["ID"])
        tsk._init_fields(js)
        return tsk

    def get_cross_project_predecessors(self):
        '''
        @return: cross project predecessor task list
        '''
        res = self.get_fields([
            "predecessors:ID",
            "predecessors:predecessorType",
            "predecessors:isCP",
            "predecessors:isEnforced"])

        if 'predecessors' not in res:
            return []
        return [WFTask(self.wf, p['ID'].split('_')[0])
                for p in res['predecessors'] if p['isCP']]

    def get_predecessors(self):
        '''
        @return: a list of task predecessors
        '''
        res = self.get_fields([
            "predecessors:predecessor:ID",
            "predecessors:predecessor:name",
            "predecessors:isCP",
            "predecessors:isEnforced"])

        preds = []
        if 'predecessors' in res:
            for pred_js in res['predecessors']:
                task_js = pred_js["predecessor"]
                t = WFTask.create_from_js(self.wf, task_js)
                preds.append(t)
        return preds

    def add_predecessor(self, predecessor_task):
        '''
        @summary: add the given task as a predecessor of the current task.
        @param predecessor_task: a WFTask object
        '''
        predecessor_task_id = predecessor_task.wf_id
        current_predecessors = self.get_fields(["predecessors:*"])["predecessors"]

        # If the predecessor_task doesnt currently exists in current_predecessors -> add it
        if not any(p["predecessorID"] == predecessor_task_id for p in current_predecessors):

            new_predecessor = {"predecessorID": predecessor_task_id,
                               "predecessorType": "fs", "isEnforced": True}
            if predecessor_task.get_project().wf_id != self.get_project().wf_id:
                new_predecessor["isCP"] = True
            current_predecessors.append(new_predecessor)

            params = {"updates": json.dumps({"predecessors": current_predecessors})}
            self.wf.put_object(self.obj_code, self.wf_id, params)

    def set_parent(self, parent_task):
        '''
        @summary: The given parent task will be set as parent of the current
        task.
        @param: A WFTask object
        '''
        self.set_fields({"parentID": parent_task.wf_id})

    def remove_parent(self, ):
        '''
        @summary: Remove the parent task of the current task.
        '''
        self.set_fields({"parentID": ''})
