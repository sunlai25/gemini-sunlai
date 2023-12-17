import pathlib
import textwrap
import google.generativeai as genai
# Used to securely store your API key
from google.colab import userdata
from IPython.display import display
from IPython.display import Markdown
from flask import Flask, render_template, request
from pyngrok import ngrok
import threading
app = Flask(__name__)

# 配置和生成内容的函数，使用生成模型
def generate_content(input_text):
    # 在这里使用你的API密钥
    GOOGLE_API_KEY = environ['使用你自己的key']
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input_text)
    return response.text

# 将文本转换为Markdown的函数。作废，使用它转换的数据不能被http渲染。
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_text = request.form['input_text']
        response_text = generate_content(input_text)
        response_markdown = to_markdown(response_text)
        return render_template('index.html', response=response_text)

    return render_template('index.html', response="请在上面提出问题，并执行。")

ngrok_token = "使用你自己的key"
# 设置ngrok身份验证令牌
ngrok.set_auth_token(ngrok_token)
port = 5000 
def start_ngrok():
    public_url = ngrok.connect(port)
    print(' * ngrok tunnel "', public_url, '" -> "http://127.0.0.1:{}/"'.format(port))

# 在新线程中运行ngrok，以防止阻塞主线程
threading.Thread(target=start_ngrok).start()
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=port)
