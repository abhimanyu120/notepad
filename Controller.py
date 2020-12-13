import Model
class Controller:
    def __init__(self):
        self.model=Model.Model()
    def save_file(self,msg,url):
        self.model.save_file(msg,url)
    def save_as(self,msg,url):
        self.model.save_as(msg,url)
    def read_file(self,url):
        result=self.model.read_file(url)
        return result
    def saysomething(self):
        self.takeAudio=self.model.takeQuery()
        return self.takeAudio