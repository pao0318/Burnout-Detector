from flask import Flask, jsonify, request,render_template
import time
import  numpy as np
import pickle as pkl

app = Flask(__name__)

model = pkl.load(open('model_file.pkl', 'rb'))
url_timestamp = {}
url_viewtime = {}
prev_url = ""
working_url=""

eid=""
doj=""
gender=0
company=0
wfh=1
des=3
URL=""


def url_strip(url):
    if "http://" in url or "https://" in url:
        url = url.replace("https://", '').replace("http://", '').replace('\"', '')
    if "/" in url:
        url = url.split('/', 1)[0]
    return url


@app.route('/', methods =["GET", "POST"])
def cfd():
    if request.method == "POST":

       eid = request.form.get("user_name")

       doj = request.form.get("doj")

       gender = int(request.form.get("gender"))

       company= int(request.form.get("company"))

       wfh = int(request.form.get("wfh"))

       des= int(request.form.get("des"))

       URL= request.form.get("work_url")

       print(eid,doj,gender,company,wfh,des,URL)

    return render_template("form.html")

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

print([int(gender),int(company),int(wfh),int(des),int(resource_time),0.5])
@app.route('/predict')
def predict():

    int_features = [int(gender),int(company),int(wfh),int(des),int(resource_time),0.5]
    print(int_features)
    final_features = np.array(int_features)
    prediction = model.predict(final_features.reshape(1, -1))
    #p = model.predict_proba(final_features)
    #prediction_chances=p[0][1]

    print(prediction)


    return render_template('predict5.html',  prediction_chances=prediction)

@app.route('/quit_url', methods=['POST'])
def quit_url():
    resp_json = request.get_data()
    print("Url closed: " + resp_json.decode())
    return jsonify({'message': 'quit success!'}), 200

if __name__ == "__main__":
    app.run(debug= True)
