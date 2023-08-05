

from timeit import default_timer as timer
from IPython.display import display, Markdown

from ._util import Util
from .response_rollbox_relative_roll import ResponseRollboxRelativeRoll


class RequestRollboxRelativeRoll:
    """
    """

    def __init__(self,
                 underlying=None,
                 rollKey=None,
                 relativeRoll=+4):
        """
        """
        dic_url = {'base_url': 'https://analytics-api.sgmarkets.com',
                   'service': '/frb',
                   'endpoint': '/v1/relative-roll'}
        self.url = Util.build_url(dic_url)

        self.dic_input = {
            'underlying': underlying,
            'rollKey': rollKey,
            'relativeRoll': relativeRoll,
        }

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
        self.dic_api = self.dic_input
        raw_response = api.get(self.url, payload=self.dic_api)
        t1 = timer()
        print('done in {:.2f} s'.format(t1 - t0))
        if debug:
            print('*** START DEBUG ***\n{}\n*** END DEBUG ***'.format(raw_response))
        response = ResponseRollboxRelativeRoll(raw_response, self.dic_api)
        return response
