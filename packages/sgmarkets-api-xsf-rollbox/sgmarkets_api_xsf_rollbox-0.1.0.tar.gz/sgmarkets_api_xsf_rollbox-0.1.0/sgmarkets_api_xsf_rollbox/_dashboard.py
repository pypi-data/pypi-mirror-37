

import os
import json

import ezdashboard as ed
from ezdashboard.elements import Div, ListDiv, Title, Row, Tab, ListJs, Misc, Header, Dashboard


class MyDashboard:
    """
    """

    def __init__(self,
                 undl,
                 rollKey,
                 data,
                 name='dashboard_rollbox',
                 folder_save='dump',
                 verbose=True,
                 **kwargs):
        """
        """
        self.undl = undl
        self.rollKey = rollKey
        self.data_in = data
        self.verbose = verbose
        self.name = name
        self.folder_save = folder_save

        here = os.path.dirname(__file__)
        self.path_img = {}
        self.path_img['sg'] = os.path.join(here, 'img', 'sg-logo.png')
        self.path_img['jupyter'] = os.path.join(here, 'img', 'jupyter-logo.png')

    def build(self):
        """
        """
        dic_div = {}
        widgets_state = []

        for name, df, plot_html, grid_div_html, grid_state_json in self.data_in:
            dic_div[name] = Div(**{
                # 'id_name': 'myname-'+str(name),
                # 'class_name': 'my-style-'+str(name),
                'content': plot_html,
                'width': 12,
                'with_borders': False,
                'is_markdown': False
            })
            dic_div['grid_div_'+name] = Div(**{
                # 'id_name': 'myname-'+str(name),
                # 'class_name': 'my-style-'+str(name),
                'content': grid_div_html,
                'width': 12,
                'with_borders': False,
                'is_markdown': False
            })
            widgets_state.append(json.loads(grid_state_json))

        css = """
        /* IMPORTANT: tile is a KEYWORD */
        /* It is the class of all display divs in the dashboard tabs */
        .tile {
            padding: 15px;
            margin: 17.5px;
            font-size: 1.6rem;
        }
        .nav-tab {
        font-family: 'Source Sans Pro', Arial, sans-serif;
        color: #333333;
        }
        /* IMPORTANT: tile is a KEYWORD */
        /* It is the class of all display divs in the dashboard tabs */
        .header img.left-logo {
        width: 46px;
        height: 46px;
        }
        .header img.right-logo {
        width: 46px;
        height: 46px;
        }
        .wrapper {
        width: 1250px;
        margin-top: 15px;
        }
        """

        # tab
        name = 'price_evolution_1'

        d = dic_div[name]
        li_d = ListDiv(**{'elmts': [d]})
        row = Row(**{'elmts': li_d})
        tab11 = Tab(**{'name': 'Plot', 'elmts': [row], 'level': 2, 'active': True})

        d = dic_div['grid_div_'+name]
        li_d = ListDiv(**{'elmts': [d]})
        row = Row(**{'elmts': li_d})
        tab12 = Tab(**{'name': 'Table', 'elmts': [row], 'level': 2, 'keyboard': False})

        tab1 = Tab(**{'name': 'Price & Volume', 'elmts': [tab11, tab12], 'active': True})

        # tab
        name = 'volume_price'

        d = dic_div[name]
        li_d = ListDiv(**{'elmts': [d]})
        row = Row(**{'elmts': li_d})
        tab21 = Tab(**{'name': 'Plot', 'elmts': [row], 'level': 2, 'active': True})

        d = dic_div['grid_div_'+name]
        li_d = ListDiv(**{'elmts': [d]})
        row = Row(**{'elmts': li_d})
        tab22 = Tab(**{'name': 'Table', 'elmts': [row], 'level': 2, 'keyboard': False})

        tab2 = Tab(**{'name': 'Volume vs. Price', 'elmts': [tab21, tab22]})

        # tab
        name = 'open_interest'

        d = dic_div[name]
        li_d = ListDiv(**{'elmts': [d]})
        row = Row(**{'elmts': li_d})
        tab31 = Tab(**{'name': 'Plot', 'elmts': [row], 'level': 2, 'active': True})

        d = dic_div['grid_div_'+name]
        li_d = ListDiv(**{'elmts': [d]})
        row = Row(**{'elmts': li_d})
        tab32 = Tab(**{'name': 'Table', 'elmts': [row], 'level': 2, 'keyboard': False})

        tab3 = Tab(**{'name': 'Open Interest', 'elmts': [tab31, tab32]})

        # tab
        name = 'relative_open_interest'

        d = dic_div[name]
        li_d = ListDiv(**{'elmts': [d]})
        row = Row(**{'elmts': li_d})
        tab41 = Tab(**{'name': 'Plot', 'elmts': [row], 'level': 2, 'active': True})

        d = dic_div['grid_div_'+name]
        li_d = ListDiv(**{'elmts': [d]})
        row = Row(**{'elmts': li_d})
        tab42 = Tab(**{'name': 'Table', 'elmts': [row], 'level': 2, 'keyboard': False})

        tab4 = Tab(**{'name': 'Open Interest Variations', 'elmts': [tab41, tab42]})

        js = ListJs([''])

        title = Title(**{'size': 2,
                         'text': 'Rollbox Futures Data for {} - {}'.format(self.undl,
                                                                           self.rollKey)})

        misc = Misc(**{'main_type': 'container-fluid',
                       'main_class_name': 'wrapper',
                       'main_nav_width': '17%',
                       'main_nav_min_height': '15%',
                       'main_content_width': '82%',
                       'no_margins': False,
                       })

        header = Header(**{'left_logo': self.path_img['sg'],
                           'left_title': 'SG',
                           'right_logo': self.path_img['jupyter'],
                           'toggle': False
                           })

        self.dashboard = Dashboard(**{'title': title,
                                      'tabs': [tab1, tab2, tab3, tab4],
                                      'css': css,
                                      'js': js,
                                      'misc': misc,
                                      'header': header,
                                      'markdown': False,
                                      'widgets': True,
                                      'widgets_state': widgets_state,
                                      'latex': False
                                      }, verbose=self.verbose)
        self.data = self.dashboard.to_dict()

    def save(self):
        """
        """
        ed.build(self.data,
                 save=True,
                 save_path=self.folder_save)
