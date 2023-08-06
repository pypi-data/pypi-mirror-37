# coding:utf-8
#
# The MIT License (MIT)
#
# Copyright (c) 2016-2018 yutiansut/QUANTAXIS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os

import tornado
from tornado.web import Application, RequestHandler, authenticated

from QAWebServer.arphandles import (AccountHandler, MemberHandler,
                                        RiskHandler)
from QAWebServer.basehandles import QABaseHandler
from QAWebServer.commandhandler import CommandHandler, RunnerHandler
from QAWebServer.datahandles import (StockBlockHandler, StockCodeHandler,
                                         StockdayHandler, StockminHandler,
                                         StockPriceHandler)
from QAWebServer.quotationhandles import (MonitorSocketHandler,
                                              RealtimeSocketHandler,
                                              SimulateSocketHandler)
from QAWebServer.strategyhandlers import BacktestHandler, StrategyHandler
from QAWebServer.tradehandles import AccModelHandler, TradeInfoHandler
from QAWebServer.userhandles import (PersonBlockHandler, SigninHandler,
                                         SignupHandler)

from QAWebServer.jobhandler import JOBHandler
class INDEX(QABaseHandler):
    def get(self):
        self.finish('.{}{}'.format(os.sep, "index.html"))


def main():
    apps = Application(
        handlers=[
            (r"/", INDEX),
            (r"/marketdata/stock/day", StockdayHandler),
            (r"/marketdata/stock/min", StockminHandler),
            (r"/marketdata/stock/block", StockBlockHandler),
            (r"/marketdata/stock/price", StockPriceHandler),
            (r"/marketdata/stock/code", StockCodeHandler),
            (r"/user/signin", SigninHandler),
            (r"/user/signup", SignupHandler),
            (r"/user/blocksetting", PersonBlockHandler),
            (r"/strategy/content", StrategyHandler),
            (r"/backtest/content", BacktestHandler),
            (r"/trade", AccModelHandler),
            (r"/tradeinfo", TradeInfoHandler),
            (r"/realtime", RealtimeSocketHandler),
            (r"/simulate", SimulateSocketHandler),
            (r"/monitor", MonitorSocketHandler),
            (r"/accounts", AccountHandler),
            (r"/accounts/all", MemberHandler),
            (r"/risk", RiskHandler),
            (r"/command/run", CommandHandler),
            (r"/command/runbacktest", RunnerHandler),
            (r"/command/jobmapper",JOBHandler)
        ],
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(apps)
    http_server.bind(8010, address='0.0.0.0')
    """增加了对于非windows下的机器多进程的支持
    """
    http_server.start(1)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
