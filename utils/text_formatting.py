def text_formatting(ten_day, three_day, initialized):
    text_str = "*This is an AUTOMATED MESSAGE* \n"

    if len(initialized) != 0:
        "\n * New Submissions * \n\n"
        for assign in initialized:
            text_str = text_str + f"*{assign['Title']}  {assign['Type']}* \nDue Date - _{assign['Due Date']}_ \nTime Remaining - _{assign['Time Remaining']}_ \n"

    if len(ten_day) != 0:
        text_str = text_str + "\n *Ten Day Reminder* \n\n"
        for assign in ten_day:
            text_str = text_str + f"*{assign['Title']}  {assign['Type']}* \nDue Date - {assign['Due Date']} \nTime Remaining - _{assign['Time Remaining']}_ \n"

    if len(three_day) != 0:
        text_str = text_str + "\n *Three Day Reminder* \n\n"
        for assign in three_day:
            text_str = text_str + f"*{assign['Title']}  {assign['Type']}* \nDue Date - _{assign['Due Date']}_ \nTime Remaining - _{assign['Time Remaining']}_ \n"

    return text_str
