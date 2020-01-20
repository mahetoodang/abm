import pandas as pd
import numpy as np
import webbrowser
import os
from pandas_profiling import ProfileReport

def create_model_report():
    df = pd.read_csv('data/sim_stats_30agents.csv')

    profile = ProfileReport(df, title="30 Agent Model")

    model_report_name = 'model_report' + '.html'

    profile.to_file(output_file="model_report.html")

    model_report_path = os.getcwd() + '/' + model_report_name

    new = 2 # open in a new tab, if possible

    return webbrowser.open(model_report_path, new=new)