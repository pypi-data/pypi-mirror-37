
class WFTaskStatus:
    '''
    @summary: Possible status of a task.
    '''
    new = "NEW"
    in_progress = "INP"
    complete = "CPL"
    failure = "FLR"
    ready_to_start = "RTS"
    cancelled = "CNL"


class WFProjectStatus:
    '''
    @summary: Possible status of a project.
    '''
    planning = "PLN"
    on_hold = "ONH"
    in_progress = "CUR"
    cancelled = "DED"
    rejected = "REJ"
    complete = "CPL"
