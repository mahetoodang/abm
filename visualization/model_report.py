import pandas as pd
import numpy as np
import webbrowser
import os
import glob
from pandas_profiling import ProfileReport

def create_model_report(html_report=True):
    if html_report == True:
        file_list = glob.glob('data/stats/*')
        latest_file = max(file_list, key=os.path.getctime)
        df = pd.read_csv(latest_file)
        profile = ProfileReport(df, title="Profiling Report")
        output_file = 'data/html/model_report.html'
        profile.to_file(output_file=output_file)
        model_report_path = os.getcwd() + '/' + output_file
        new = 2 # open in a new tab, if possible
        return webbrowser.open(model_report_path, new=new)
    else:
        pass

if __name__ == '__main__':
    create_model_report(True)
