import os

dirname = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(dirname, "resources/access_token")

try:
    access_token = open(filepath).readline()
except FileNotFoundError:
    info_message = """You now have to provide an access token to be able to run API methods.
To do so, one may add a file named 'access_token' with a string containing his app's access token to resources folder of the project
How to obtain access_token: https://vk.com/dev/access_token
"""
    print(info_message)
    access_token = str(input("Insert your access_token manually: "))
