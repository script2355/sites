from flask import Flask, request, render_template, send_file
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <h2>Gerador de Vídeo Simples</h2>
    <form method="POST" action="/gerar" enctype="multipart/form-data">
      Texto para destaque:<br>
      <input type="text" name="texto" required><br><br>
      Upload da imagem (PNG/JPG):<br>
      <input type="file" name="imagem" accept="image/*" required><br><br>
      <button type="submit">Gerar Vídeo</button>
    </form>
    '''

@app.route('/gerar', methods=['POST'])
def gerar():
    texto = request.form['texto']
    imagem = request.files['imagem']

    # Salvar imagem temporariamente
    img_path = "temp_img.png"
    imagem.save(img_path)

    # Criar clipe da imagem (5 segundos)
    clip_img = ImageClip(img_path).set_duration(5)

    # Criar clipe do texto
    clip_text = TextClip(texto, fontsize=70, color='white', bg_color='black').set_duration(5).set_position('center')

    # Combinar os clipes
    video = CompositeVideoClip([clip_img, clip_text])

    output_path = "video_gerado.mp4"
    video.write_videofile(output_path, fps=24)

    # Apagar imagem temporária
    os.remove(img_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
