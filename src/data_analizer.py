class DataAnalizer:

    def __init__(self):
        self.data = []

    def set_data(self, new_data: list):
        self.data = new_data

    def get_data(self):
        return self.data
