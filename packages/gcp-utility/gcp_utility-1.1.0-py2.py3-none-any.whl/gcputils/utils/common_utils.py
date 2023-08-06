from google.cloud import bigquery
from jinja2 import Template
from datetime import datetime, timedelta
from argparse import ArgumentTypeError


def date_template(execution_date=datetime.now()):
    """

    :return: date template dictionary
    """
    current_date = execution_date
    return {
        'ds': datetime.strftime(current_date, '%Y-%m-%d'),
        'ds_nodash': datetime.strftime(current_date, '%Y%m%d'),
        'ds_yesterday': datetime.strftime(current_date - timedelta(1), '%Y-%m-%d'),
        'ds_yesterday_nodash': datetime.strftime(current_date - timedelta(1), '%Y%m%d'),
        'ds_tomorrow': datetime.strftime(current_date + timedelta(1), '%Y-%m-%d'),
        'ds_tomorrow_nodash': datetime.strftime(current_date + timedelta(1), '%Y%m%d')
    }

def valid_date(s):
    """

    :param s: date string
    :return: python datetime object
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise ArgumentTypeError(msg)


def apply_template_values(template_string, template_fields={}, execution_date=datetime.now()):
    """
     :param string: string that need to be replace the template values
     :return:       """
    apply_date_templates = Template(template_string).render(**date_template(execution_date=execution_date))
    return Template(apply_date_templates).render(**template_fields)


def read_from_file(file_path):
    """

    :param file_path: full absolute path of the file that need to be read
    :return: return string content of the file
    """
    return open(file_path).read()

