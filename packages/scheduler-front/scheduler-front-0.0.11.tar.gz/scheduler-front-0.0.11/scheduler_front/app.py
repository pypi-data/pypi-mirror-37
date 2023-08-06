import webbrowser
import os
from flask import Flask, render_template, request
from scheduler_front.script_template import file as source_file
from distutils.dir_util import copy_tree

ADMIN_EMAIL = 'c.camilli@criteo.com'

app = Flask(__name__, static_url_path='')


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        create_folder(request)
        write_scheduler_configuration_file(request)
        write_query(request)
        write_script_configuration_file(request)
        copy_script_template(request)
        return render_template('success.html')


def create_folder(form):
    output_dir = parse_output_dir(form)
    folder_name = parse_folder_name(form)

    os.mkdir(f"{output_dir}\{folder_name}")
    os.mkdir(f"{output_dir}\{folder_name}\\bin")
    os.mkdir(f"{output_dir}\{folder_name}\\conf")
    os.mkdir(f"{output_dir}\{folder_name}\\queries")
    os.mkdir(f"{output_dir}\{folder_name}\\outputs")

    with open(f"{output_dir}\{folder_name}\\conf\\.gitignore", 'w') as f:
        f.write("*.conf5\n")

    with open(f"{output_dir}\{folder_name}\\outputs\\.gitignore", 'w') as f:
        f.write("*.csv\n")
        f.write("*.xlsx\n")

    with open(f"{output_dir}\{folder_name}\\outputs\\cleaning_bot_instructions.txt", 'w') as f:
        f.write("delete_after_nb_days: 60\n")




def copy_script_template(form):
    output_dir = parse_output_dir(form)
    folder_name = parse_folder_name(form)

    filename = f"{output_dir}\{folder_name}\\bin\\script.py" if output_dir else 'script.py'

    with open(filename, 'w') as destination_file:
        destination_file.write(source_file)


def parse_destination_emails(form):
    return form.form['destination_email'].split(';')


def parse_folder_name(form):
    return form.form['job_name']


def parse_kind_of_query(form):
    return form.form['kind_of_query']


def parse_email_subject(form):
    return form.form['subject_email']


def parse_email_body(form):
    return form.form['body_email']


def parse_output_file_format(form):
    return form.form['output_type']


def parse_error_emails(form):
    return [email.strip() for email in form.form['error_email'].split(';')]


def parse_output_dir(form):
    return form.form['output_dir']


def write_script_configuration_file(form):
    output_dir = parse_output_dir(form)
    folder_name = parse_folder_name(form)
    kind_of_query = parse_kind_of_query(form)
    destination_emails = parse_destination_emails(form)
    email_subject = parse_email_subject(form)
    email_body = parse_email_body(form)
    output_file_format = parse_output_file_format(form)
    email_sender = ADMIN_EMAIL

    filename = f"{output_dir}\{folder_name}\\bin\\script_config.py" if output_dir else 'script_config.py'

    parsed_emails = ", ".join([f"'{email.strip()}'" for email in destination_emails])

    with open(filename, 'w') as f:
        f.write(f"kind_of_query = '{kind_of_query}'\n")
        f.write(f"output_type = '{output_file_format}'\n")
        f.write(f"destination_emails = [{parsed_emails}]\n")
        f.write(f"email_subject = '{email_subject}'\n")
        f.write(f"email_body = '''{email_body}'''\n")
        f.write(f"email_sender = '{email_sender}'")


def write_query(form):
    output_dir = parse_output_dir(form)
    folder_name = parse_folder_name(form)
    filename = f"{output_dir}\{folder_name}\\queries\\query.sql" if output_dir else 'query.sql'

    with open(filename, 'w') as f:
        f.write(form.form['query'])


def parse_days(form):
    days = []
    for i in range(1, 32):
        try:
            if form.form[str(i)]:
                days.append(str(i))
        except KeyError:
            pass

    return ",".join(days)


def parse_weekdays(form):
    weekdays = ""

    days_of_the_week = [
        'sunday',
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday'
    ]

    weekdays = []

    for i, day in enumerate(days_of_the_week):
        try:
            if form.form[day]:
                weekdays.append(str(i))
        except KeyError:
            pass

    return ",".join(weekdays)


def parse_months(form):
    months = []
    months_of_the_year = [
        'jan',
        'feb',
        'mar',
        'apr',
        'may',
        'jun',
        'jul',
        'aug',
        'sep',
        'oct',
        'nov',
        'dec'
    ]

    for i, month in enumerate(months_of_the_year):
        try:
            if form.form[month]:
                months.append(str(i + 1))
        except KeyError:
            pass

    return ",".join(months)


def write_scheduler_configuration_file(form):
    error_emails = parse_error_emails(form)
    days = parse_days(form)
    weekdays = parse_weekdays(form)
    months = parse_months(form)

    output_dir = parse_output_dir(form)
    folder_name = parse_folder_name(form)
    filename = f"{output_dir}\{folder_name}\\conf\\config.txt" if output_dir else 'config.txt'

    with open(filename, 'w') as f:
        if not error_emails:
            raise ValueError
        else:
            f.write(f"error_email: {', '.join(error_emails)}\n")
        if days:
            f.write(f"days: {days}\n")
        if weekdays:
            f.write(f"weekdays: {weekdays}\n")
        if months:
            f.write(f"months: {months}\n")


def start():
    webbrowser.open('http://127.0.0.1:5000')
    app.run()


if __name__ == '__main__':
    start()
