# -*- coding:utf8 -*-
import requests
import os
import json
import time
import uuid
import base64

class API(object):

    def __init__(self):
        dic = {
            'hello':'欢迎使用语音播放',
            'error':'识别错误',
        }
        for key in dic:
            self.txt2audio(dic[key],key)
            if key == 'hello':
                self.play(key)
        pass

    def get_token(self):

        token = None
        if os.path.exists('token'):
            file = open('token','r')
            token = file.read()
            file.close()


            if json.loads(token)['expires'] < time.time():
                token = self.req_token()
            else:
                print "load cache token"
            pass
        else:
            token = self.req_token()

        return json.loads(token)['access_token']

    def req_token(self):
        print "request new token"
        token = None
        url = 'https://openapi.baidu.com/oauth/2.0/token'
        key = 'ZEzwlE2gipnqoE3jqiCKN7SN'
        secret = 'KOyWkyE57qWnDnFoc5afwIk0zBMw2X1p'
        payload = {'grant_type':'client_credentials',
                   'client_id':key,
                   'client_secret':secret}

        r = requests.post(url,data=payload)
        token = r.text
        jtoken = json.loads(token)
        jtoken['expires'] = jtoken['expires_in'] + time.time()
        token = json.dumps(jtoken)

        file = open('token','w')
        file.write(token)
        file.close()
        return token


    def txt2audio(self,txt,audio='tmp'):
        access_token = self.get_token()
        url = "http://tsn.baidu.com/text2audio"
        payload = {
            'tex':txt,
            'lan':'zh',
            'tok':access_token,
            'ctp':1,
            'cuid':uuid.UUID(int = uuid.getnode()).hex,
            'spd':5,
            'pit':8,
            'vol':9,
            'per':1,
        }

        r = requests.post(url,payload)

        if r.headers['Content-Type'] == 'audio/mp3':
            file = open(audio + '.mp3','w')
            file.write(r.content)
            file.close()

        else:
            self.play('error')
            print r.text
        pass

    def audio2txt(self,file='rec'):
        access_token = self.get_token()
        url="http://vop.baidu.com/server_api"

        self.txt2audio('请说:')
        self.play('tmp')

        os.system('arecord --duration=2 -c 1 --device=plughw:1,0 -f S16_LE -t wav -v  --rate=16000 ' + file + '.wav')

        f = open(file + '.wav','r')
        sound = f.read()
        f.close()

        payload = {
        'format':'wav',
        'rate':16000,
        'channel':1,
        'cuid':uuid.UUID(int = uuid.getnode()).hex,
        'token':access_token,
        'lan':'zh',
        'speech':base64.b64encode(sound),
        'len':len(sound),

        }
        header = {'Content-Type':'application/json'}


        r = requests.post(url,data=json.dumps(payload),headers=header)
        print r.text
	jret = json.loads(r.text)
	if jret.has_key('result'):
        	ret = json.loads(r.text)['result'][0].split(',')[0]
        else:
		ret = ""
	return ret
        pass

    def play(self,file='tmp'):
        # can not play the mp3 by aplay
        # os.system("aplay " + file + ".mp3")
        os.system("mpg321 " + file + ".mp3")
        pass

