from flask import Flask, render_template, request, send_from_directory
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    target_path = "./downloads"
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=target_path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        filename = os.path.basename(new_file)
        return send_from_directory(directory=target_path, path=filename, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    
