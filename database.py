from time import sleep
class Database():
    def get_user(self, user=None):
        sleep(5)
        return [{'photo': '/tmp/photo1.png', 'nick':'Peto'}, {'photo':'/tmp/photo2.png', 'nick':'Kubo'}]

    def get_food(self, food=None):
        sleep(3)
        return [{'name': 'Horalky', 'price': 25}, {'name': 'Pizza', 'price': 135}]
