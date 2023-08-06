from . import Entity
from enum import Enum
from pysimba.entities.keyword import Keyword, MatchingOptions
from pysimba.entities.creative import Creative
from pysimba.client.utils import batch, get


class ComputerRankRange(Enum):
    INVALID = '-'
    CREATIVE_OFFLINE = '-2'
    CAMPAIGN_OFFLINE = '-1'
    HOME_LEFT = '0'
    HOME_RIGHT_FIRST = '1'
    HOME_RIGHT_SECOND = '2'
    HOME_RIGHT_THIRD = '3'
    HOME_RIGHT_NOT_TOP_THREE = '4'
    PAGE_2 = '5'
    PAGE_3 = '6'
    PAGE_4 = '7'
    PAGE_5 = '8'
    AFTER_PAGE_5 = '9'


class MobileRankRange(Enum):
    INVALID = '-'
    CREATIVE_OFFLINE = '-2'
    CAMPAIGN_OFFLINE = '-1'
    TOP_ONE = '0'
    TOP_THREE = '1'
    FROM_4_TO_6 = '3'
    FROM_7_TO_10 = '6'
    FROM_11_TO_15 = '10'
    FROM_16_TO_20 = '11'
    AFTER_20 = '12'


class Ad(Entity):
    def enable(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10539&docType=2
        """
        campaign = self.owner
        customer = campaign.owner

        self.client.call('taobao.simba.adgroup.update', params={
            'adgroup_id': self.entity_id,
            'online_status': 'online'
        }, token=customer.token)

    def disable(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10539&docType=2
        """
        campaign = self.owner
        customer = campaign.owner

        self.client.call('taobao.simba.adgroup.update', params={
            'adgroup_id': self.entity_id,
            'online_status': 'offline'
        }, token=customer.token)

    @property
    def keywords(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=21682&docType=2
        """
        campaign = self.owner
        customer = campaign.owner

        r = self.client.call('taobao.simba.keywordsbyadgroupid.get', params={
            'adgroup_id': self.entity_id,
        }, token=customer.token)

        return [Keyword(x['keyword_id'], owner=self, **x) for x in get(r, path='simba_keywordsbyadgroupid_get_response.keywords.keyword', default=[])]

    @property
    def creatives(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10530&docType=2
        """
        campaign = self.owner
        customer = campaign.owner

        r = self.client.call('taobao.simba.creatives.get', params={
            'adgroup_id': self.entity_id,
        }, token=customer.token)

        return [Creative(x['creative_id'], owner=self, **x) for x in get(r, path='simba_creatives_get_response.creatives.creative', default=[])]

    def create_keywords(self, texts):
        """
        Ref: http://open.taobao.com/api.htm?docId=21681&docType=2
        """
        campaign = self.owner
        customer = campaign.owner
        
        r = self.client.call('taobao.simba.keywordsvon.add', params={
            'adgroup_id': self.entity_id,
            'keyword_prices': json.dumps([{
                'word': text,
                'maxPrice': int(5.0),
                'matchScope': MatchingOptions.EXACT_MATCH
            } for text in texts])
        }, token=customer.token)
        
        return [Keyword(x['keyword_id'], owner=self, **x) for x in get(r, path='simba_keywordsvon_add_response.keywords.keyword', default=[])]

    def update_keywords(self, payloads):
        """
        Ref: http://open.taobao.com/api.htm?docId=21685&docType=2
        """
        campaign = self.owner
        customer = campaign.owner
        
        _payloads = []
        for payload in payloads:
            _payload = dict()
            _payload['keywordId'] = payload['entity_id']

            if 'bidding' in payload:
                if 'computer' in payload['bidding']:
                    _payload['maxPrice'] = int(payload['bidding']['computer'])
                if 'mobile' in payload['bidding']:
                    _payload['maxMobilePrice'] = int(payload['bidding']['mobile'])

            if 'matching' in payload:
                _payload['matchScope'] = payload['matching']

            _payloads.append(_payload)

        r = self.client.call('taobao.simba.keywords.pricevon.set', params={
            'keywordid_prices': json.dumps(_payloads)
        }, token=customer.token)

        return [Keyword(x['keyword_id'], owner=self, **x) for x in get(r, path='simba_keywords_pricevon_set_response.keywords.keyword', default=[])]


    def delete_keywords(self, entity_ids):
        """
        Ref: http://open.taobao.com/api.htm?docId=10554&docType=2
        """
        campaign = self.owner
        customer = campaign.owner

        r = self.client.call('taobao.simba.keywords.delete', params={
            'campaign_id': campaign.entity_id,
            'keyword_ids': ','.join(entity_ids)
        }, token=customer.token)

        return [Keyword(x['keyword_id'], owner=self, **x) for x in get(r, path='simba_keywords_delete_response.keywords.keyword', default=[])]

    @batch(20)
    def query_keyword_ranks(self, entity_ids):
        """
        Ref: http://open.taobao.com/api.htm?docId=26824&docType=2
        """
        campaign = self.owner
        customer = campaign.owner

        r = self.client.call('taobao.simba.keywords.realtime.ranking.batch.get', params={
            'nick': customer.seller.nick,
            'ad_group_id': self.entity_id,
            'bidword_ids': ','.join(entity_ids)
        }, token=customer.token)

        # TODO: add retry logic if `result.success == False`
        #       or `realtime_rank_list.stat == 1`

        # return [{
        #     'entity_id': x['bidwordid'],
        #     'computer': ComputerRankRange(x['pc_rank']),
        #     'mobile': MobileRankRange(x['mobile_rank'])
        # } for x in get(r, path='simba_keywords_realtime_ranking_batch_get_response.result.realtime_rank_list.result', default=[])]

        return get(r, path='simba_keywords_realtime_ranking_batch_get_response.result.realtime_rank_list.result', default=[])
