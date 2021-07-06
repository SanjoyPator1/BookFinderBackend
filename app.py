
from flask import Flask, jsonify
import json

app = Flask(__name__)  # creating the Flask class object

data = json.loads(open('data.json', encoding="utf8").read())


@app.route("/", methods=['GET', 'POST'])
def hello():
    return jsonify({"key": "home page value"})



    


#book searching - backend
def sendJson(id_list):
    # object list
    list1 = []

    check_list = []
    for element in data["books"]:
        for id in id_list:
            if id == element["id"] and id not in check_list:
                print("if condition fulfilled")

                class my_dict(dict):
                    # __init__ function
                    def __init__(self):
                        self = dict()
                # Function to add key:value

                    def add(self, key, value):
                        self[key] = value
                # Main Function
                dict_obj = my_dict()

                print('id to insert in json response')
                print(element['id'])
                dict_obj.add("id", element["id"])
                dict_obj.add("title", element["title"])
                dict_obj.add("author", element["author"])
                dict_obj.add("pdate", element["pdate"])

                print("dictionary : ", dict_obj)
                list1.append(dict_obj)
                check_list.append(element["id"])
                print("list1 now : ", list1)
                # break
            else:
                print('not there')

    # final dictionary
    final_book_dict = {"books": list1}

    print("final book_dictionary : ", final_book_dict)

    # convert into JSON:
    json_send = json.dumps(final_book_dict)

    return json_send


# # test
# lis = ["2"]
# x = sendJson(lis)
# print("x value: ", x)


def findBook(name):
    string = name
    name = string.lower()
    print("lower name: ", name)

    id_list = []

    for element in data["books"]:
        for tag in element["tags"]:
            if tag == name:
                print('there')
                print(element['id'])
                if element['id'] not in id_list:
                    id_list.append(element['id'])
                # break
            else:
                print('not there')
    json_response = sendJson(id_list)
    
    return json_response


# function to replace '+' character with ' ' spaces
def decrypt(msg):

    string = msg

    # converting back '+' character back into ' ' spaces
    # new_string is the normal message with spaces that was sent by the user
    new_string = string.replace("+", " ")

    return new_string


# creating a url dynamically
@app.route('/home/<name>')
def hello_name(name):

    # dec_msg is the real question asked by the user
    dec_msg = decrypt(name)

    response = findBook(dec_msg)

    # creating a json object
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(debug=True)

'''methods=['GET'],['POST']'''
