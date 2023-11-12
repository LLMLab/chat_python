import requests
import base64

def pp_human_seg_v2(img_path):
  url = 'https://aistudio.baidu.com/serving/app/3/run/predict/'
  headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,pt-BR;q=0.8,pt;q=0.7,ja;q=0.6,vi;q=0.5,en;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'jsdk-uuid=491230ca-95f9-46df-829c-2ed15f2caa28; BIDUPSID=C8AD555290A6717D7C2ACEAD6E64F96C; PSTM=1697639877; BAIDUID=C8AD555290A6717D7C2ACEAD6E64F96C:SL=0:NR=10:FG=1; Hm_lvt_6b7a9d245c3be48de953790e7b6aea6b=1697640775; MCITY=-179%3A; match-invite-ticket=; ai-studio-lc=zh_CN; __cas__st__533=NLI; __cas__id__533=0; __cas__rn__=0; Hm_up_6b7a9d245c3be48de953790e7b6aea6b=%7B%22user_reg_date%22%3A%7B%22value%22%3A%2220181127%22%2C%22scope%22%3A1%7D%2C%22user_course_rt%22%3A%7B%22value%22%3A%22%E9%9D%9E%E8%AF%BE%E7%A8%8B%E7%94%A8%E6%88%B7%22%2C%22scope%22%3A1%7D%2C%22user_center_type%22%3A%7B%22value%22%3A%223%22%2C%22scope%22%3A1%7D%7D; H_PS_PSSID=39635; BAIDUID_BFESS=C8AD555290A6717D7C2ACEAD6E64F96C:SL=0:NR=10:FG=1; delPer=0; PSINO=5; ZFY=cmclCyQVpGBbRg2s8tzpFTNXZZipwfj2guSdvAAmybQ:C; log_first_time=1699715327305; log_last_time=1699716913445; JSESSIONID=ABE0A131F571898B2074D1F1B5605233; BDUSS=plaUZQc28yTDZUejB4MjZTa2NsdEluNlVWSERGS2FRcVBYd0hKWHBaLVNPbmRsSUFBQUFBJCQAAAAAAAAAAAEAAAA9y8Qv0ruw2cHjsMvWu8zhxKoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKtT2WSrU9lTF; BDUSS_BFESS=plaUZQc28yTDZUejB4MjZTa2NsdEluNlVWSERGS2FRcVBYd0hKWHBaLVNPbmRsSUFBQUFBJCQAAAAAAAAAAAEAAAA9y8Qv0ruw2cHjsMvWu8zhxKoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKtT2WSrU9lTF; BAIDU_WISE_UID=wapp_1699763521436_289; arialoadData=false; RT="z=1&dm=baidu.com&si=a96a7287-5b16-4e03-9e89-839f47600cb0&ss=louzb9xg&sl=2&tt=4tw&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=6af&ul=c4ss&hd=c4tg"; ai-studio-ticket=38C84D8C839A429FBA6E7A646828562D017918A354AB4ABA9D31A726F858A7F5; lang=zh; Hm_lpvt_6b7a9d245c3be48de953790e7b6aea6b=1699768837',
    'Origin': 'https://aistudio.baidu.com',
    'Referer': 'https://aistudio.baidu.com/serving/app/3/?__theme=light',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
  }
  img = open(img_path, 'rb').read()
  base64_jpg_prefix = 'data:image/jpeg;base64,'
  base64_png_prefix = 'data:image/png;base64,'
  # 转换为base64
  img_base64 = base64_jpg_prefix + base64.b64encode(img).decode('utf-8')
  result = requests.post(url, headers=headers, json={"fn_index":0,"data":[img_base64]})
  out_img_base64 = result.json()['data'][0].replace(base64_png_prefix, '')
  # 转为图片
  out_img = base64.b64decode(out_img_base64)
  open('out.png', 'wb').write(out_img)
  return 'out.png'

def pp_tts(text):
  url = 'https://aistudio.baidu.com/serving/app/10/run/predict/'
  headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,pt-BR;q=0.8,pt;q=0.7,ja;q=0.6,vi;q=0.5,en;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Cookie': 'jsdk-uuid=491230ca-95f9-46df-829c-2ed15f2caa28; BIDUPSID=C8AD555290A6717D7C2ACEAD6E64F96C; PSTM=1697639877; BAIDUID=C8AD555290A6717D7C2ACEAD6E64F96C:SL=0:NR=10:FG=1; Hm_lvt_6b7a9d245c3be48de953790e7b6aea6b=1697640775; MCITY=-179%3A; match-invite-ticket=; ai-studio-lc=zh_CN; __cas__st__533=NLI; __cas__id__533=0; __cas__rn__=0; Hm_up_6b7a9d245c3be48de953790e7b6aea6b=%7B%22user_reg_date%22%3A%7B%22value%22%3A%2220181127%22%2C%22scope%22%3A1%7D%2C%22user_course_rt%22%3A%7B%22value%22%3A%22%E9%9D%9E%E8%AF%BE%E7%A8%8B%E7%94%A8%E6%88%B7%22%2C%22scope%22%3A1%7D%2C%22user_center_type%22%3A%7B%22value%22%3A%223%22%2C%22scope%22%3A1%7D%7D; H_PS_PSSID=39635; BAIDUID_BFESS=C8AD555290A6717D7C2ACEAD6E64F96C:SL=0:NR=10:FG=1; delPer=0; PSINO=5; ZFY=cmclCyQVpGBbRg2s8tzpFTNXZZipwfj2guSdvAAmybQ:C; log_first_time=1699715327305; log_last_time=1699716913445; BDUSS=plaUZQc28yTDZUejB4MjZTa2NsdEluNlVWSERGS2FRcVBYd0hKWHBaLVNPbmRsSUFBQUFBJCQAAAAAAAAAAAEAAAA9y8Qv0ruw2cHjsMvWu8zhxKoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKtT2WSrU9lTF; BDUSS_BFESS=plaUZQc28yTDZUejB4MjZTa2NsdEluNlVWSERGS2FRcVBYd0hKWHBaLVNPbmRsSUFBQUFBJCQAAAAAAAAAAAEAAAA9y8Qv0ruw2cHjsMvWu8zhxKoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJKtT2WSrU9lTF; BAIDU_WISE_UID=wapp_1699763521436_289; arialoadData=false; ai-studio-ticket=38C84D8C839A429FBA6E7A646828562D017918A354AB4ABA9D31A726F858A7F5; lang=zh; JSESSIONID=8A68F03E9E315C0F2D5D0FE150FFB4A0; RT="z=1&dm=baidu.com&si=a96a7287-5b16-4e03-9e89-839f47600cb0&ss=lovlodpc&sl=a&tt=e2v&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=19t4&ul=1ct3&hd=1ct6"; BA_HECTOR=210gal8hag048ka12h0h8gak1il1ttu1r; Hm_lpvt_6b7a9d245c3be48de953790e7b6aea6b=1699807858',
    'Origin': 'https://aistudio.baidu.com',
    'Referer': 'https://aistudio.baidu.com/serving/app/10/?__theme=light',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
  }
  
  result = requests.post(url, headers=headers, json={"fn_index":0,"data":[text],"session_hash":"5429as3korl"})
  # 下载音频
  out_name = result.json()['data'][0]['name']
  url = 'https://aistudio.baidu.com/serving/app/10/file=' + out_name
  result = requests.get(url, headers=headers)
  open('out.wav', 'wb').write(result.content)
  return 'out.wav'

functions = [
    {
        'name': 'pp_human_seg_v2',
        'description': "人像分割，把人扣出来，背景透明",
        'parameters': {
            'type': 'object',
            'properties': {
                'img_path': {
                    'type': 'string',
                    'description': "图片路径",
                },
            },
            'required': [
                'img_path',
            ],
        },
        'responses': {
            'type': 'object',
            'properties': {
                'img_path': {
                    'type': 'string',
                    'description': "图片路径",
                },
            },
        },
    },
    {
        'name': 'pp_tts',
        'description': "文字转语音",
        'parameters': {
            'type': 'object',
            'properties': {
                'text': {
                    'type': 'string',
                    'description': "待转换的文字",
                },
            },
            'required': [
                'text',
            ],
        },
        'responses': {
            'type': 'object',
            'properties': {
                'wav_path': {
                    'type': 'string',
                    'description': "音频路径",
                },
            },
        },
    },
]

if __name__ == '__main__':
  # pp_human_seg_v2('img/human.jpg')
  pp_tts('今天天气怎么样')
