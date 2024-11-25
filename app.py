from flask import Flask, render_template, Response, request, redirect, url_for
from gender_detection import analyze_video

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_stream', methods=['POST'])
def start_stream():
    video_type = request.form.get('type')
    if video_type == 'webcam':
        return redirect(url_for('webcam_page'))  # Redirect to webcam page
    elif video_type == 'ip':
        ip = request.form.get('ip')
        username = request.form.get('username')
        password = request.form.get('password')
        return redirect(url_for('ip_stream_page', ip=ip, username=username, password=password))
    else:
        return "Invalid option selected", 400

@app.route('/webcam')
def webcam_page():
    return render_template('webcam.html')

@app.route('/ip_stream')
def ip_stream_page():
    ip = request.args.get('ip')
    username = request.args.get('username')
    password = request.args.get('password')
    return render_template('ip_stream.html', ip=ip, username=username, password=password)

@app.route('/video_feed')
def video_feed():
    video_type = request.args.get('type')
    if video_type == 'webcam':
        video_source = 0  # Webcam source
    elif video_type == 'ip':
        ip = request.args.get('ip')
        username = request.args.get('username')
        password = request.args.get('password')
        video_source = f"rtsp://{username}:{password}@{ip}/"  # IP camera stream
    else:
        return "Invalid video type", 400

    return Response(analyze_video(video_source), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
