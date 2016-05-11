from time import sleep


class Database:
    @staticmethod
    def get_user(_=None):
        sleep(5)
        return [{'photo': '/tmp/photo.bmp', 'nick': 'Peto', 'balance': 47}, {'nick': 'Kubo'}]

    @staticmethod
    def get_item(_=None):
        sleep(3)
        return [{'name': 'Horalky', 'price': 25}, {'name': 'Pizza', 'price': 135}]

    @staticmethod
    def buy_items(user_id, item_id, amount, price=None):
        print("user: ", user_id, "\nitem: ", item_id, "\n amount: ", amount, "\nprice: ", price)
