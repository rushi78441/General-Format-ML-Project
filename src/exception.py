import sys 

"""
This function returns a custom error message with details like:
- filename where the error occurred,
- line number of the error,
- actual error message.
"""

def error_message_details(erro, error_detail: sys):
    # Get exception info including traceback using sys.exc_info()
    _, _, exc_tb = error_detail.exc_info()

    # Get the filename where the exception occurred
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Format a detailed error message with filename, line number, and exception message
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
                        file_name, exc_tb.tb_lineno, str(erro)
                    )
    
    # Return the formatted error message
    return error_message


"""
CustomException is a user-defined exception class that inherits from Python's built-in Exception.
It generates a custom and detailed error message using the error_message_details() function.
"""

class CustomException(Exception):
    def __init__(self, error, error_detail: sys):
        """
        Constructor method to initialize the custom exception.

        Parameters:
        - error: The actual exception object (e.g., ZeroDivisionError, FileNotFoundError, etc.)
        - error_detail: The sys module used to extract traceback information
        """
        # Call the parent class constructor
        super().__init__(error)

        # Generate a detailed error message using the helper function
        self.error_message = error_message_details(error, error_detail)

    def __str__(self):
        """
        This method returns the string representation of the exception.
        It ensures that when the exception is printed, the custom error message is shown.
        """
        return self.error_message


## for checking Exception handling and logging working or not 
from logger import logging 

if __name__ == "__main__":
    try: 
        a=1/0
    except Exception as e: 
        logging.info("Divide by zero error")
        raise CustomException(e, sys)