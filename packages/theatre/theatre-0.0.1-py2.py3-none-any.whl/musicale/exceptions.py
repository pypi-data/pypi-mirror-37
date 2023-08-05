class MPVException(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        return f"MPV request failed. Response: {self.response}"
