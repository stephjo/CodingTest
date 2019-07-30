
import statistics
from statistics import mean

def validate_list(input_list):
    '''
    Validate the conditions on the list
    :param input_list:
    :return: validated list
    '''
    valid = False
    len_list = len(input_list)
    if len_list < 6:
        raise Exception('Length of the list must be greater or equal to 6. The value of Length was: {}'.format(len_list))
    if (len_list % 2) !=0:
        raise Exception('Length of the list must be an even number. The value of Length was: {}'.format(len_list))
    valid = True
    return valid

def Average(input_list):
    '''
    Find the avarage value
    :param input_list:
    :return:
    '''
    input_list = map(int,input_list)
    print('Calculating the mean of the list')
    print('Mean = {}'.format(round(mean(input_list),2)))

if __name__ == '__main__':
    input_string = (input("Enter a list of numbers separated by comma "))
    num_list = input_string.split(',')
    #sort the list so that all elements are in sequential order
    num_list = sorted(num_list)
    print('List is : {}'.format(num_list))
    #if list is valid find the average
    if(validate_list(num_list)):
        Average(num_list)


