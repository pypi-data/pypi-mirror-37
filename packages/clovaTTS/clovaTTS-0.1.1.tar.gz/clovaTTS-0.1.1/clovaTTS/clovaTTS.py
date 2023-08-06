import os
import time
import urllib.request

class clovaTTS(object):
    def __init__(self, speaker_name, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.speaker_name = speaker_name

    def tts(self, text):
        return self.naver_clova_tts(text)

    def save(self, filename, speech):
        with open(filename, 'wb') as f:
            f.write(speech)

    def naver_clova_tts(self, text):
        encText = urllib.parse.quote(text)
        data = "speaker=" + self.speaker_name + "&speed=0&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", self.client_id)
        request.add_header("X-NCP-APIGW-API-KEY", self.client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            return response_body
        else:
            return None
