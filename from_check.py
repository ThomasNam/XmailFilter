import os
import sys
import json
import re


def write_log(log_path, str):
    with open(log_path, "a") as f:
        f.write(f"{str}\n")


def main_work():
    root_folder = os.path.dirname(os.path.abspath(__file__))

    log_path = os.path.join(root_folder, "log")

    # PASS CACHE
    xmail_root = None

    if not xmail_root:
        with open(os.path.join(root_folder, "setting.json"), "r") as st_json:
            st_python = json.load(st_json)
            xmail_root = st_python["xmailPath"]

    if len(sys.argv) < 2:
        exit(0)

    from_email = sys.argv[1]
    auth_email = sys.argv[2]
    # file_path = sys.argv[3]
    # write_log(log_path, f"Start Auth Work {from_email}, {auth_email}")

    data = from_email.split("@")

    # FROM ERROR
    if len(data) != 2:
        exit(3)

    domain = data[1]
    front = data[0]

    domain_folder = os.path.join(xmail_root, "domains", domain)

    # Check "from" domain
    if os.path.isdir(domain_folder):
        user_path = os.path.join(domain_folder, front)

        # Check exist a user
        if not os.path.isdir(user_path):
            write_log(log_path, f"Error - Not exist {user_path}")
            exit(3)

        # Check auth
        if auth_email != from_email:
            write_log(log_path, f"ERROR - Auth {user_path}, {auth_email}")
            exit(3)

    # write_log(log_path, f"Start File Path {file_path}")

    # DATA CHECK
    # data_from_check(file_path, from_email, log_path)


def data_from_check(file_path, from_email, log_path):
    with open(file_path, "r") as my_file:
        one_line = my_file.readline()
        start_data = False
        while one_line:
            # write_log(log_path, one_line)
            if not start_data and one_line.strip() == '<<MAIL-DATA>>':
                start_data = True

            elif start_data:
                temp_line = one_line.lower()

                # FROM 절 체크
                if temp_line.startswith("from"):
                    # write_log(log_path, f"from : {temp_line}")
                    pattern = r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+)"

                    match = re.search(pattern, temp_line)

                    if match:
                        data_form_email = match.group()

                        # write_log(log_path, f"data_form_email : {data_form_email}")

                        if data_form_email != from_email:
                            write_log(log_path, f"Diff Form D : {data_form_email}, A : {from_email}")
                            exit(3)

                    break

            one_line = my_file.readline()


if __name__ == '__main__':
    main_work()
