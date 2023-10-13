import gradio as gr
from main import chat_python
import os

def quickstart(name=[], need=''):
    if not name:
        name = []
    input_files = [f.name for f in name]
    answer, files = chat_python(input_files, need)
    return answer, files

cur_dir = os.path.dirname(os.path.abspath(__file__))

# 支持上传任意文件
demo = gr.Interface(
    title='chat_python（一句话处理文件）',
    description='底层LLM来自文心一言erniebot，通过对话生成python代码，用于处理任意文件。每次返回平均10s，如果没有结果就是代码出错了，可以再次尝试或者调整处理要求后再次尝试，欢迎留言交流♥',
    fn=quickstart,
    inputs=[gr.File(label="输入文件", file_count="multiple"), gr.inputs.Textbox(label="处理要求", type="text")],
    outputs=[gr.outputs.Textbox(label="处理结果", type="text"), gr.File(label="输出文件", file_count="multiple")],
    examples=[
      [[f'{cur_dir}/assets/60223956_p0.png', f'{cur_dir}/assets/animals-05.f3ffaf95.png'], '把图片缩放到200x200'],
      [[f'{cur_dir}/assets/85771697026152.zip'], '解压这个文件'],
      [[f'{cur_dir}/assets/T20_02.wav'], '裁剪到10s内'],
      [[f'{cur_dir}/assets/T20_02.wav'], '转成mp3格式'],
      [[f'{cur_dir}/assets/demo.txt'], '按换行符切分成多份文件'],
      [[f'{cur_dir}/assets/167500466772289.mp3', f'{cur_dir}/assets/output.mp4'], '把音频变成该视频的背景音乐'],
      # [[f'{cur_dir}/assets/60223956_p0.png', f'{cur_dir}/assets/animals-05.f3ffaf95.png'], '在每张图下面写上这张图的尺寸'],
    ]
)



# 处理文件，输出文件


demo.launch()
