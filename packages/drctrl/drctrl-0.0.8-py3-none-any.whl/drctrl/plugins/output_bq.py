import pandas as pd
from drctrl.plugins.base import BaseOutput
from drctrl.lib.rsdf import rsdf

class OutputBQ(BaseOutput):
    def __init__(self, **kwargs):

    def preprocess(self):
        pass

    def output(self, df, exists='replace'):
        return True

