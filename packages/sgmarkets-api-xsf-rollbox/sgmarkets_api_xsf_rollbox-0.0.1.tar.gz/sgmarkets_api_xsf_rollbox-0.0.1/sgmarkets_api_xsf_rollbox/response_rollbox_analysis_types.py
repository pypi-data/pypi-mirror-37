
import pandas as pd

from IPython.display import Markdown

from sgmarkets_api_auth.util import save_result


class ResponseRollboxAnalysisTypes:
    """
    """

    def __init__(self,
                 raw_data=None):
        """
        """
        msg1 = 'Error: data returned by API must be a dict - Run call_api() again with debug=True'
        msg2 = 'Error: "analysisTypes" must be a key of the dict - Run call_api() again with debug=True'
        msg3 = 'Error: data["analysisTypes"] must be a list - Run call_api() again with debug=True'

        assert isinstance(raw_data, dict), msg1
        assert 'analysisTypes' in raw_data, msg2
        assert isinstance(raw_data['analysisTypes'], list), msg3

        self.raw_data = raw_data['analysisTypes']
        self.li_res = self._build_df_res()

    def _build_df_res(self):
        """
        """
        data = self.raw_data
        li_analysis_types = data
        return li_analysis_types

    def info(self):
        """
        """
        md = """
A ResponseRollboxAnalysisTypes object has the properties:
+ `li_res`: response data (list)

+ `raw_data`: raw data in response under key 'analysisTypes' (list)
"""
        return Markdown(md)
