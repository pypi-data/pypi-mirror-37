from . import Entity
from pysimba.entities.ad import Ad
from pysimba.client.utils import batch, get


class Campaign(Entity):
    @property
    def budget(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10549&docType=2
        """
        customer = self.owner

        r = self.client.call('taobao.simba.campaign.budget.get', params={
            'campaign_id': self.entity_id
        }, token=customer.token)

        return float(get(r, path='simba_campaign_budget_get_response.campaign_budget.budget')) * 100

    @budget.setter
    def budget(self, value):
        """
        Ref: http://open.taobao.com/api.htm?docId=10548&docType=2
        """
        customer = self.owner

        self.client.call('taobao.simba.campaign.budget.update', params={
            'campaign_id': self.entity_id,
            'budget': int(value / 100),
            'use_smooth': 'false'
        }, token=customer.token)

    def enable(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10556&docType=2
        """
        customer = self.owner

        self.client.call('taobao.simba.campaign.update', params={
            'campaign_id': self.entity_id,
            'online_status': 'online',
            'title': self.title
        }, token=customer.token)

    def disable(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=10556&docType=2
        """
        customer = self.owner

        self.client.call('taobao.simba.campaign.update', params={
            'campaign_id': self.entity_id,
            'online_status': 'offline',
            'title': self.title
        }, token=customer.token)

    @property
    def ads(self):
        """
        Ref: http://open.taobao.com/api.htm?docId=21676&docType=2
        """
        customer = self.owner

        r = self.client.call('taobao.simba.adgroupsbycampaignid.get', params={
            'campaign_id': self.entity_id,
            'page_size': 20,  # TODO: pagination support
            'page_no': 1
        }, token=customer.token)

        return [Ad(x['adgroup_id'], owner=self, **x) for x in get(r, path='simba_adgroupsbycampaignid_get_response.adgroups.adgroup_list.a_d_group', default=[])]
