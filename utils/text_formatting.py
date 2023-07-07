def text_formatting(ten_day, three_day, initialized):
    text_str = "*This is an AUTOMATED MESSAGE* \n"

    if len(initialized) != 0:
        text_str = text_str + "\n * New Submissions * \n\n"
        count = 1
        for assign in initialized:
            text_str = text_str + f"\n{count}. *{assign['Title']}  {assign['Type']}* \nDue Date - _{assign['Due Date']}_ \nTime Remaining - _{assign['Time Remaining'].days} days {int(assign['Time Remaining'].seconds/3600)} hours_ \nLink - {assign['Link']}\n"
            count += 1

    if len(ten_day) != 0:
        text_str = text_str + "\n *Ten Day Reminder* \n\n"
        count = 1
        for assign in ten_day:
            text_str = text_str + f"\n{count}. *{assign['Title']}  {assign['Type']}* \nDue Date - {assign['Due Date']} \nTime Remaining - _{assign['Time Remaining'].days} days {int(assign['Time Remaining'].seconds/3600)} hours_ \nLink - {assign['Link']}\n"
            count += 1

    if len(three_day) != 0:
        text_str = text_str + "\n *Three Day Reminder* \n\n"
        count = 1
        for assign in three_day:
            text_str = text_str + f"\n{count}. *{assign['Title']}  {assign['Type']}* \nDue Date - _{assign['Due Date']}_ \nTime Remaining - _{assign['Time Remaining'].days} days {int(assign['Time Remaining'].seconds/3600)} hours_ \nLink - {assign['Link']}\n"
            count += 1
    return text_str
