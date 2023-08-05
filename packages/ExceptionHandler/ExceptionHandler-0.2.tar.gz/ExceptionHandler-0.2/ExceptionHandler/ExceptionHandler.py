class ExceptionHandler(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message =  message
        self.status = status

special_character_list = ['@','!', '$', '~', '&', '#']
number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]

def specialCharacterCheck(str):
    for char in str:
        if char.lower() in special_character_list:
            string = ''.join(special_character_list)
            raise ExceptionHandler("Special Character "+ string +" Not Accepted",406) # 406 not exceptable Status

def numberExceptionCheck(number):
    for num in number:
        if num in ''.join(str(e) for e in number_list):
            string = ''.join(str(e) for e in num)
            raise ExceptionHandler("number "+ string +" Not Accepted",406) # 406 not exceptable Status
