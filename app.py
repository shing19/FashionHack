import json,time
from flask import Flask, render_template, request, jsonify, Response
import requests
import hashlib
import os

app=Flask(__name__)

# Jiaxin setting
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


@app.route("/upload_image", methods=["POST"])
def add_picture():
    img = request.files['image']
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
            return {"filename": filename}
    return {"code": 401}


@app.route("/hello", methods=["GET", "POST"])
def hello():
    return "hello update from shing's repo"


# default setting
output=[]#("message stark","hi")]
@app.route('/')
def home_page():
    return render_template("IY_Home_page.html",result=output)
@app.route('/about')
def about_page():
    return render_template("about.html",result=output)
@app.route('/contact')
def contact_page():
    return render_template("contact.html",result=output)
@app.route('/charts')
def charts_page():
    return render_template("charts.html",result=output)

@app.route('/cam')
def sign_page():
    return render_template("camera.html")

@app.route('/result',methods=["POST","GET"])
def Result():
    if request.method=="POST":
        print(list(request.form.values()))
        result=list(request.form.values())[0]
        if result.lower()=="restart":
            output.clear()
        else:
            try:
                r = requests.post('http://13.88.218.187:5005/webhooks/rest/webhook', json={"message": result})
                print("Bot says, ")
                for i in r.json():
                    bot_message = i['text']
                    print(f"{i['text']}")
                output.extend([("message parker",result),("message stark",bot_message)])
            except:
                output.extend([("message parker", result), ("message stark", "We are unable to process your request at the moment. Please try again...")])

        print(output)
        return render_template("IY_Home_page.html",result=output)

if __name__=="__main__":
    app.run(debug=True)#,host="1.117.208.226")



