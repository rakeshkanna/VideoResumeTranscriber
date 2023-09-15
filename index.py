from flask import Flask,request
import Transcriber as transcriber
app = Flask(__name__)
@app.route('/Transcribe',methods=['POST','Get'])
def Transcribe(path):
    return transcriber.transcribeVideoFile(request.form[path])


@app.route('/GenerateEntity',methods=['POST','Get'])
def GenerateEntity(text):
    return transcriber.IdentifyCustomEntities(request.form[text])

if __name__ == "__main__":
    app.run(debug=True)