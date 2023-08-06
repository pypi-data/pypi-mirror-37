from fleader import fleader as rq
import time,os

local,queue,sem=rq.getGevent()

q=queue()
# local.lo=1
# l=local()
def getp(_):
    while 1:
        qs=q.qsize()
        if qs==0:
            time.sleep(1)
        # l.l=1
        else:
            qg=q.get()
            url,request,parse,meta=qg['url'],qg['request'],qg['parse'],qg['meta']
            rp=response()
            rp.result=request(url)
            rp.meta=meta
            parse(rp)
            qsz=q.qsize()
            if qsz==0:
                os._exit(0)
        # print(qs,url,l.l)
class response():
    result=''
    meta={}

class spider():
    start_urls = []
    num=800
    def __init__(self):
        self.start()

    def request(self,url):
        return rq.get(url)

    def parse(self, response):
        pass

    def feed(self,url,meta={},callback=None,request=None):
        if callback == None:
            callback=self.parse
        if request == None:
            request=self.request
        if type(url)==str:
            url=[url]
        for u in url:
            food={}
            food['url']=u
            food['request']=request
            food['parse']=callback
            food['meta']=meta
            q.put(food) 

    def start(self):
        if len(self.start_urls)>0:
            self.feed(self.start_urls)
            num = self.num
            rq.gPool(getp,range(num),num)
        else:
            print('hello pider')

if __name__ == '__main__':
    spider()
