
import pandas as pd

from IPython.display import Markdown
from copy import deepcopy as copy

from sgmarkets_api_auth.util import save_result


class ResponseRollboxUnderlyings:
    """
    TBU
    """

    def __init__(self,
                 raw_data=None,
                 dic_req=None):
        """
        """
        msg1 = 'Error: data returned by API must be a dict - Run call_api() again with debug=True'
        msg2 = 'Error: "underlyings" must be a key of the dict - Run call_api() again with debug=True'
        msg3 = 'Error: data["underlying"] must be a list - Run call_api() again with debug=True'

        assert isinstance(raw_data, dict), msg1
        assert 'underlyings' in raw_data, msg2
        assert isinstance(raw_data['underlyings'], list), msg3

        self.dic_req = dic_req
        self.raw_data = raw_data['underlyings']
        self.df_res = self._build_df_res()

    def _build_df_res(self):
        """
        """
        data = self.raw_data

        li = []
        for e in data:
            d = {}
            for k in ['indexLongName']:
                d[k] = e[k]
            for e2 in e['futureRolls']:
                d2 = copy(d)
                for k, v in e2.items():
                    d2[k] = v
            li.append(d2)

        df = pd.DataFrame(li)
        df = df.rename(columns={'underlying': 'undl',
                                'indexLongName': 'undlLongName'})
        df = df[['undl',
                 'undlLongName',
                 'rollKey',
                 'currentFuture',
                 'nextFuture',
                 'startDate',
                 'endDate',
                 'firstTradeDate',
                 'lastTradeDate']]
        return df

    def save(self,
             folder_save='dump',
             name=None,
             tagged=True,
             excel=False):
        """ 
        """
        if name is None:
            name = 'SG_ROLLBOX_Underlyings'

        save_result(self.df_res,
                    folder_save,
                    name=name,
                    tagged=tagged,
                    excel=excel)

    def _repr_html_(self):
        """
        """
        return self.df_res.to_html()

    def info(self):
        """
        """
        md = """
A ResponseRollboxUnderlyings object has the properties:
+ `dic_req`: request data (dict)
+ `df_res`: response data (dataframe)

+ `raw_data`: raw data in response under key 'underlyings' (dictionary)

and the methods:
+ `save()` to save the data as `.csv` and `.xlsx` files
        """
        return Markdown(md)
