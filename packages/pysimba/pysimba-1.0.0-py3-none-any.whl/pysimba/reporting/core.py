from functools import partial
from enum import Enum, auto
from datetime import datetime, timedelta
from functools import lru_cache
from delorean import Delorean


class TrafficTypes(Enum):
    SEARCH = 'SEARCH'
    TARGETING = 'NOSEARCH'


class TrafficSourceTypes(Enum):
    COMPUTER_ONSITE = '1'
    COMPUTER_OFFSITE = '2'
    MOBILE_ONSITE = '4'
    MOBILE_OFFSITE = '5'


class DateRangeTypes(Enum):
    TODAY = auto()
    YESTERDAY = auto()
    LAST_7_DAYS = auto()
    LAST_WEEK = auto()
    LAST_BUSINESS_WEEK = auto()
    THIS_MONTH = auto()
    LAST_MONTH = auto()
    ALL_TIME = auto()
    CUSTOM_DATE = auto()
    LAST_14_DAYS = auto()
    LAST_30_DAYS = auto()
    THIS_WEEK_SUN_TODAY = auto()
    THIS_WEEK_MON_TODAY = auto()
    LAST_WEEK_SUN_SAT = auto()
    
    @property
    def today(self):
        return Delorean(timezone='Asia/Shanghai').date

    @property
    def yesterday(self):
        return self.today - timedelta(days=1)

    @property
    def value(self):
        if self.name == 'TODAY':
            return self.today
        elif self.name == 'YESTERDAY':
            return self.yesterday, self.yesterday
        elif self.name == 'LAST_7_DAYS':
            return self.yesterday - timedelta(days=6), self.yesterday
        elif self.name == 'LAST_30_DAYS':
            return self.yesterday - timedelta(days=29), self.yesterday
        else:
            raise NotImplementedError


class Reporter:
    def __init__(self, ad, date=None, start_date=None, end_date=None): 
        if date != DateRangeTypes.CUSTOM_DATE and date != DateRangeTypes.TODAY:
            start_date, end_date = date.value

        self.ad = ad
        self.date = date
        self.start_date = start_date
        self.end_date = end_date

    @property
    @lru_cache(maxsize=None)
    def token(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10950&docType=2
        """
        campaign = self.ad.owner
        customer = campaign.owner

        r = self.ad.client.call('taobao.simba.login.authsign.get', token=customer.token)
        return r['simba_login_authsign_get_response']['subway_token']
    
    def report(self):
        """
        Refs:
            1. http://open.taobao.com/api.htm?docId=25052&docType=2
            2. http://open.taobao.com/api.htm?docId=10953&docType=2
            3. http://open.taobao.com/api.htm?docId=10952&docType=2
        """
        campaign = self.ad.owner
        customer = campaign.owner
        
        if self.date == DateRangeTypes.TODAY:
            r = self.ad.client.call('taobao.simba.rtrpt.bidword.get', params={
                'campaign_id': campaign.entity_id,
                'adgroup_id': self.ad.entity_id,
                'the_date': self.date.value.strftime('%Y-%m-%d')
            }, token=customer.token)

            try:
                return r['simba_rtrpt_bidword_get_response']['results']['rt_rpt_result_entity_d_t_o']
            except KeyError:
                return []
        else:
            call = partial(self.ad.client.call, params={
                'campaign_id': campaign.entity_id,
                'adgroup_id': self.ad.entity_id,
                'start_time': self.start_date.strftime('%Y-%m-%d'),
                'end_time': self.end_date.strftime('%Y-%m-%d'),
                'source': ','.join([
                    TrafficSourceTypes.COMPUTER_ONSITE.value,
                    TrafficSourceTypes.COMPUTER_OFFSITE.value,
                    TrafficSourceTypes.MOBILE_ONSITE.value,
                    TrafficSourceTypes.MOBILE_OFFSITE.value
                ]),
                'subway_token': self.token,
                'page_no': 1,
                'page_size': 100000000,
                'search_type': ','.join([
                    TrafficTypes.SEARCH.value,
                    TrafficTypes.TARGETING.value
                ])
            }, token=customer.token)

            basic_report = call('taobao.simba.rpt.adgroupkeywordbase.get')['simba_rpt_adgroupkeywordbase_get_response']['rpt_adgroupkeyword_base_list']
            advanced_report = call('taobao.simba.rpt.adgroupkeywordeffect.get')['simba_rpt_adgroupkeywordeffect_get_response']['rpt_adgroupkeyword_effect_list']

            if len(basic_report) != len(advanced_report):
                raise ValueError

            return [{**b, **a} for b, a in zip(basic_report, advanced_report)]
