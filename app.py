import json,time
from flask import Flask, render_template, request, jsonify, Response, flash, redirect, url_for, send_from_directory
import requests
import hashlib
import os
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware


PICTURE_PATH = "static/images/"
ALLOWED_EXTENSIONS = {'png', "PNG", 'jpg', "JPG", 'jpeg', "JPEG", }
CHANGE_EXTENSIONS = {
    'png': 'png',
    'PNG': 'png',
    'jpg': 'jpg',
    'JPG': 'jpg',
    'jpeg': 'jpg',
    'JPEG': 'jpg'
}
app=Flask(__name__)
app.config['PICTURE_PATH'] = PICTURE_PATH
app.add_url_rule('/uploads/<filename>', 'uploaded_file',
                 build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads':  app.config['PICTURE_PATH']
})

@app.route("/hello", methods=["GET", "POST"])
def hello():
    return "hello update from shing's repo"

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['PICTURE_PATH'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def home_page():
    return render_template("index.html",result=output)
def add_picture():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        img = request.files['image']
        if img.filename == '':
            flash('No selected file')
        if img and '.' in img.filename:
            ext = img.filename.rsplit('.', 1)[1]
            if ext in ALLOWED_EXTENSIONS:
                ext = CHANGE_EXTENSIONS[ext]
                md5 = hashlib.md5(img.read()).hexdigest()
                filename = md5 + '.' + ext
                directory = os.path.join(PICTURE_PATH, filename)
                if not os.path.isfile(directory):
                    img.seek(0)
                    img.save(directory)
                    return redirect(url_for('uploaded_file', filename=filename))
    return redirect(url_for('/', {'code':401}))

output=[]#("message stark","hi")]
@app.route('/result',methods=["POST","GET"])
def Result():
    if request.method=="POST":
        print(list(request.form.values()))
        result=list(request.form.values())[0]
        if result.lower()=="restart":
            output.clear()
        else:
            try:
                r = requests.post('http://1.117.208.226:5005/webhooks/rest/webhook', json={"message": result})
                print("Bot says, ")
                for i in r.json():
                    bot_message = i['text']
                    print(f"{i['text']}")
                output.extend([("message parker",result),("message stark",bot_message)])
            except:
                output.extend([("message parker", result), ("message stark", "We are unable to process your request at the moment. Please try again...")])

        print(output)
        return render_template("index.html",result=output)

if __name__=="__main__":
    app.run(debug=True)#,host="1.117.208.226")



