file = """from script_config import *
import pandas as pd
from CriteoPy import AXDBTools, AXOutTools
import argparse

def GetCommandLineArgs():

    oParser = argparse.ArgumentParser(description="")
    hArgs = dict()
    oParser.add_argument('-sd','--start_date', help = 'start date of the study', type=str, required=True)
    oParser.add_argument('-ed','--end_date', help = 'end date of the study', type=str, required = True)
    oParser.add_argument('-rd','--report_date', help = 'original date the report should have run', type=str, required = True)
           
    return hArgs

def main():
    if kind_of_query != 'vertica':
        raise NotImplementedError("This kind of query hasn't been implemented yet.")

    oAXD = AXDBTools()
    connection = oAXD.GetoDbh()

    # read the query
    with open('queries\\query.sql', 'r') as f:
        query = f.read()

    # run the query
    results = pd.read_sql(query, connection)

    # assign the filename for the output
    filename = 'outputs\\output_file'

    # write the results to a file
    if output_type == 'csv':
        filename += '.csv'
        results.to_csv(filename, index=False)

    elif output_type == 'excel':
        filename += '.xlsx'
        results.to_excel(filename, index=False)

    # send an email with the report
    email = AXOutTools()

    email_args = {
        'sTo': destination_emails,
        'sFrom': email_sender,
        'sSubject': email_subject,
        'sBody': email_body,
        'aAttachments': [filename]
    }

    email.SendEmail(email_args)

if __name__ == '__main__':
    hArgs = GetCommandLineArgs()
    main()


"""