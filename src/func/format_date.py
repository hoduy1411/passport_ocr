import re
from unidecode import unidecode
from datetime import datetime


dict_month = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06", "JUL": "07", "AUG": "08", "SEP": "09", "OCT": "10", "NOV": "11", "DEC": "12"}


def clean_string(input_string):
    # Remove signed characters
    normalized_string = unidecode(input_string)

    # Remove characters that not number or text, retain "/"
    cleaned_string = re.sub(r'[^a-zA-Z0-9/]', '', normalized_string)

    # Return the clean string
    return cleaned_string


def check_day(inp_day, inp_month, inp_year):
    correct_day = ''

    if int(inp_month) == 1 or int(inp_month) == 3 or int(inp_month) == 5 or int(inp_month) == 7 or\
            int(inp_month) == 8 or int(inp_month) == 10 or int(inp_month) == 12:
        
        if int(inp_day) > 31:
            correct_day = ''
        else:
            correct_day = inp_day

    if int(inp_month) == 2:
        if int(inp_year) % 4 == 0:
            if int(inp_day) > 29:
                correct_day = ''
            else:
                correct_day = inp_day
        else:
            if int(inp_day) > 28:
                correct_day = ''
            else:
                correct_day = inp_day
    
    if int(inp_month) == 4 or int(inp_month) == 6 or int(inp_month) == 9 or int(inp_month) == 11:
        if int(inp_day) > 30:
            correct_day = ''
        else:
            correct_day = inp_day

    return correct_day


def convert_year(two_digits_year):
    if two_digits_year.isnumeric():
        return '20' + two_digits_year if int(two_digits_year) < 50 else '19' + two_digits_year
        

def format_date(inp_string):  
    # Clean input string before formatting the date
    inp_string = clean_string(inp_string)

    # Variables
    day, month, year = '', '', ''
    lst_result = list()

    # Using this when input is dd/mm/yy or dd/mm/yyyy
    if inp_string.count("/") == 2:
        new_str = inp_string.split("/")
        if new_str[0].isnumeric() and new_str[0].startswith(('0', '1', '2', '3')) and new_str[2].isnumeric():
            if (int(new_str[0]) <= 31) and (int(new_str[2]) <= (datetime.now().year + 10)):

                day = new_str[0]
                year = new_str[2]

                if len(new_str[2]) == 2:
                    year = convert_year(new_str[2])

                if new_str[1].isnumeric():
                    if new_str[1].startswith(('0', '1')):
                        if int(new_str[1]) <= 12:
                            day = check_day(new_str[0], new_str[1], year)
                            month = new_str[1]
                        else:
                            month = ""
                    else:
                        month = ""
                else:
                    if new_str[1].upper() in dict_month:
                        month = dict_month.get(new_str[1].upper())
                    else:
                        month = ''

                if not day or not month or not year:
                    return ""
                else:
                    return f'{day}/{month}/{year}'
            else:
                return ""

    # Format: dd mm(alpha) yyyy
    ket_qua_1 = re.search(r'(\d{2})([a-zA-Z]{3})(\d{4})', inp_string)
    if ket_qua_1:
        rst = list(ket_qua_1.groups())
        print('format 1', rst)

        if rst[0].isnumeric() and rst[1].isalpha() and rst[2].isnumeric():
            if (int(rst[0]) <= 31) and (int(rst[2]) <= (datetime.now().year + 10)):
                print('Format dd/mm(alpha)/yyyy')
                
                if rst[1].upper() in dict_month:
                    month = dict_month.get(rst[1].upper())
                else:
                    month = ''
                
                day = rst[0]
                year = rst[2]
                day = check_day(day, month, year)

            else:
                day = ''
                year = ''

        else:
            day = ''
            month = ''
            year = ''

        lst_result.append([day, month, year])
    
    # Format: dd mm(digit) yyyy
    ket_qua_2 = re.search(r'(\d{2})(\d{2})(\d{4})', inp_string)
    if ket_qua_2:
        rst = list(ket_qua_2.groups())
        print('format 2', rst)

        if rst[0].isnumeric() and rst[1].isnumeric() and rst[2].isnumeric():
            if (int(rst[0]) <= 31) and (int(rst[1]) <= 12) and (int(rst[2]) <= (datetime.now().year + 10)):
                print('Format dd/mm(digit)/yyyy')

                day = rst[0]
                month = rst[1]
                year = rst[2]

                day = check_day(day, month, year)

                if not month.startswith('0'):
                    month = ''
                
            else:
                day = ''
                month = ''
                year = ''

        else:
            day = ''
            month = ''
            year = ''

        lst_result.append([day, month, year])
            

    # Format: dd mm/m'm'(alpha/as nation) yyyy
    ket_qua_3 = re.search(r'(\d{2})([a-zA-Z]{3,4}/[a-zA-Z]{3,4})(\d{4})', inp_string)
    if ket_qua_3:
        rst = list(ket_qua_3.groups())
        print('format 3', rst)

        if rst[0].isnumeric() and rst[2].isnumeric():
            if (int(rst[0]) <= 31) and (int(rst[2]) <= (datetime.now().year + 10)):
                print('Format dd/mm(alpha/as nation)/yyyy')

                month = rst[1].replace(" ", "")
                month_list = month.split("/")
                
                if len(month_list) == 2:
                    if month_list[0].upper() in dict_month:
                        month = dict_month.get(month_list[0].upper())
                    elif month_list[1].upper() in dict_month:
                        month = dict_month.get(month_list[1].upper())
                    else:
                        month = ''
                elif len(month_list) == 1:
                    if month_list[0].upper() in dict_month:
                        month = dict_month.get(month_list[0].upper())
                    else:
                        month = ''
                else:
                    month = ''
                
                day = rst[0]
                year = rst[2]

                if month != '':
                    day = check_day(day, month, year)

            else:
                day = ''
                year = ''

        else:
            day = ''
            month = ''
            year = ''
            
        lst_result.append([day, month, year])
    
    # Format: dd mm(alpha) yy
    ket_qua_4 = re.search(r'(\d{2})([a-zA-Z]{3})(\d{2})', inp_string)
    if ket_qua_4:
        
        rst = list(ket_qua_4.groups())
        print('format 4', rst)

        if rst[0].isnumeric() and rst[1].isalpha() and rst[2].isnumeric():
            if (int(rst[0]) <= 31) and (rst[2] != '0'):
                print('Format dd/mm(alpha)/yy')
                
                if rst[1].upper() in dict_month:
                    month = dict_month.get(rst[1].upper())
                else:
                    month = ''
                
                day = rst[0]
                year = rst[2]
                
                if len(year) == 2:
                    year = convert_year(year)
                if month != '':
                    day = check_day(day, month, year)
            else:
                day = ''
        else:
            day = ''
            month = ''
            year = ''

        lst_result.append([day, month, year])
    
    # Format: dd mm/m'm'(alpha/as nation) yy
    ket_qua_5 = re.search(r'(\d{2})([a-zA-Z]{3,4}/[a-zA-Z]{3,4})(\d{2})', inp_string)
    if ket_qua_5:
        rst = list(ket_qua_5.groups())
        print('format 5', rst)

        if rst[0].isnumeric() and rst[2].isnumeric():
            if (int(rst[0]) <= 31) and (rst[2] != '0'):
                print('Format dd/mm(alpha/as nation)/yy')
                
                month = rst[1].replace(" ", "")
                month_list = month.split("/")

                if len(month_list) == 2:
                    if month_list[0].upper() in dict_month:
                        month = month = dict_month.get(month_list[0].upper())
                    elif month_list[1].upper() in dict_month:
                        month = month = dict_month.get(month_list[1].upper())
                    else:
                        month = ''
                elif len(month_list) == 1:
                    if month_list[0].upper() in dict_month:
                        month = month = dict_month.get(month_list[0].upper())
                    else:
                        month = ''
                else:
                    month = ''
                
                day = rst[0]
                year = rst[2]

                if len(year) == 2:
                    year = convert_year(year)

                if month != '':
                    day = check_day(day, month, year)

            else:
                day = ''
                year = ''

        else:
            day = ''
            month = ''
            year = ''

        lst_result.append([day, month, year])
    
    # Format: dd mm(digit) yy
    ket_qua_6 = re.search(r'(\d{2})(\d{2})(\d{2})', inp_string)
    if ket_qua_6:
        rst = list(ket_qua_6.groups())
        print('format 6', rst)

        if rst[0].isnumeric() and rst[1].isnumeric() and rst[2].isnumeric():
            if (int(rst[0]) <= 31) and (rst[2] != '0') and (int(rst[1]) <= 12):
                print('Format dd/mm(digit)/yy')

                day = rst[0]
                month = rst[1]
                year = rst[2]
                if len(year) == 2:
                    year = convert_year(year)
                
                day = check_day(day, month, year)

            else:
                day = ''
                month = ''

        else: 
            day = ''
            month = ''
            year = ''

        lst_result.append([day, month, year])
    #print(lst_result)
    rslt = [lst for lst in lst_result if all (ele != '' for ele in lst)]

    if len(rslt):
        return "/".join(rslt[0])
    
    else:
        day = ''
        month = ''
        year = ''

        rst = re.sub(r'[.\-/]', ' ', inp_string)
        rst = rst.split()
        #print(rst)
        # Only day starts with 0, 1, 2, or 3, that valid and this day is only number
        if not rst[0][:2].startswith(('0', '1', '2', '3')) and rst[0][:2].isnumeric() == False:
            return ""       
        else:
            if (int(rst[0][:2]) > 31):                       # day > 31 -> invalid
                return ""
            day = rst[0][:2]                                 # get day
            if rst[0][2:].upper() in dict_month:             # find valid month (from retaining string)
                month = dict_month.get(rst[0][2:].upper())   # get month
            else:
                month = ''
        
        if len(rst) != 1:
            # ex: 01 JAN/JAN 2001
            if rst[1][-4:].isnumeric():
                year = rst[1][-4:]
                if int(year) > (datetime.now().year + 10):
                    year = ''
                if not month:
                    if rst[1][:-4].upper() in dict_month:
                        month = dict_month.get(rst[1][:-4].upper())
                    else:
                        month = ''
            # ex: 01 JAN/JAN 01
            else:
                year = rst[1][-2:]
                if len(year) == 2:
                    year = convert_year(year)
                if int(year) > (datetime.now().year + 10):
                    year = ''
                if not month:
                    if rst[1][:-4].upper() in dict_month:
                        month = dict_month.get(rst[1][:-4].upper())
                    else:
                        month = ''
        
        # Return the result 
        if not day or not month or not year:
            return ''                              # empty string
        else:
            return f'{day}/{month}/{year}'         # format dd/mm/yyyy 

    # Invalid format
    #return ''  