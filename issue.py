"""
Issue tokens to Thalia members

"""

from jinja2 import Environment, FileSystemLoader

import sys
from datetime import datetime

env = Environment(loader=FileSystemLoader('./templates'))
existing_users = []

with open('existing_users', 'r') as f:
    for line in f:
        existing_users.append(line.strip().lower())

def render(template_name, **kwargs):
    "Render an XML file"
    template = env.get_template("{}.j2".format(template_name))
    template.stream(**kwargs).dump("tmp/{}".format(template_name))

def create_issuescript():
    "Create the issueScript.xml"
    print("Enter your PIN-code:", end=" ", flush=True)
    input_ = sys.stdin.readline().strip().lower()
    if input_.isdigit():
        render("issueScript.xml", pin_code=input_)
    else:
        print("Digits only!", flush=True)
        return create_issuescript()

def over_18():
    "Issue over 18 credential"
    print("Over 18? [y/n]", end=" ", flush=True)
    input_ = sys.stdin.readline().strip().lower()
    if input_ in ('y', 'yes', 'ja', 'j'):
        render("age-cred.xml", over_18="yes")
    elif input_ in ('n', 'no', 'nee'):
        render("age-cred.xml", over_18="no")
    else:
        return over_18()

def kind_of_member():
    "Issue membership credential"
    print("Kind of member? [Member, Begunstiger, Honorary member]: ",
            end=" ", flush=True)
    input_ = sys.stdin.readline().strip().lower()
    lid_type = ""
    if input_ in ('m', 'l', 'member', 'lid'):
        lid_type = 'member'
    elif input_ in ('erelid', 'honorary member', 'h', 'e'):
        lid_type = 'honorary member'
    elif input_ in ('begunstiger', 'b'):
        lid_type = 'begunstiger'
    else:
        return kind_of_member()

    print("You entered: {}. Are you sure? [y/n]".format(lid_type), end=" ",
            flush=True)
    input_ = sys.stdin.readline().strip().lower()
    if input_ in ("y", "j", "ja", "yes"):
        render("member-cred.xml",
              is_member=("yes" if lid_type == "member" else "no"),
              is_begunstiger=("yes" if lid_type == "begunstiger" else "no"),
              is_honorary_member=("yes" if lid_type == "honorary member"
                                        else "no"),
              days_to_sept_1=(
                  datetime(datetime.now().year+1, 9, 1) - datetime.now()).days)

    else:
        return kind_of_member()

def issue_root():
    "Issue Thalia root credential"
    print("Thalia username:", end=" ", flush=True)
    username = sys.stdin.readline().strip().lower()
    if username in existing_users:
        print("User {} already exists!".format(username))
        return issue_root()
    print("Is {} correct? [y/n]".format(username), end=" ", flush=True)
    input_ = sys.stdin.readline().strip().lower()
    if input_ in ("y", "j", "ja", "yes"):
        render("root-cred.xml", user_id=username)
        with open("existing_users", "a") as f:
            f.write("{}\n".format(username))
    else:
        return issue_root()


if __name__ == "__main__":
    issue_root()
    kind_of_member()
    over_18()
    create_issuescript()
