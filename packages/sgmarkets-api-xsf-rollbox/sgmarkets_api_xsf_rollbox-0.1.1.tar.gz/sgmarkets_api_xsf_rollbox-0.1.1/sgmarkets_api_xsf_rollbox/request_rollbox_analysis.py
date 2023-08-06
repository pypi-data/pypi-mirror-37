

from timeit import default_timer as timer
from IPython.display import display, Markdown

from ._util import Util
from .response_rollbox_analysis import ResponseRollboxAnalysis


class RequestRollboxAnalysis:
    """
    """

    def __init__(self,
                 analysisTypes=None,
                 underlying=None,
                 rollKey=None,
                 startDate=None,
                 endDate=None,
                 relativeRoll=+4):
        """
        """
        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/frb',
                   'endpoint': '/v1/analysis'}
        self.url = Util.build_url(dic_url)

        if analysisTypes is None:
            analysisTypes = ['Global',
                             'PriceEvolution',
                             'VolumeAtPrice',
                             'OpenInterest',
                             'RelativeRollOpenInterest']

        self.dic_input = {
            'analysisTypes': analysisTypes,
            'underlying': underlying,
            'rollKey': rollKey,
            'startDate': startDate,
            'endDate': endDate,
            'relativeRoll': relativeRoll,
        }
        self.dic_api = self.dic_input

    def info(self):
        """
        """
        md = """
A RequestRollboxRelativeRoll object has the properties:
+ `url`: {}
+ `dic_input`: user input (dictionary)

and the methods:
+ `call_api()` to make the request to the url
""".format(self.url)
        return Markdown(md)

    def call_api(self,
                 api,
                 debug=False):
        """
        See https://analytics-api.sgmarkets.com/frb/swagger/ui/index#!/Explore/Explore_02
        """
        t0 = timer()
        print('calling API...')
        raw_response = api.post(self.url, payload=self.dic_api)
        t1 = timer()
        print('done in {:.2f} s'.format(t1 - t0))
        if debug:
            print('*** START DEBUG ***\n{}\n*** END DEBUG ***'.format(raw_response))
        response = ResponseRollboxAnalysis(raw_response, self.dic_api)
        return response
