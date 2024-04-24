import sys

def error_message_detail(error,error_detail:sys):
    """ this function is used to return a customized error message"""
    _, _, exc_tb = error_detail.exc_info()
    # get the file name that error was occured
    file_name = exc_tb.tb_frame.f_code.co_filename
    # creat a custom error message
    error_message = f"""Error occured in python script name {file_name} line number {exc_tb.tb_lineno}
      {str(error)} error message """
    return error_message

# create a custom exception class
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message,error_detail)
    
    def __str__(self):
        return self.error_message
    

