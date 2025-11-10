#!/usr/bin/python
import os
import sys
import time
import getpass
import smtplib


class bcolors:
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


def raw_input(prompt):
    return input(prompt)


def help_message(server_no):
    if server_no == 1:
        print(
            bcolors.WARNING
            + "\n[!] For Gmail, you need to use an App Password:"
            + bcolors.ENDC
        )
        print("    1. Go to https://myaccount.google.com/apppasswords")
        print("    2. Generate an App Password for 'Mail'")
        print("    3. Use that 16-character password instead of your regular password")
    elif server_no == 2:
        print(
            bcolors.WARNING
            + "\n[!] For Yahoo, you need to generate an App Password:"
            + bcolors.ENDC
        )
        print("    1. Go to https://login.yahoo.com/account/security")
        print("    2. Generate an app password")
        print("    3. Use that password instead of your regular password")
    else:
        print(
            bcolors.FAIL
            + "\n[!] OUTLOOK/HOTMAIL NO LONGER SUPPORTS BASIC SMTP AUTHENTICATION!"
            + bcolors.ENDC
        )
        print(
            bcolors.WARNING
            + "\n    Microsoft has completely disabled SMTP for personal accounts."
            + bcolors.ENDC
        )
        print("    This cannot be fixed with app passwords or any workaround.")
        print("    \n    SOLUTION: Please use Gmail or Yahoo instead:")
        print("    - Gmail: Works perfectly with app passwords")
        print("    - Yahoo: Also supports app passwords")
        print("\n    If you must use Outlook, you'll need to use Microsoft Graph API")
        print("    (which requires OAuth2 and is much more complex).")


def bomb():
    os.system("clear")
    print(
        bcolors.OKGREEN
        + """
             \|/
                       `--+--'
                          |
                      ,--'#`--.
                      |#######|
                   _.-'#######`-._
                ,-'###############`-.
              ,'#####################`,         .___     .__         .
             |#########################|        [__ ._ _ [__) _ ._ _ |_  _ ._.
            |###########################|       [___[ | )[__)(_)[ | )[_)(/,[
           |#############################|
           |#############################|              Author: Mazen Elzanaty
           |#############################|
            |###########################|
             \#########################/
              `.#####################,'
                `._###############_,'
                   `--..#####..--'                                 ,-.--.
*.______________________________________________________________,' (Bomb)
                                                                    `--' """
        + bcolors.ENDC
    )


def get_server_info(index):
    server_info = {
        1: ("smtp.gmail.com", 587),
        2: ("smtp.mail.yahoo.com", 587),
        3: ("smtp-mail.outlook.com", 587),
    }

    return server_info.get(index, None)


def send_email(server_no, user, pwd, to, subject, body, nomes):
    bomb()
    message = "From: " + user + "\nSubject: " + subject + "\n" + body
    server_info = get_server_info(server_no)
    if server_info is None:
        print(bcolors.FAIL + "[-] Invalid Mail Server choice." + bcolors.ENDC)
        return None
    try:
        smtp_server = smtplib.SMTP(server_info[0], server_info[1])
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(user, pwd)
        for no in range(nomes):
            smtp_server.sendmail(user, to, message)
            print(
                bcolors.OKGREEN
                + "[+] Email Sent Successfully to "
                + to
                + " ("
                + str(no + 1)
                + "/"
                + str(nomes)
                + ")"
                + bcolors.ENDC
            )
            time.sleep(1)
        smtp_server.quit()
    except smtplib.SMTPAuthenticationError as e:
        print(
            bcolors.FAIL
            + "[-] Authentication Error. Check your email and password."
            + bcolors.ENDC
        )
        help_message(int(server_no))
        # raise e
    except Exception as e:
        print(bcolors.FAIL + "[-] An error occurred: " + str(e) + bcolors.ENDC)
        # raise e


def main():
    os.system("clear")
    try:
        file1 = open("Banner.txt", "r")
        print(" ")
        print(bcolors.OKGREEN + file1.read() + bcolors.ENDC)
        file1.close()
    except IOError:
        print("Banner File not found")

    # Input
    print(
        bcolors.WARNING
        + """
    Choose a Mail Service:
    1) Gmail
    2) Yahoo
    3) Hotmail/Outlook
    """
        + bcolors.ENDC
        + "--------------------------------------------------------------"
    )

    try:
        server = raw_input(bcolors.OKGREEN + "Mail Server: " + bcolors.ENDC)

        # Warn user if they select Outlook
        if server == "3":
            print(
                bcolors.FAIL
                + "\n[!] WARNING: Outlook/Hotmail is NOT supported!"
                + bcolors.ENDC
            )
            print(
                bcolors.WARNING
                + "    Microsoft has disabled basic SMTP authentication for personal accounts."
                + bcolors.ENDC
            )
            print("    This will NOT work even with app passwords.\n")
            proceed = raw_input(
                bcolors.WARNING
                + "    Do you want to continue anyway? (yes/no): "
                + bcolors.ENDC
            )
            if proceed.lower() not in ["yes", "y"]:
                print(
                    bcolors.OKGREEN
                    + "\n[+] Please use Gmail (1) or Yahoo (2) instead."
                    + bcolors.ENDC
                )
                sys.exit()

        user = raw_input(bcolors.OKGREEN + "Your Email: " + bcolors.ENDC)
        pwd = getpass.getpass(bcolors.OKGREEN + "Password: " + bcolors.ENDC)
        to = raw_input(bcolors.OKGREEN + "To: " + bcolors.ENDC)
        subject = raw_input(bcolors.OKGREEN + "Subject (Optional): " + bcolors.ENDC)
        body = raw_input(bcolors.OKGREEN + "Message: " + bcolors.ENDC)
        nomes = input(bcolors.OKGREEN + "Number of Emails to send: " + bcolors.ENDC)
        no = 0
        message = "From: " + user + "\nSubject: " + subject + "\n" + body
    except KeyboardInterrupt:
        print(bcolors.FAIL + "\nCanceled" + bcolors.ENDC)
        sys.exit()

    status = send_email(int(server), user, pwd, to, subject, body, int(nomes))
    if status is None:
        sys.exit()


if __name__ == "__main__":
    main()
