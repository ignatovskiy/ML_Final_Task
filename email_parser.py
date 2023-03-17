from email import message_from_string
from email import policy
import re
import os
import pandas as pd


def read_email_raw_data(directory, email_name):
    try:
        with open(f"{directory}/{email_name}", "r", encoding='UTF-8') as f:
            raw_string = f.read().strip()
    except UnicodeDecodeError:
        raw_string = None
    return raw_string


def get_message_from_email(message):
    try:
        msg = message_from_string(message, policy=policy.default)
        body = msg.get_body(('plain',))

        if body:
            body = str(body.get_content())
            body = re.sub('\s+', ' ', body)
            body = re.sub('\n+', ' ', body)
            body = body.lower().strip()
            return body
    except (LookupError, AttributeError):
        return None


def emails_processing(csv_filename, spam_value, directory):
    emails = []

    for filename in os.listdir(directory):
        print(filename)
        raw_string = read_email_raw_data(directory, filename)
        message = get_message_from_email(raw_string)
        if message:
            emails.append([message, spam_value])
    
    data = pd.DataFrame(emails, columns=["Message", "Spam"])
    data.to_csv(csv_filename)
    print(data.head())


def concat_files(filename1, filename2, result_filename):
    pd1 = pd.read_csv(filename1, sep=',')
    pd2 = pd.read_csv(filename2, sep=',')
    data = pd.concat([pd1, pd2])
    data.to_csv(result_filename)


if __name__ == "__main__":
    filename_spam = "spam.csv"
    filename_notspam = "notspam.csv"
    result_filename = "result.csv"

    emails_processing(filename_spam, 1, "spam")
    emails_processing(filename_notspam, 0, "ham")
    concat_files(filename_spam, filename_notspam, result_filename)