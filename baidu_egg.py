# -*- coding=utf-8 -*-
import base64
import urllib2
import urllib
import json
import wave
import time
import requests

def get_token():
    URL = 'http://openapi.baidu.com/oauth/2.0/token'
    _params = urllib.urlencode({'grant_type' : 'client_credentials',
                                'client_id' : '4G1xvWotGkLceAFm8YU5ILzp',
                                'client_secret' : '2ccfddf594113641e3e99f615b38e26a'})
    _res = urllib2.Request(URL,_params)
    _response = urllib2.urlopen(_res)
    _data = _response.read()
    _date = json.loads(_data)
    # print _date['access_token']
    return _date["access_token"]

def wav_to_text(wav_file):
    print '开始解析'
    try:
        wav_file = open(wav_file,'rb')
    except IOError:
        print u'文件错误...'
        return
    wav_file = wave.open(wav_file)
    n_frames = wav_file.getnframes()
    # print n_frames
    frame_rate = wav_file.getframerate()
    # print n_frames,frame_rate
    # if n_frames != 1 :
    #     print u'不符合格式'
    #     return
    audio = wav_file.readframes(n_frames)
    # print audio
    seconds = n_frames/frame_rate + 1
    # print seconds
    minute = seconds / 10 + 1

    for i in range(0,minute):
        # print 'cc:',frame_rate
        sub_audio = audio[i * 10 * frame_rate : (i + 1) * 10 * frame_rate]

        # 转码成base64
        base_data = base64.b64encode(sub_audio).encode('utf-8')
        data = {'format' : 'wav',
                'token' : get_token(),
                'len' : len(sub_audio),
                'rate' : frame_rate,
                'speech' : base_data,
                'cuid' : 'B8-AC-6F-2D-7A-9527',
                'channel' : 1,
                'lan' : 'zh'
                }
        # data = json.dumps(data)

        # res = urllib2.Request('http://vop.baidu.com/server_api',
        #                       data,
        #                       {'content-type' : 'application/json'})
        time.sleep(5)
        # response = urllib2.urlopen(res)
        headers = {'Content-type': 'application/json',
                   'Content-length': str(len(str(data)))}
        response = requests.post('http://vop.baidu.com/server_api', headers=headers, json=data)
        # print response
        res_data = response.text
        # res_data = res_data.decode('utf8')
        result = response.json()
        try:
            # print type(result['result'])
            #print str.decode(str(result['result'][0]),'utf-8')
            r = (result['result'])[0]
            print r
            # print res_data
        except Exception:
            pass
        # print res_data['result'][0]
    print '解析完成...'


if __name__ == '__main__':
   wav_to_text('test3.wav')
