from flask import Flask, request, render_template, send_file
from moviepy.editor import ImageSequenceClip, concatenate_videoclips
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_video', methods=['POST'])
def create_video():
    images = request.files.getlist('images')
    image_paths = []

    for image in images:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
        image.save(image_path)
        image_paths.append(image_path)

    duration_per_image = max(30 / len(image_paths), 1)
    
    video_clips = []
    for image_path in image_paths:
        clip = ImageSequenceClip([image_path], fps=1)
        clip = clip.set_duration(duration_per_image)
        video_clips.append(clip)
    
    final_clip = concatenate_videoclips(video_clips, method="compose")
    video_path = 'output_video.mp4'
    final_clip.write_videofile(video_path, fps=24)

    return send_file(video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
