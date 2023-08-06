import inspect

from types import SimpleNamespace
from functools import lru_cache
from . import Entity
from pysimba.entities.campaign import Campaign
from pysimba.client.utils import batch, get


class Customer(Entity):
    @property
    @lru_cache(maxsize=None)
    def seller(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=21349&docType=2
        """
        r = self.client.call('taobao.user.seller.get', params={
            'fields': ','.join([
                'user_id',
                'nick',
                'sex',
                'seller_credit',
                'type',
                'has_more_pic',
                'item_img_num',
                'item_img_size',
                'prop_img_num',
                'prop_img_size',
                'auto_repost',
                'promoted_type',
                'status',
                'alipay_bind',
                'consumer_protection',
                'avatar',
                'liangpin',
                'sign_food_seller_promise',
                'has_shop',
                'is_lightning_consignment',
                'has_sub_stock',
                'is_golden_seller',
                'magazine_subscribe',
                'vertical_market',
                'online_gaming',
                'vip_info'
            ])
        }, token=self.token)
        
        return SimpleNamespace(**get(r, path='user_seller_get_response.user'))

    @property
    def campaigns(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10557&docType=2
        """
        r = self.client.call('taobao.simba.campaigns.get', token=self.token)
        
        return [Campaign(x['campaign_id'], owner=self, **x) for x in get(r, path='simba_campaigns_get_response.campaigns.campaign', default=[])]
