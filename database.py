from time import sleep
class Database():
    def get_user(self, user=None):
        sleep(5)
        return [{'photo': '/tmp/photo.bmp', 'nick': 'Peto'}, {'nick': 'Kubo'}]

    def get_item(self, food=None):
        sleep(3)
        return [{'name': 'Horalky', 'price': 25}, {'name': 'Pizza', 'price': 135}]

    def buy_items(self, user_id, item_id, amount, price=None):
        print("user: ", user_id, "\nitem: ", item_id, "\n amount: ", amount, "\nprice: ", price)
