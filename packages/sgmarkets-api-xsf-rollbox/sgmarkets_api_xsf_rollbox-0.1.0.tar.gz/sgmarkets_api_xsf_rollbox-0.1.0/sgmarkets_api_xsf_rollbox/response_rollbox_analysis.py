
import pandas as pd

from IPython.display import display, HTML, Markdown
from copy import deepcopy as copy

from sgmarkets_api_auth.util import save_result

from ._plot import Plot
from ._util import Util
from ._dashboard import MyDashboard


pd.options.mode.chained_assignment = None


class ResponseRollboxAnalysis:
    """
    TBU
    """

    def __init__(self,
                 raw_data=None,
                 dic_req=None):
        """
        """
        msg1 = 'Error: data returned by API must be a dict - Run call_api() again with debug=True'

        assert isinstance(raw_data, dict), msg1

        self.dic_req = dic_req
        self.raw_data = raw_data
        self.dic_res = self._build_dic_res()

    def _build_dic_res(self):
        """
        """
        data = self.raw_data
        dic = {}

        for k, v in data.items():

            if k == 'globalAnalysis':
                df = pd.DataFrame(pd.Series(v),
                                  columns=['value'])
                dic[k] = df

            if k == 'priceEvolutionAnalysis':
                df = pd.DataFrame(v)
                df['date'] = pd.to_datetime(df['date'])
                df = df[['date',
                         'bid',
                         'ask',
                         'trade',
                         'volume']]
                dic[k] = df

            if k == 'volumeAtPriceAnalysis':
                df = pd.DataFrame(v)
                dic[k] = df

            if k == 'openInterestAnalysis':
                df = pd.DataFrame(v)
                df['date'] = pd.to_datetime(df['date'])
                df = df[['date',
                         'currentRollOpenInterest',
                         'nextRollOpenInterest',
                         'totalOpenInterest']]
                dic[k] = df

            if k == 'relativeRollOpenInterestAnalysis':
                for k2, v2 in v.items():

                    if k2 == 'relativeOpenInterestAnalysis':
                        df = pd.DataFrame(v2)
                        dic[k2] = df

                    if k2 == 'relativeTotalInterestAnalysis':
                        df = pd.DataFrame(v2)
                        dic[k2] = df

        return dic

    def plot_priceEvolution(self,
                            save=False,
                            folder_save='dump',
                            name='plot_price_evolution',
                            tagged=False,
                            x_axis_ordinal=False,
                            show=True):
        """
        """
        dfi = self.dic_res['priceEvolutionAnalysis']
        undl = self.dic_req['underlying']
        rollKey = self.dic_req['rollKey']
        df, html = Plot.price_evolution(dfi,
                                        undl,
                                        rollKey,
                                        save=save,
                                        folder_save=folder_save,
                                        name=name,
                                        tagged=tagged,
                                        x_axis_ordinal=x_axis_ordinal)
        if show:
            display(HTML(html))
        else:
            return df, html

    def plot_volumeAtPrice(self,
                           save=False,
                           folder_save='dump',
                           name='plot_volume_price',
                           tagged=False,
                           x_axis_ordinal=False,
                           show=True):
        """
        """
        dfi = self.dic_res['volumeAtPriceAnalysis']
        undl = self.dic_req['underlying']
        rollKey = self.dic_req['rollKey']
        df, html = Plot.volume_price_analysis(dfi,
                                              undl,
                                              rollKey,
                                              save=save,
                                              folder_save=folder_save,
                                              name=name,
                                              tagged=tagged,
                                              x_axis_ordinal=x_axis_ordinal)

        if show:
            display(HTML(html))
        else:
            return df.reset_index(), html

    def plot_openInterest(self,
                          save=False,
                          folder_save='dump',
                          name='plot_open_interest',
                          tagged=False,
                          x_axis_ordinal=False,
                          show=True):
        """
        """
        dfi = self.dic_res['openInterestAnalysis']
        undl = self.dic_req['underlying']
        rollKey = self.dic_req['rollKey']
        df, html = Plot.open_interest_analysis(dfi,
                                               undl,
                                               rollKey,
                                               save=save,
                                               folder_save=folder_save,
                                               name=name,
                                               tagged=tagged,
                                               x_axis_ordinal=x_axis_ordinal)
        if show:
            display(HTML(html))
        else:
            return df.reset_index(), html

    def plot_relativeTotalInterest(self,
                                   save=False,
                                   folder_save='dump',
                                   name='plot_relative_total_interest',
                                   tagged=False,
                                   x_axis_ordinal=False,
                                   show=True):
        """
        """
        dfi1 = self.dic_res['priceEvolutionAnalysis']
        dfi2 = self.dic_res['relativeTotalInterestAnalysis']
        undl = self.dic_req['underlying']
        rollKey = self.dic_req['rollKey']
        ts = dfi1['date'].iloc[-1].round('D')
        dfi2['date'] = [ts + e*pd.offsets.Day() for e in dfi2['dateOffset']]
        df = dfi2[['date', 'ratio']]
        df.loc[:, 'delta'] = df['ratio'].shift(1)-df['ratio']
        df.loc[:, 'delta'] = df['delta'].fillna(0)
        df, html = Plot.relative_total_interest_analysis(df,
                                                         undl,
                                                         rollKey,
                                                         save=save,
                                                         folder_save=folder_save,
                                                         name=name,
                                                         tagged=tagged,
                                                         x_axis_ordinal=x_axis_ordinal)
        if show:
            display(HTML(html))
        else:
            return df.reset_index(), html

    def build_dashboard(self,
                        save=False,
                        folder_save='dump',
                        verbose=True):
        """
        """
        data = []

        for name, func, kwargs in [
            ('price_evolution_1', self.plot_priceEvolution, {}),
            ('price_evolution_2', self.plot_priceEvolution, {'x_axis_ordinal': True}),
            ('volume_price', self.plot_volumeAtPrice, {}),
            ('open_interest', self.plot_openInterest, {}),
            ('relative_open_interest', self.plot_relativeTotalInterest, {}),
        ]:
            df, html = func(save=True,
                            folder_save=folder_save,
                            name='plot_'+name,
                            show=False,
                            **kwargs
                            )
            df = df.reset_index(drop=True)
            Plot.build_grid(df,
                            folder_save=folder_save,
                            name_div='grid_div_'+name,
                            name_state='grid_state_'+name)
            data.append([name,
                         df.copy(),
                         Util.load(folder_save, 'plot_{}.html'.format(name)),
                         Util.load(folder_save, 'grid_div_{}.html'.format(name)),
                         Util.load(folder_save, 'grid_state_{}.json'.format(name)),
                         ])

        undl = self.dic_req['underlying']
        rollKey = self.dic_req['rollKey']
        dashboard = MyDashboard(undl,
                                rollKey,
                                data,
                                folder_save=folder_save,
                                name=name,
                                verbose=verbose)
        dashboard.build()
        dashboard.save()

    def save(self,
             folder_save='dump',
             tagged=True,
             excel=False):
        """ 
        """
        for k, df in self.dic_res.items():
            name = 'SG_ROLLBOX_Analysis_'+k
            save_result(df,
                        folder_save,
                        name=name,
                        tagged=tagged,
                        excel=excel)

    def info(self):
        """
        """
        md = """
A ResponseRollboxRelativeRoll object has the properties:
+ `dic_req`: request data (dict)
+ `dic_res`: response data (dict of dataframes)

+ `raw_data`: raw data in response (dictionary)

and the methods:
+ `save()` to save the data as several `.csv` or `.xlsx` files
"""
        return Markdown(md)
