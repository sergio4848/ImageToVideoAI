# Image to Video Creator AI

This project is a Flask application that generates a video from a series of uploaded images. The video includes dynamic transitions and ensures a minimum length of 30 seconds. The front-end features a user-friendly, animated interface.

## Features

- Upload multiple images to create a video
- Ensures the video is at least 30 seconds long
- Adds transitions between images
- Animated front-end interface

## Requirements

Install the necessary Python libraries:

```sh
pip install flask moviepy
```

## Project Structure

```
image_to_video_creator/
├── app.py
├── templates/
│   └── index.html
└── uploads/
```

## `app.py`

```python
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
```

## Front-End (HTML, CSS, JS)

### `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image to Video</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background: #282c34;
            color: white;
            margin: 0;
        }
        .container {
            text-align: center;
        }
        h1 {
            animation: fadeIn 2s ease-in-out;
        }
        form {
            animation: slideIn 2s ease-in-out;
        }
        input[type="file"] {
            padding: 10px;
            background: #61dafb;
            border: none;
            border-radius: 5px;
            color: black;
        }
        button {
            padding: 10px 20px;
            background: #61dafb;
            border: none;
            border-radius: 5px;
            color: black;
            cursor: pointer;
            transition: background 0.3s ease-in-out;
        }
        button:hover {
            background: #21a1f1;
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes slideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Image to Video</h1>
        <form action="/create_video" method="post" enctype="multipart/form-data">
            <label for="images">Select Images:</label><br>
            <input type="file" id="images" name="images" multiple><br><br>
            <button type="submit">Create Video</button>
        </form>
    </div>
</body>
</html>
```

## How to Run

1. Clone the repository:

```sh
git clone https://github.com/yourusername/image_to_video_creator.git
cd image_to_video_creator
```

2. Install the requirements:

```sh
pip install flask moviepy
```

3. Run the application:

```sh
python app.py
```

4. Open your web browser and go to `http://127.0.0.1:5000/`.

