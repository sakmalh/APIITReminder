def text_formatting(ten_day, three_day, initialized, one_day):
    text_str = "*This is an AUTOMATED MESSAGE* \n"

    if len(initialized) != 0:
        text_str = text_str + "\n * New Submissions * \n\n"
        text_str = print_list(text_str, initialized)

    if len(ten_day) != 0:
        text_str = text_str + "\n *Ten Day Reminder* \n\n"
        text_str = print_list(text_str, ten_day)

    if len(three_day) != 0:
        text_str = text_str + "\n *Three Day Reminder* \n\n"
        text_str = print_list(text_str, three_day)

    if len(one_day) != 0:
        text_str = text_str + "\n *One Day Reminder* \n\n"
        text_str = print_list(text_str, one_day)

    return text_str


def print_list(text_str, assigned_list):
    count = 1
    for assign in assigned_list:
        text_str = text_str + f"\n{count}. *{assign['Title']}  {assign['Type']}* \nDue Date - _{assign['Due Date']}_ \nTime Remaining - _{assign['Time Remaining'].days} days {int(assign['Time Remaining'].seconds / 3600)} hours_ \nLink - {assign['Link']}\n"
        count += 1

    return text_str
