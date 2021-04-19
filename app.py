from flask import Flask, jsonify, request,render_template, redirect
from script import Predictor
import time

app = Flask(__name__)

url_timestamp = {}
url_viewtime = {}
prev_url = ""
working_url=""

eid = ''
doj = ''
gender = 0
company = 0
wfh = 0
des = 0
URL = ''


def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url


@app.route('/', methods =["GET", "POST"])
def cfd():
    if request.method == "POST":
        global eid
        eid = request.form.get("user_name")
        global doj
        doj = request.form.get("doj")
        global gender 
        gender = int(request.form.get("gender"))
        global company 
        company= int(request.form.get("company"))
        global wfh 
        wfh = int(request.form.get("wfh"))
        global des
        des= int(request.form.get("des"))
        global URL
        URL= request.form.get("work_url")

        print(eid,doj,gender,company,wfh,des,URL)
        return redirect(request.url)

    return render_template('form.html')

Url = url_strip(URL)
resource_time=0

@app.route('/send_url', methods=['POST'])
def send_url():
    resp_json = request.get_data()
    params = resp_json.decode()
    url = params.replace("url=", "")
    print("currently viewing: " + url_strip(url))
    parent_url = url_strip(url)

    global url_timestamp
    global url_viewtime
    global prev_url
    global resource_time

    print("initial db prev tab: ", prev_url)
    print("initial db timestamp: ", url_timestamp)
    print("initial db viewtime: ", url_viewtime)

    if parent_url not in url_timestamp.keys():
        url_viewtime[parent_url] = 0

    if prev_url != '':
        time_spent = int(time.time() - url_timestamp[prev_url])
        url_viewtime[prev_url] = url_viewtime[prev_url] + time_spent

    if prev_url != '' and url==Url:
        resource_time= int(time.time() - url_timestamp[prev_url])


    x = int(time.time())
    url_timestamp[parent_url] = x
    prev_url = parent_url
    print("final timestamps: ", url_timestamp)
    print("final viewtimes: ", url_viewtime)

    return jsonify({'message': 'success!'}), 200

print([int(gender),int(company),int(wfh),int(des),int(resource_time),4.5])

@app.route('/predict')
def predict():

    int_features = [int(gender),int(company),int(wfh),int(des),int(resource_time),4.5]
    print(int_features)
    predictor = Predictor()
    prediction = predictor.predict(int_features)
    #p = model.predict_proba(final_features)
    #prediction_chances=p[0][1]

    print(prediction)


    return render_template('predict5.html',  prediction_chances=round(prediction[0], 2))

@app.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200

if __name__ == "__main__":
    app.run(debug= True)
