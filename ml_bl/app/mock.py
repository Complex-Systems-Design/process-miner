'''
Module to mock behaviour of machine learning algorithm TO BE REPLACED
'''

from time import sleep

def ml_algorithm_mock() -> str:
    '''
    Function to mock the behaviour of the machine learning algorithm
    parameters:
        None
    returns
        value (str): Sample string
    '''
    value = 'Hello World!'
    
    sleep(3)

    return value
