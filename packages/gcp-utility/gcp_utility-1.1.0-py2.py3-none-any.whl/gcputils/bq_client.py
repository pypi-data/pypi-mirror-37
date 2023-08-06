import argparse
import sys
import logging
from utils.bigquery_utils import BigQueryUtils
from utils.common_utils import *

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


class BigQueryClient:

    def __init__(self, args):
        """

        :param args: argparse Namespace instance which contains list of command line args
        """

        self.bq_utils = BigQueryUtils(project=args.project)
        self.template_fields = self.read_from_file(args.template_file) if args.template_file else args.template
        self.start_date = args.start_date if args.start_date else datetime.now()
        self.end_date = args.end_date if args.end_date else self.start_date
        self.date_diff = self.end_date - self.start_date

        if args.service_account_path:
            self.service = self.bq_utils.get_connection(service_account_file_path=args.service_account_path)
        else:
            self.service = self.bq_utils.get_connection()


    def read_from_file(self, file_path):
        """

        :param file_path: full absolute path of the file that need to be read
        :return: return string content of the file
        """
        return open(file_path).read()

    def controller(self, args):
        """

        :param args: Namespace object which contains list of arguments
        :return:
        """
        start_date = self.start_date
        end_date = self.end_date
        while end_date >= start_date: # backfilling
            logging.info("Executing query for {}".format(datetime.strftime(start_date, "%Y-%d-%m")))

            if args.query or args.query_file:

                query_string = apply_template_values(args.query if args.query else self.read_from_file(args.query_file), execution_date=start_date)

                if args.destination_table:
                    try:
                        assert len(args.destination_table.split(':')) <= 1
                        assert len(args.destination_table.split('.')) == 2
                    except Exception, e:
                        raise argparse.ArgumentError("destination table is not in proper format <datasetid>.<tableid>")

                    dataset_id, table_id = args.destination_table.split('.')

                    table_id = apply_template_values(table_id, self.template_fields, execution_date=start_date)
                    logging.info("----------------------------")
                    logging.info("table name - %s", table_id)
                    logging.info("----------------------------")
                    try:

                        logging.info("bq job initiated for date - {}".format(datetime.strftime(start_date, "%Y-%m-%d")))
                        self.bq_utils.query_to_table(self.service,
                                                     query=query_string,
                                                     dest_dataset_id=dataset_id,
                                                     dest_table_id=table_id,
                                                     flattern_results=args.flattern_results,
                                                     write_disposition=args.write_desposition,
                                                     use_standard_sql=bool(args.ssql))
                        logging.info("Successfully completed for date - {}".format(datetime.strftime(start_date, "%Y-%m-%d  ")))
                    except Exception, e:
                        logging.info("Something went wrong for date {}".format(datetime.strftime(start_date, "%Y-%m-%d")))
                        logging.info(e)
            else:
                logging.info("Please provide destination details")


            start_date = start_date + timedelta(1)


def main():
    parser = argparse.ArgumentParser(version="0.1", description="Bq utility tool")
    parser.add_argument("-q", "--query", dest="query", help="provide valid bigquery sql")
    parser.add_argument("-f", "--no-flattern", dest="flattern_results", action="store_true", default=True, help="Flattern results")
    parser.add_argument("-p", "--project_id", default=None, dest="project", help="provide valid project id")
    parser.add_argument("-ssql", "--standard-sql", dest="ssql", default=False, action="store_true", help="Mention if using Standard sql")
    parser.add_argument("-d", "--destination-table", dest="destination_table", help="<projectname>:<datasetid>.<tableid> provide valid destination project-id")
    parser.add_argument("-w", "--write-desposition", default='WRITE_IF_EMPTY', dest="write_desposition", help="Write disposition value")
    parser.add_argument("-qf", "--query-file", dest="query_file", help="provide bigquery sql filepath")
    parser.add_argument("-t", "--template", default={}, dest="template", help="provide template values")
    parser.add_argument("-tf", "--template-file", dest="template_file", help="provide template file path")
    parser.add_argument("-s", "--start-date", dest="start_date", help="Provide valid startdate (YYYY-MM-DD)", type=valid_date)
    parser.add_argument("-e", "--end-date", dest="end_date", help="Provide valid end date (YYYY-MM-DD)", type=valid_date)
    parser.add_argument("-sf", "--service-account-file-path", dest="service_account_path", help="provide valid path of service account json file")
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        exit()

    bq_client = BigQueryClient(args)
    bq_client.controller(args)

    # t = Thread(target=bq_client.controller, kwargs={'args':args})
    # t.start()
    # timeout = 30.0
    #
    # while t.isAlive():
    #     time.sleep(0.1)
    #     timeout -= 0.1
    #     if timeout == 0.0:
    #         print 'Please wait...'
    #         timeout = 30.0

