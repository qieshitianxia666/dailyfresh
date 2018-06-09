# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import GoodsInfo,TypeInfo
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
# 查询每类商品最新的4个和点击率最高的4个
def index(request):
    count = request.session.get('count')
    fruit = GoodsInfo.objects.filter(gtype_id=1).order_by("-id")[:4]
    fruit2 = GoodsInfo.objects.filter(gtype_id=1).order_by("-gclick")[:4]
    fish = GoodsInfo.objects.filter(gtype_id=7).order_by("-id")[:4]
    fish2 = GoodsInfo.objects.filter(gtype_id=7).order_by("-gclick")[:4]
    meat = GoodsInfo.objects.filter(gtype_id=3).order_by("-id")[:4]
    meat2 = GoodsInfo.objects.filter(gtype_id=3).order_by("-gclick")[:4]
    egg = GoodsInfo.objects.filter(gtype_id=4).order_by("-id")[:4]
    egg2 = GoodsInfo.objects.filter(gtype_id=4).order_by("-gclick")[:4]
    vegetables = GoodsInfo.objects.filter(gtype_id=5).order_by("-id")[:4]
    vegetables2 = GoodsInfo.objects.filter(gtype_id=5).order_by("-gclick")[:4]
    frozen = GoodsInfo.objects.filter(gtype_id=6).order_by("-id")[:4]
    frozen2 = GoodsInfo.objects.filter(gtype_id=6).order_by("-gclick")[:4]
    # count = CartInfo.objects.filter(
    #     user_id=request.session.get('userid')).count()   'count':count,
    # # 构造上下文
    context = {'title': '首页', 'fruit': fruit,
               'fish': fish, 'meat': meat, 'egg': egg,
               'vegetables': vegetables, 'frozen': frozen,
               'fruit2': fruit2, 'fish2': fish2, 'meat2': meat2,
               'egg2': egg2, 'vegetables2': vegetables2, 'frozen2': frozen2,
               'guest_cart': 1,'page_name':0,'count':count}

    # 返回渲染模板
    return render(request, 'df_goods/index.html', context)


#商品列表
def goodlist(request, typeid, pageid, sort):
    """
    typeid:商品类型id;selectid:查询条件id，1为根据id查询，2位根据价格查询，3位根据点击量查询
    """
    count = request.session.get('count')
    # 获取最新发布的商品
    newgood = GoodsInfo.objects.all().order_by('-id')[:2]
    # 根据条件查询所有商品
    if sort == '1':#按最新   gtype_id  , gtype__id  指typeinfo_id
        sumGoodList = GoodsInfo.objects.filter(
            gtype_id=typeid).order_by('-id')
    elif sort == '2':#按价格
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('gprice')
    elif sort == '3':#按点击量
        sumGoodList = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('-gclick')
    # 分页
    paginator = Paginator(sumGoodList, 12)
    goodList = paginator.page(int(pageid))
    pindexlist = paginator.page_range
    # print pindexlist    xrange(1,2)
    # 确定商品的类型
    goodtype = TypeInfo.objects.get(id=typeid)
    # count = CartInfo.objects.filter(
    #     user_id=request.session.get('userid')).count()
    # 构造上下文  'count': count,
    context = {'title': '商品详情',  'list': 1,
               'guest_cart': 1, 'goodtype': goodtype,
               'newgood': newgood, 'goodList': goodList,

               'typeid': typeid, 'sort': sort,
               'pindexlist': pindexlist, 'pageid': int(pageid),'count':count}

    # 渲染返回结果
    return render(request, 'df_goods/list.html', context)


def detail(request,id):
    goods = GoodsInfo.objects.get(pk=int(id))
    goods.gclick=goods.gclick+1
    goods.save()
    # 查询当前商品的类型   goodsinfo__id 值
    # goodtype = TypeInfo.objects.get(goodsinfo__id=id)
    goodtype = goods.gtype
    # type = TypeInfo()

    count = request.session.get('count')
    #goods.gtype = typeinfo    goods.gtype.goodsinfo_set -> typeinfo.goodsinfo_set
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]

    #使用cookies记录最近浏览的商品id

    #获取cookies
    goods_ids = request.COOKIES.get('goods_ids', '')
    tap_ids = request.COOKIES.get('tap_ids','')
    obj = {}
    max_two = []
    maxNum = 0
    like_list = []
    like_len = 0
    #获取当前点击商品id
    goods_id='%d'%goods.id
    if tap_ids != '':
        tap_id_list = tap_ids.split(',')
        for curr_id in tap_id_list:
            if obj.has_key(curr_id):
                obj[curr_id] = obj[curr_id] + 1

            else:
                obj[curr_id] = 1
        for k in obj:
            if obj[k] > maxNum:
                maxNum = obj[k]
                mostEle = k

        max_two.append(mostEle)
        obj.pop(mostEle)
        maxNum = 0
        if len(obj)>0:
            for k in obj:
                if obj[k] > maxNum:
                    maxNum = obj[k]
                    mostEle = k
            max_two.append(mostEle)
        for like_id in max_two:
            like_list.append(GoodsInfo.objects.get(id=int(like_id)))
            like_len = len(like_list)
        tap_id_list.insert(0,goods_id)
        tap_ids = ','.join(tap_id_list)
    else:
        tap_ids = goods_id

    #判断cookies中商品id是否为空
    if goods_ids!='':
        #分割出每个商品id
        goods_id_list=goods_ids.split(',')
        #判断商品是否已经存在于列表
        if goods_id_list.count(goods_id)>=1:
            #存在则移除
            goods_id_list.remove(goods_id)
        #在第一位添加
        goods_id_list.insert(0,goods_id)
        #判断列表数是否超过5个
        if len(goods_id_list)>=6:
            #超过五个则删除第6个
            del goods_id_list[5]
        #添加商品id到cookies
        goods_ids=','.join(goods_id_list)
    else:
        #第一次添加，直接追加
        goods_ids=goods_id
    context={
        'title':goodtype.ttitle,
        'guest_cart':1,
        'g':goods,
        'newgood':news,
        'id':id,
        'isDetail': True,
        'list':1,
        'goodtype': goodtype,
        'count':count,
        'like_list':like_list,
        'like_len':like_len
    }
    response=render(request,'df_goods/detail.html',context)
    response.set_cookie('goods_ids',goods_ids)
    response.set_cookie('tap_ids', tap_ids)
    return response
def search(request):
    val=request.POST['q']
    goods=GoodsInfo.objects.get(gtitle=val)

    if isinstance(int(goods.gclick),int):
        goods.gclick=goods.gclick+1
        goods.save()
        goodtype = goods.gtype
        count = request.session.get('count')
        news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
        context = {
                   'title': goodtype.ttitle,
                   'guest_cart': 1,
                   'g': goods,
                   'newgood': news,
                   'isDetail': True,
                   'list': 1,
                   'goodtype': goodtype,
                   'count': count,
                   }
        return render(request, 'df_goods/detail.html', context)

    else:
        return HttpResponse('<h1>404! 对不起，您搜索的商品暂未找到</h1>')
