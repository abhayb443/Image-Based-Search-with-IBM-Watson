import json
from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import Flask, render_template
import httplib2


def image_search():
    IBM_API_KEY = 'g1n50O5_I0sRiJGkoGy7x2cwdRKgyCpc9lLF-T2zA0po'
    IBM_URL = 'https://api.us-south.visual-recognition.watson.cloud.ibm.com/instances/c0aa675b-7bdd-42b8-bd93-df6d6fc3a5ce'

    # # Passing API KEY and URL to the Visual Recognition
    authenticator = IAMAuthenticator(IBM_API_KEY)

    visual_recognition = VisualRecognitionV3(
                        version='2018-03-19',
                        authenticator=authenticator)

    visual_recognition.set_service_url(IBM_URL)

    # Running the Visual Recognition on test.img file
    with open('./static/Pepperoni-pizza.jpg', 'rb') as image:
        classes = visual_recognition.classify(images_file=image, threshold='0.6', classifier_ids='food').get_result()

    # print(json.dumps(classes, indent=2))
    output_query = classes['images'][0]['classifiers'][0]['classes'][0]['class']

    # latitude = 19.245690
    # longitude = 73.140822
    latitude = 12.959111
    longitude = 77.732022

    return latitude, longitude, output_query


def nearby_places(latitude, longitude, query):
    rest_api = '8HnOw70LjqOg4ARPX4pt1OOvP6_H4b_GA2uSWIFtO0A'
    app_id = 'sXPR28hTcgrpcSHY25rI'
    url = ('https://places.ls.hereapi.com/places/v1/suggest?at={0}%2C{1}&q={2}&apiKey={3}'.format(latitude, longitude,
                                                                                                  query, rest_api))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    for i in result.items():
        res = i

    res_key = res[0]
    res_value = res[1]

    return res_key, res_value


app = Flask(__name__)

@app.route('/')
def map_func():
    app_id = '2Q82XD6Ywh5sLlJQtON4'
    app_pass = 'bJLB7QNPh83pVJFnBhBcv3vk1UN-z5QAxUaTEAaWMUc'
    return render_template('Home.html', latitude=latitude, longitude=longitude,
                           output_query=query, res_key=res_key, res_value=res_value)


if __name__ == '__main__':
    latitude, longitude, query = image_search()
    res_key, res_value = nearby_places(latitude, longitude, query)
    print(res_key)
    print(res_value)
    app.run(debug=True)