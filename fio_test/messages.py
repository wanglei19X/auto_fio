from Path import Paths

class Messages:
    
    def __init__(self):
        self.messsagespath = "messages.log"
    
    def savemessages(self, date, messages, statu, case):
        with open(self.messsagespath, "a+") as f:
            f.write(f'{date} {statu} {messages} {case}\n')

#mess = Messages()
#mess.savemessages("2021-2-20-10:40", "file not find", "error")
