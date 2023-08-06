from itertools import chain
from pysimba.client.mixins import ClientCapability
from pysimba.client.utils import batch, get
from pysimba.reporting.core import DateRangeTypes


class Insight(ClientCapability):
    @batch(100)
    def predict_categories(self, texts):
        """
        Ref: http://open.taobao.com/api.htm?docId=23571&docType=2
        """
        r = self.client.call('taobao.simba.insight.catsforecastnew.get', params={
            'bidword_list': ','.join(texts)
        })

        return get(r, path='simba_insight_catsforecastnew_get_response.category_forecast_list.insight_category_forcast_d_t_o', default=[])

    @batch(100)
    def report(self, texts, date=None, start_date=None, end_date=None):
        """
        Ref: http://open.taobao.com/api.htm?docId=23577&docType=2
        """
        if date != DateRangeTypes.CUSTOM_DATE and date != DateRangeTypes.TODAY:
            start_date, end_date = date.value

        r = self.client.call('taobao.simba.insight.wordssubdata.get', params={
            'bidword_list': ','.join(texts),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        })

        return get(r, path='simba_insight_wordssubdata_get_response.word_subdata_list.insight_word_sub_data_d_t_o', default=[])

    @batch(100)
    def summary(self, texts, date=None, start_date=None, end_date=None):
        """
        Ref: http://open.taobao.com/api.htm?docId=23576&docType=2
        """
        if date != DateRangeTypes.CUSTOM_DATE and date != DateRangeTypes.TODAY:
            start_date, end_date = date.value

        r = self.client.call('taobao.simba.insight.wordsdata.get', params={
            'bidword_list': ','.join(texts),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        })
        
        return get(r, path='simba_insight_wordsdata_get_response.word_data_list.insight_word_data_d_t_o', default=[])
