from os import path
from io import TextIOWrapper
import speech_recognition as s
class Model:
    def __init__(self):
        self.key="QWERTYUIOPLKJHGFDSAZXCVBNMasdfghjklpoiuytrewqzxcvbnm1234567890"
        self.offset=5
    def encrypt(self,plaintext):
        result=""
        for ch in plaintext:
            try:
              i=(self.key.index(ch)+self.offset)%len(self.key)
              result+=self.key[i]
            except ValueError:
                result+=ch
        return result
    def decrypt(self,cipertext):
        result = ""
        for ch in cipertext:
            try:
                i = (self.key.index(ch) - self.offset) % len(self.key)
                result += self.key[i]
            except ValueError:
                result += ch
        return result
    def save_file(self,msg,url):
        if type(url) is not str:
            file=url.name
        else:
            file=url
        f_name,f_extension=path.splitext(file)
        if f_extension in ".ntxt":
            msg=self.encrypt(msg)
        with open(file, "w") as fw:
            fw.write(msg)
    def save_as(self,msg,url):
        if type(url) is TextIOWrapper:
            file=url.name
        else:
            file=url
        msg = self.encrypt(msg)
        with open(file,"w") as fw:
            fw.write(msg)

    def read_file(self,url):
        f_name,f_extension=path.splitext(url)
        with open(url, "r") as fw:
            content = fw.read()
        if f_extension in ".ntxt":
            content=self.decrypt(content)

        return content,f_name+f_extension

    def takeQuery(self):
        sr = s.Recognizer()
        sr.pause_threshold = 1
        with s.Microphone() as m:
            #sr.adjust_for_ambient_noise(m)
            audio = sr.listen(m)
            query = sr.recognize_google(audio, language='eng-in')
            print(query)
            return query