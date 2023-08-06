from fleader import fleader as rq


# _,doc=rq.get('http://www.runoob.com/',ex='jq')
# item = doc('.item-top,.item-1').items()
# for i in item:
# 	print(i.attr('class'))
# 	print(i('h4').text())
# 	print('==========================')


#gevent测试
# def pr(x):
# 	print(x)

# urls = [i for i in range(100)]
# rq.gPool(pr, urls)


#gevent测试2
# from fleader import fleader as rq
# l,q,s=rq.getGevent()#返回常量,队列,锁

# l.x=0
# def getu(url):
# 	print(url,l.x)
# 	l.x=l.x+1

# urls = [i for i in range(100)]
# rq.gPool(getu, urls)


# @rq.cache(ext=[0])
# def test1(a,b,v=1,c=2):
#     print('111111111111')
#     return 1

# print(test1(1,2,v=1,c=3))


# 修饰器函数缓存
# @rq.cache()
# def gethtml(r):
#     rt=rq.get('http://127.0.0.1',cache=True)
#     print('1111111111111111111111')
#     return rt


# rt=gethtml('rrrrrrrrrrr')
# print(rt)








#并发测试
# def Downloader(arg):
#     q,lock=arg['arg']
#     while 1:
#         lock.acquire()
#         if not q.empty():
#             url=q.get()
#             lock.release()
#             rq.get(url)
#         else:
#             lock.release()
#             break

# if __name__ == "__main__":
#     urls=['http://127.0.0.1']*100
#     q,lock = rq.Manager()
#     rq.feed(q,urls)
#     rq.sPool(Downloader,tnum=25,cnum=4,arg=[q,lock])
 



