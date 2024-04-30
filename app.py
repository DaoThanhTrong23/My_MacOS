from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

# Lưu trữ ghi chú và hình ảnh
notes = []
images = []

# Thiết lập thư mục cho các tệp tải lên
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'note' in request.form:
            note = request.form['note']
            if note:
                notes.append(note)
        elif 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
                image.save(image_path)
                images.append(image.filename)
        return redirect(url_for('index'))
    return render_template('index.html', notes=notes, images=images)

@app.route('/delete_note/<int:index>', methods=['POST'])
def delete_note(index):
    try:
        notes.pop(index)
    except IndexError:
        pass
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete_image/<filename>', methods=['POST'])
def delete_image(filename):
    if filename in images:
        images.remove(filename)
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
