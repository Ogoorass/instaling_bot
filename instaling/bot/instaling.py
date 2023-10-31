from requests import Session
from time import time
import json

from .data import Url, Header, Data
from .utils import extract_student_id_from_url
from .error import SessionEnd
from .answer import Answer

class Instaling:
    def __init__(self,
        login,
        passwd):
        self.login = login
        self.passwd = passwd

        # setup
        self.session = Session()
        self.session.headers.update(Header.default)

        # inicjalizacja połączenia
        init_request = self.session.get(Url.init)
        
        # logowanie
        login_request = self.session.post(Url.login, data=Data.login(login=self.login, passwd=self.passwd))

        # get student id from url, can raise an BadStudentIdUrlError
        self.student_id = extract_student_id_from_url(login_request.url)


    def generate_new_word(self) -> str:
        # request for new word and return it it
        #request o kolejne słówko, użwany także do zakończenia sesji
        next_word_request = self.session.post(
            Url.next_word, 
            data= Data.next_word(
                student_id=self.student_id, 
                time=int(time())
            )
        )


        # wydobywanie pytania i tłumaczenia ze storny
        # jeżeli nie ma tych wartości to znaczy, że sesja została skończona
        # raise error (e.g. SessionEndError) when session is finished
        try:
            usage_example = json.loads(next_word_request.text)['usage_example']
            self.word_id = json.loads(next_word_request.text)['id']
        except KeyError:
            raise SessionEnd
        
        return usage_example

    def send_answer(self, answer) -> Answer:
        
        # send answer
        answer_request = self.session.post(
            Url.answer, 
            data=Data.answer(
                answer= answer,
                student_id= self.student_id,
                word_id= self.word_id
            )
        )

        answer_data = json.loads(answer_request.text)

        return Answer(
            word= answer_data['word'],
            isCorrect= answer_data['grade']
        )
    
    def logout(self):
        # wyloguj się
        logout_request = self.session.get(Url.logout)
