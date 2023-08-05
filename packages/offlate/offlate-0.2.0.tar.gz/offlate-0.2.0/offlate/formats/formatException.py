class UnsupportedFormatException(Exception):
    def __init__(self, message):
        super().__init__('Unsupported format: '+message)
