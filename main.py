import erniebot
import re
import os
import requests
import json
import shutil

erniebot.api_type = 'aistudio'
erniebot.access_token = '3c410ce131fe8d246c47e26fdf932cfd44e95aa8'

def chat(msg, history=[]):
  response = erniebot.ChatCompletion.create(
      model='ernie-bot',
      messages=[*history, {'role': 'user', 'content': msg}]
  )
  return response.result

def chat_python(file, need):
  os.chdir(f'.')
  if not os.path.exists('temp'):
    os.mkdir('temp')
  id = len(os.listdir('temp'))
  if type(file) == str:
    file = [file]
  msg_temp = '你是一个优秀的python代码解释器，请生成一段可直接运行的python代码，用于处理以下文件，要求为【{need}】, 输入文件名为【{file}】，输出到新的文件里'
  msg = msg_temp.format(need=need, file=[f.replace('\\', '/').split('/')[-1] for f in file])
  answer = chat(msg)
  python_code = re.findall(r'```python\n([^犭]*?)\n```', answer, flags=re.M)[0]
  id += 1
  os.makedirs(f'temp/{id}', exist_ok=True)
  open(f'temp/{id}/python_code.py', 'w', encoding='utf-8').write(python_code)
  open(f'temp/{id}/question.md', 'w', encoding='utf-8').write(msg)
  open(f'temp/{id}/answer.md', 'w', encoding='utf-8').write(answer)
  open(f'temp/{id}/info.json', 'w', encoding='utf-8').write(json.dumps({
    'need': need,
    'file': file,
  }, indent=2, ensure_ascii=False))
  # exec(python_code)
  print(f'【id_{id}】start------------------', flush=True)
  print(f'【id_{id}】file:', file, flush=True)
  print(f'【id_{id}】need:', need, flush=True)
  print(f'【id_{id}】answer:', answer, flush=True)
  [shutil.copy(f, f'temp/{id}/') for f in file]
  os.chdir(f'temp/{id}')
  old_files = os.listdir('.')
  # 执行python代码
  os.system('python python_code.py')
  new_files = os.listdir('.')
  new_files = [f for f in new_files if f not in old_files]
  print(f'【id_{id}】new_files:', new_files, flush=True)
  print(f'【id_{id}】end--------------------', flush=True)
  # 获取绝对路径
  new_files = [os.path.abspath(f) for f in new_files]
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  return answer, new_files

if __name__ == '__main__':
  files = [
    '60223956_p0.png',
    # '167500466772289.mp3',
    ['60223956_p0.png', 'animals-05.f3ffaf95.png'],
  ]
  needs = [
    '等比例切成4张图',
    '把图片缩放到200x200',
    '裁剪出中间偏右边的200x200',
    '把图里的人扣出来，背景透明',
    #  '从网络帮我找一张相似的图片',
    # '把这个音频转成wav格式',
    # '裁剪前30s',
    # '在音频开头加上高科技的音效',
    # '把这两张图片拼接成一张',
    # '把这两张图按左右拼接成一张',
    # '把这些图片转成200x200',
    # '不改变图片比例，保留原图的中间部分，把图片缩放到200x200',
    '按图片短的一边等比例缩放到200px，然后裁剪长出来的部分，缩放到200x200的正方形',
    # '将所有图片变成暖色调',
  ]
  file = 'assets/' + files[-1]
  need = needs[-1]
  chat_python(file, need)
