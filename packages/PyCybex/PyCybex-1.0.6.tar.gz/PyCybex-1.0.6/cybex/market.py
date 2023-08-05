from bitshares.market import Market as BitsharesMarket
from bitshares.price import Price as BitsharesPrice
from bitshares.amount import Amount as BitsharesAmount
from bitshares.utils import formatTime
import pdb

class Kline(dict):
    def __init__(self, d, instance):
        self['base'] = instance.rpc.get_asset(d['key']['base'])
        self['quote'] = instance.rpc.get_asset(d['key']['quote'])
        for i in ['open', 'close', 'high', 'low']:
            for j in ['Base', 'Quote']:
                self['{}{}Volume'.format(i, j)] = BitsharesAmount(
                    amount = d['{}_{}'.format(i, j.lower())],
                    asset = self[j.lower()],
                    bitshares_instance = instance
                )
            self['{}Price'.format(i)] = BitsharesPrice(
                base = self['{}BaseVolume'.format(i)],
                quote = self['{}QuoteVolume'.format(i)],
                bitshares_instance = instance)

class Market(BitsharesMarket):
    def __init__(
        self,
        *args,
        base = None,
        quote = None,
        cybex_instance = None,
        **kwargs
    ):
        if 'rte' in kwargs and isinstance(kwargs['rte'], bool):
            self.is_rte = kwargs['rte'] 
        else:
            self.is_rte = False

        super(Market, self).__init__(args = args, base = base, quote = quote, bitshares_instance = cybex_instance)

    def get_market_history(
        self,
        bucket_seconds,
        start,
        end
    ):
        return [Kline(d, self.bitshares) 
                for d in self.bitshares.rpc.get_market_history(
                self['base']['id'],
                self['quote']['id'],
                bucket_seconds,
                formatTime(start),
                formatTime(end),
                api = 'history'
            )]

    def get_fill_order_history(
        self,
        limit = 100):
        return self.bitshares.rpc.get_fill_order_history(
                self['base']['id'],
                self['quote']['id'],
                limit,
                api = 'history'
            )

    def buy(
        self,
        price,
        amount,
        expiration=None,
        killfill=False,
        account=None,
        returnOrderId=False,
        ):
        r = super(Market, self).buy(price, amount, expiration, killfill, account, returnOrderId)
        if not self.is_rte:
            return r
        return {'tx': r, 'txid': self.bitshares.tx().tx.id}

    def sell(
        self,
        price,
        amount,
        expiration=None,
        killfill=False,
        account=None,
        returnOrderId=False,
        ):
        r = super(Market, self).sell(price, amount, expiration, killfill, account, returnOrderId)
        if not self.is_rte:
            return r

        return {'tx': r, 'txid': self.bitshares.tx().tx.id}
