from http.server import BaseHTTPRequestHandler
import json

def default_welcome_message(message):
    if message:
        return message


bot_1 = {
    "id": 1,
    "name": "bot-1",
    "intents": ["play_sound"],
    "password": "password123"
}
bot_2 = {
    "id": 2,
    "name": "bot-2",
    "intents":["default_welcome_message"],
    "password": 'password456'
}
bot_3 = {
    "id": 3,
    "name": "bot-3",
    "intents": [],
    "password": "password789",
    "token": "123456789"
}

bots = [bot_1, bot_2, bot_3]

class MyServer(BaseHTTPRequestHandler):

    def make_api_call(self):
        return "You can make api calls"

    def check_bot(self, bot_name): #bot_name
        for bot in bots:
            if bot["name"] == bot_name:
                return bot
        else:
            return None

    def check_intents(self, bot, intents):
        if intents in bot["intents"]:
            return True
        return False

    def authenticate(self, bot, password):
        if password == bot["password"]:
            return True
        return False

    def oauth(self, bot, token):
        if token == bot["token"]:
            return True
        return False

    def simple_request(self):

        json_data = dict()

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def body_request(self):
        # json data initiated
        json_data = dict()
        # response and headers
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # extracting body data
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself

        # checking data validity
        try:
            post_data = json.loads(post_data)
        except:
            return self.send_error(403, "Invalid data")

        # get bot data
        bot = self.check_bot(post_data["name"])
        if bot:

            # authenticate bot using password
            authenticate = self.authenticate(bot, post_data.get("password"))
            if authenticate:
                self.wfile.write("User authenticated ".encode('utf-8'))
                json_data["Authorization_password"] = "User authenticated"


                # authenticate bot using token
                token = self.headers.get("Authorization")
                if token:

                    oauth = self.oauth(bot, token.split(" ")[-1])

                    # if authenticated it can make api calls
                    if oauth:
                        self.wfile.write(self.make_api_call().encode('utf-8'))
                        json_data["Authenticate_token"] = 'user can make api calls '
                    else:
                        self.wfile.write("Token is failed ".encode('utf-8'))
                        json_data["Authenticate_token"] = 'Token is failed'


                # check permission of bot
                if post_data.get("intents"):
                    permit = self.check_intents(bot, post_data["intents"])
                    if permit:
                        self.wfile.write("Bot can {} ".format(post_data["intents"]).encode('utf-8'))
                        json_data["intents"] = "Bot can {} ".format(post_data["intents"])

                        # check if user can generate message

                        if post_data["intents"] == "default_welcome_message":
                            if "message" in post_data:
                                self.wfile.write("{}\n".format(default_welcome_message(post_data["message"])).encode('utf-8'))
                                json_data["message"] = default_welcome_message(post_data["message"])
                            else:
                                print("Else!")
                                json_data["message"] = "Hi this is the defualt welcome message"


                    else:
                        self.wfile.write("Wrong intents ".encode('utf-8'))
                        json_data["intents"] = "Wrong intents"


            else:
                self.wfile.write("Unauthenticated User ".encode('utf-8'))
                json_data["Authorization_password"] = "Incorrect password, try again!"


        self.wfile.write("{} request for {} ".format(self.command, self.path).encode('utf-8'))
        json_to_pass = json.dumps(json_data)
        self.wfile.write(json_to_pass.encode('utf-8'))


    do_GET = simple_request
    do_DELETE = simple_request
    do_POST = body_request
    do_PUT = body_request
    do_PATCH = body_request