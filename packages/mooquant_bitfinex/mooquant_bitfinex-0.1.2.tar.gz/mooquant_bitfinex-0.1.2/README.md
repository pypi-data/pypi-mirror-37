# [Bitfinex](https://www.bitfinex.com/) [MooQuant](http://gbeced.github.io/pyalgotrade/) Module

This is a very early version of the module. **Live trading is not yet implemented.** Right now, I have only implemented LiveFeed (extends ```barfeed.BaseBarFeed```). Live data is fetched from the trades and order book API endpoint of Bitfinex. Hopefully in the near future, a live broker class will be implemented.

The LiveFeed class can be plugged just as any other bar feed in MooQuant. To subscribe for bid and ask prices, just call ```getOrderBookUpdateEvent().subscribe(<your_callback_function>)``` from the LiveFeed instance. Kindly see example at sample.py.

