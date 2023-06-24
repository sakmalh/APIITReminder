def text_formatting(turnitin, assignment):
    text_str = "*This is an AUTOMATED MESSAGE* \n\n*Turnitin Submissions* \n\n"
    for turnit in turnitin:
        text_str = text_str + f"*{turnit['Title']}* \nDue Date - {turnit['Due Date']} \nTime Remaining - _{turnit['Time Remaining']}_ \n"

    text_str = text_str + "\n *Normal Submissions* \n\n"
    for assign in assignment:
        text_str = text_str + f"*{assign['Title']}* \nDue Date - _{assign['Due Date']}_ \nTime Remaining - _{assign['Time Remaining']}_ \n"

    return text_str
