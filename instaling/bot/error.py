# technicly not error, just state
class SessionEnd(Exception):
    pass


# propbaly some endpoint has changed
class BadStudentIdUrlError(Exception):
    pass


# bad answer is in josn
class BadAnswerError(Exception):
    pass


# error occured when sending answer
class SendAnswerError(Exception):
    pass


# error when logging in
class LoginError(Exception):
    pass
