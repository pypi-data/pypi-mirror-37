
class WFException(Exception):
    pass


def raise_if_not_ok(resp, obj_code, wf_id="New"):
    '''
    @raise WFException: if the return status code is not 200 ok.
    @param resp: Response object.
    @param obj_code: WF object code.
    @param wf_id: WF object id if the action was perform on an existing object.
    '''
    if resp.status_code != 200:
        err = "When performing {} for object {} {}: {}\nUrl hit was {}"
        err = err.format(resp.request.method, obj_code, wf_id, resp.json(),
                         resp.request.url)
        raise WFException(err)
