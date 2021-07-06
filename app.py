
from flask import Flask, jsonify, request, render_template
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)  # creating the Flask class object
CORS(app)

data = json.loads(open('data.json', encoding="utf8").read())


@app.route("/", methods=['GET', 'POST'])
# @cross_origin()
def hello():
    return jsonify({"key": "home page value"})


# creating a url dynamically
@app.route('/test/<name>')
# @cross_origin()
def hello_test(name):

    # dec_msg is the real question asked by the user
    response = jsonify({"key": name})

    return response

# post - create a new book data


@app.route("/saveItems", methods=['POST'])
def storeData():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pdate = request.form['pdate']
        tags = request.form['tags']
    else:
        title = request.args.get('title')
        author = request.args.get('author')
        pdate = request.args.get('pdate')
        tags = request.args.get('tags')

    try:
        '''Appending Data Items to a json file'''
        tags = tags.split(",")
        data = {}

        with open('data.json', 'r') as file:
            json_data = file.read()
            json_data = json.loads(json_data)

        # Generating ID
        nth_books = json_data['books']
        len_books = len(nth_books)
        _genID = len_books + 1

        # Reconstructing incoming data to json dict
        data = {
            "id": f"{_genID}",
            "title": f"{title}",
            "author": f"{author}",
            "pdate": f"{pdate}",
            "tags": tags
        }

        # Appending data to file
        with open('data.json', 'w') as file:
            json_data['books'].append(data)
            json.dump(json_data, file, indent=4)
        return jsonify({"success": "values stored successfully!"})
    except:
        return jsonify({"error": "Some error occured!"})


# book searching - backend
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

# display all

@app.route("/displayall", methods=['GET', 'POST'])
def DisplayAll():
    # object list
    list1 = []

    check_list = []
    for element in data["books"]:

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
        #print('id to insert in json response')
        #print(element['id'])
        dict_obj.add("id", element["id"])
        dict_obj.add("title", element["title"])
        dict_obj.add("author", element["author"])
        dict_obj.add("pdate", element["pdate"])
        #print("dictionary : ", dict_obj)
        list1.append(dict_obj)
        check_list.append(element["id"])
        #print("list1 now : ", list1)
        # break

    # final dictionary
    final_book_dict = {"books": list1}

    print("final book_dictionary : ", final_book_dict)

    # convert into JSON:
    json_send = json.dumps(final_book_dict)

    return json_send


# # test
# x = DisplayAll()
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
# @cross_origin()
def hello_name(name):

    # dec_msg is the real question asked by the user
    dec_msg = decrypt(name)

    response = findBook(dec_msg)

    # creating a json object

    return response


if __name__ == '__main__':
    app.run(debug=True)

'''methods=['GET'],['POST']'''
