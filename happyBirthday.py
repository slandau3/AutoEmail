#! python3
# happyBirthday.py - Sends emails to specific person wishing them a happy birthday!

import smtplib as smtp
import sys
import datetime
import shelve

import math

SMTP_EMAIL = 'smtp.gmail.com'
EMAIL_LOGIN = 'example@something.com'
EMAIL_PASSWORD = 'password1234'
SUBJECT = 'SUBJECT_LINE'
NAME = 'name'


def add_entry(name, email, day, month, message):
    add_to_dictionary(name, email, day, month)
    set_message(name, message)


def add_to_dictionary(person, email, day, month):
    """
    :param person: String of someones name
    :param email: that persons email
    :param day: the current day (recommend using datetime module)
    :param month: the current month (same as above)
    """
    shelf_file = shelve.open('birthdays')  # opens birthdays file
    name_dates = shelve.open('nameDates')
    shelf_file_email = shelve.open('emails')  # opens emails file

    """Store the month and day in a list for future concatination"""
    lst = [str(month), str(day)]

    """Write to the name->HumanReadableDate file."""
    name_dates[person] = '/'.join(lst)

    """Hash the day + month (key) and set it equal to the name (value)."""
    shelf_file[str(hash(day)
                   +
                   hash(
                       month))] = person  # sets a hashcode for the day and month then sets those 2 equal to a persons name

    shelf_file_email[person] = email  # takes the persons name and connects it to an email

    """Close the files."""
    shelf_file.close()
    name_dates.close()
    shelf_file_email.close()


def get_name_and_email(day, month): # at some point I will modify this to work with name/email
    """
    :param day:  the current day (use datetime module datetime.day)
    :param month: the current month (use datetime module datetime.month)
    :return: an arraylist containing a name and email (respectively)
    """
    shelf_file = shelve.open('birthdays')  # re opens the birthdays file
    shelf_file_email = shelve.open('emails')  # re opens the emails file

    """Get the name and email from the shelve files"""
    name = shelf_file[str(hash(day) + hash(month))]
    email = shelf_file_email[name]  # obtains the persons email

    """Turn the name and email into a list."""
    lst = [name, email]

    """Close the files."""
    shelf_file_email.close()
    shelf_file.close()

    """Return the list, [name, email]."""
    return lst  # returns list name , email


def get_message(name):
    message = shelve.open('messages')

    """Get the message from the given name."""
    msg = message[name]

    """Close the file."""
    message.close()
    return msg


def send_email(name, recieptient_email):
    """
    :param name: the persons name
    :param recieptientEmail: the persons email
    """
    smtpObj = smtp.SMTP_SSL(SMTP_EMAIL, 465)
    smtpObj.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    smtpObj.sendmail(EMAIL_LOGIN, recieptient_email, 'Subject: %s\nDear %s\nI wish you '
                                                                    'a very happy birthday!\n\n%s'
                                                                    '\n\nLove,\n%s\n\n\n' % (
                         SUBJECT, name, get_message(name), NAME)) # See above to set 2 of these. I plan on making 'subject' come from a dictionary at a later point.


def del_entry(name):
    shelf_file = shelve.open('birthdays')
    name_dates = shelve.open('nameDates')
    message_file = shelve.open('messages')
    shelf_file_email = shelve.open('emails')

    """Get the date from the given name."""
    dates = name_dates[name]
    day_bool = False
    month = ''
    day = ''

    """Go through the dates to separate the '/'
    and split the string into month and day."""
    for i in dates:
        if i is '/':
            day_bool = True

        elif day_bool is False:
            month += i
        else:
            day += i

    """Deletion step."""
    code = str(hash(day) + hash(month))
    del message_file[name]
    del shelf_file[code]
    del name_dates[name]
    del shelf_file_email[name]

    """Closing of files."""
    shelf_file.close()
    name_dates.close()
    message_file.close()
    shelf_file_email.close()


def set_message(name, message=''):
    message_file = shelve.open('messages')

    """Set the name (key) and message (value)."""
    message_file[name] = message

    """Closing calls."""
    message_file.close()


def hash(var):
    var = int(var)
    return var * 8014 + 6


def print_name_and_email():
    name_email = shelve.open('emails')
    for i in name_email.keys():
        print(str(i), ' : ', name_email[i])
    name_email.close()


def print_name_and_message():
    name_message = shelve.open('messages')

    """Go through the files keys and print them"""
    for i in name_message.keys():
        print(str(i), ':', str(name_message[i]))
    name_message.close()


def print_name_and_birthday():
    name_date = shelve.open('nameDates')

    """Go through the files keys and print them."""
    for i in name_date.keys():
        print(str(i), ':', str(name_date[i]))


def main():
    """Fucntions you should use: add_entry, del_entry,
    print_name_and_email, print_name_and_message,
    set_message"""
    date = datetime.datetime.now()

    """Print statements"""
    # print_name_and_email()
    # print_name_and_message()
    # print_name_and_birthday()

    # add_entry(name, email, day, month, message) # when adding someone new to the database
    # set_message(name, message) # to change the message of a particular person

    """Will see if there are any birth days on today's date.
    If there are, everything will proceed and an email will be send.
    Otherwise an error will be thrown."""
    name_and_email = None
    try:
        name_and_email = get_name_and_email(date.day, date.month)
    except:
        pass

    if name_and_email is not None:
        send_email(name_and_email[0], name_and_email[1])


if __name__ == '__main__':
    main()
