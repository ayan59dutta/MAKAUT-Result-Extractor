from result_extractor import extract_results
from notifier import send_email

path = 'C:/makaut_result_extractor/'

def extract_all(details):

    changed = False
    new_details = details[:]

    for row_no, student in enumerate(details):
        flag = student[-1]
        if student[0] != '#' and flag == 'True':
            roll_no = student[0]
            semester_no = student[1]
            email_id = student[2]
            
            if extract_results(roll_no, semester_no):
                try:
                    send_email(roll_no, semester_no, email_id)
                except:
                    pass
                new_details[row_no][-1] = 'False'
                changed = True

    return (changed, new_details)


if __name__ == '__main__':

    with open(path + 'details.txt') as fp:
        details = list(map(lambda x: x.strip(' \n').split(), fp))

    changed, new_details = extract_all(details)

    if changed:
        with open(path + 'details.txt', 'w') as fp:
            fp.write('\n'.join([' '.join(row) for row in new_details]))
            
