import erniebot
import re
import os
import requests
import json
import shutil
import subprocess
import src.func.aistudio as aistudio
import numpy as np

erniebot.api_type = 'aistudio'
erniebot.access_token = '3c410ce131fe8d246c47e26fdf932cfd44e95aa8'

functions = aistudio.functions
f_descriptions = [f['description'] for f in functions]
def get_embs(texts):
  response = erniebot.Embedding.create(
      model='ernie-text-embedding',
      input=texts)
  embs = [np.array(embedding) for embedding in response.get_result()]
  embs = np.array(embs)
  return embs

f_embs = get_embs(f_descriptions)

def get_sim_emb(emb, embs):
  sim = np.dot(emb, embs.T)
  sim = np.max(sim, axis=1)
  return sim[0]

def chat(msg, history=[], functions=[]):
  response = erniebot.ChatCompletion.create(
      model='ernie-bot',
      # model='ernie-bot-4',
      messages=[*history, {'role': 'user', 'content': msg}],
      functions=functions,
  )
  if functions:
    if hasattr(response, 'function_call'):
      return response.function_call
    return None
  return response.result

def chat_python(file, need):
  os.chdir(f'.')
  if not os.path.exists('temp'):
    os.mkdir('temp')
  id = len(os.listdir('temp'))
  id += 1
  print(f'【id_{id}】start------------------', flush=True)
  print(f'【id_{id}】file:', file, flush=True)
  print(f'【id_{id}】need:', need, flush=True)
  if type(file) == str:
    file = [file]
  msg_temp = '你是一个优秀的python代码解释器，请生成一段可直接运行的python代码，用于处理以下文件，要求为【{need}】, 输入文件名为【{file}】，输出到新的文件里'
#   msg_temp = '''你是一个优秀的python代码解释器，以下是一些已有的可用的函数：
# def pp_human_seg_v2(img_path)：人像分割，把人扣出来，背景透明
# ---
# 请生成一段可直接运行的python代码，用于处理以下文件，要求为【{need}】, 输入文件名为【{file}】，输出到新的文件里'''
  msg = msg_temp.format(need=need, file=[f.replace('\\', '/').split('/')[-1] for f in file])
  os.makedirs(f'temp/{id}', exist_ok=True)
  [shutil.copy(f, f'temp/{id}/') for f in file]
  emb = get_embs([need])
  function_call = None
  # 和已有的函数介绍相似度大于阈值，就尝试走函数调用
  func_max_sim = get_sim_emb(emb, f_embs)
  print(f'【id_{id}】func_max_sim:', func_max_sim, flush=True)
  if func_max_sim > 0.6:
    function_call = chat(json.dumps(file)+','+need, functions=functions)
  if function_call and hasattr(aistudio, function_call['name']):
    # {'name': 'get_current_temperature', 'thoughts': '用户想要知道深圳市今天的天气情况，我可以使用get_current_temperature工具来获取这个信息。', 'arguments': '{"location":"深圳市","unit":"摄氏度"}'}
    os.chdir(f'temp/{id}')
    old_files = os.listdir('.')
    function = getattr(aistudio, function_call['name'])
    function_result = function(**json.loads(function_call['arguments']))
    answer = function_call['thoughts']
  else:
    answer = chat(msg)
    print(f'【id_{id}】answer:', answer, flush=True)
    codes = re.findall(r'```.*\n([^犭]*?)\n```', answer, flags=re.M)
    python_code = None
    for code in codes:
      if 'import' in code:
        python_code = code
    python_code = f'# 预设基础库\nimport os\nimport re\n# 生成的代码\n{python_code}' # 容易漏掉的import os
    open(f'temp/{id}/python_code.py', 'w', encoding='utf-8').write(python_code)
    open(f'temp/{id}/question.md', 'w', encoding='utf-8').write(msg)
    open(f'temp/{id}/answer.md', 'w', encoding='utf-8').write(answer)
    open(f'temp/{id}/info.json', 'w', encoding='utf-8').write(json.dumps({
      'need': need,
      'file': file,
    }, indent=2, ensure_ascii=False))
    os.chdir(f'temp/{id}')
    old_files = os.listdir('.')
    # 安装相关依赖
    install_pkg = re.findall(r'pip install ([A-Za-z- ]*)', answer, flags=re.M)
    # txt_pkg = re.findall(r'`(.*?)`', answer, flags=re.M)
    txt_pkg = []
    pkgs = install_pkg + txt_pkg
    pkgs = [pkg for pkg in pkgs if (pkg and '.' not in pkg)]
    pkgs = [pkg.replace('pip install ', '') for pkg in pkgs]
    pkgs = list(set(pkgs))
    for pkg in pkgs:
      print(f'【id_{id}】install------------------', pkg, flush=True)
      os.system(f'pip install {pkg}')
    # 执行python代码
    # os.system('python python_code.py')
    result = subprocess.run('python python_code.py', capture_output=True, text=True)
    print(f'【id_{id}】python------------------ result.returncode:', result.returncode, flush=True)
    if result.stderr:
      print(f'【id_{id}】python_err------------------', flush=True)
      print(result.stderr)
    if result.stdout:
      print(f'【id_{id}】python_out------------------', flush=True)
      print(result.stdout)
  new_files = os.listdir('.')
  new_files = [f for f in new_files if f not in old_files]
  print(f'【id_{id}】new_files:', new_files, flush=True)
  print(f'【id_{id}】end--------------------', flush=True)
  # 获取绝对路径
  new_files = [os.path.abspath(f) for f in new_files]
  _new_files = []
  for f in new_files:
    if os.path.isdir(f):
      for _f in os.listdir(f):
        _new_files.append(f'{f}/{_f}')
      continue
    _new_files.append(f)
  new_files = _new_files
      
  os.chdir(os.path.dirname(os.path.abspath(__file__)))
  return answer, new_files

if __name__ == '__main__':
  files = [
    '60223956_p0.png',
    # '167500466772289.mp3',
    ['60223956_p0.png', 'animals-05.f3ffaf95.png'],
    # '浙江工商大学432统计学考研真题参考答案2011-2020.pdf',
    # 'demo.txt',
  ]
  needs = [
    '等比例切成4张图',
    '把图片缩放到200x200',
    '裁剪出中间偏右边的200x200',
    '把图里的人扣出来，背景透明',
    '加载开源模型，人像分割，把人扣出来，背景透明',
    #  '从网络帮我找一张相似的图片',
    # '把这个音频转成wav格式',
    # '裁剪前30s',
    # '在音频开头加上高科技的音效',
    # '把这两张图片拼接成一张',
    # '把这两张图按左右拼接成一张',
    # '把这些图片转成200x200',
    # '不改变图片比例，保留原图的中间部分，把图片缩放到200x200',
    # '按图片短的一边等比例缩放到200px，然后裁剪长出来的部分，缩放到200x200的正方形',
    # '将所有图片变成暖色调',
    # '用pdfplumber把pdf里面的文字提取到一个txt中',
    # '把文本转成一段语音，并输出到mp3',
  ]
  file = files[-1]
  if type(file) == str:
    file = [file]
  file = ['assets/' + f for f in file]
  need = needs[-1]
  chat_python(file, need)
