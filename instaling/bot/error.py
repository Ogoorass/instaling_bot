# technicly not error, just state
class SessionEnd(Exception):
    pass

# propbaly some endpoint has changed
class BadStudentIdUrlError(Exception):
    pass

# bad answer is in josn
class BadAnswerError(Exception):
    pass