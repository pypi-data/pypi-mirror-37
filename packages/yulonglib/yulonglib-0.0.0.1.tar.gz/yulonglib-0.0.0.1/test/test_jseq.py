from yulonglib.jseq import Jseq

def test1():
    url="http://10.85.93.232/lib/libac2.php?ip=10.85.93.232&port=61777&socialtime=1&cuid=2511255003&from=1045595010&source=2936099636&version=45&sid=t_wap_android&dup=1&engine_type=0&wm=5091_0008&isbctruncate=1&key=%E7%8C%AB%E7%B3%BB%E5%A5%B3%E5%8F%8B%E7%8E%8B%E4%B8%BD%E5%9D%A4&count=20&z=all&pagesize=20&xsort=social&us=1&token=Authorization%3A+TAuth2+token%3D%22OXPWQTNWWTQTXNXONYUU%253DONYUS%253DOUPYOTXORQPUVNTQTXNXNXpyOLOWaBfS%22%2Cparam%3D%22uid%253D2511255003%22%2Csign%3D%222pzblUe3uYqmdd42%252Blq3AcM1g1I%253D%22&cip=223.73.172.138&t=3&nettype=wifi&nofilter=0&page="
    J=Jseq(url,"")
    result,err=J.j_dict(1,2,"subposdata",("ID"),"digit_attr")
    print result

def test_list():
    url="http://10.85.93.232/lib/libac2.php?ip=10.85.93.232&port=61777&socialtime=1&cuid=2511255003&from=1045595010&source=2936099636&version=45&sid=t_wap_android&dup=1&engine_type=0&wm=5091_0008&isbctruncate=1&key=%E7%8C%AB%E7%B3%BB%E5%A5%B3%E5%8F%8B%E7%8E%8B%E4%B8%BD%E5%9D%A4&count=20&z=all&pagesize=20&xsort=social&us=1&token=Authorization%3A+TAuth2+token%3D%22OXPWQTNWWTQTXNXONYUU%253DONYUS%253DOUPYOTXORQPUVNTQTXNXNXpyOLOWaBfS%22%2Cparam%3D%22uid%253D2511255003%22%2Csign%3D%222pzblUe3uYqmdd42%252Blq3AcM1g1I%253D%22&cip=223.73.172.138&t=3&nettype=wifi&nofilter=0&page="
    J=Jseq(url,"")
    result,err=J.j_list(1,2,"subposdata","ID")
    print result

def test2():
    url="http://topic.search.weibo.com/topic_recommender/topic_query.php?uid=1234&type=1&count=5&page="
    J_d=Jseq(url,"")
    #tid_d_dict=J_d.j_dict(1,2,"statuses",("attribute","text"),"mid","uid",("attribute","text"))
    #tid_d_dict=J_d.j_dict(1,2,"statuses",("attribute","text"),"mid","uid",("attribute","text"))
    tid_d_dict=J_d.j_dict(1,2,"statuses",("attribute","text"),"mid")
    # X tid_d_dict=J_d.j_dict(1,2,"statuses",("attribute","text"),(("mid",),))
    #tid_d_filter=J_d.j_filter(1,2,test,"statuses",("attribute","text"),"mid")
    #print tid_d_filter
    print tid_d_dict

def test3():
    urlonline="http://unify.search.weibo.com/mi/finder.php?wm=3333_2001&i=4e51dd2&b=1&from=1085393010&c=iphone&networktype=wifi&v_p=61&skin=default&v_f=1&lang=zh_CN&sflag=1&ua=iPhone6%2C2__weibo__8.5.3__iphone__os10.3.3&ft=0&scenes=0&extparam=search_biz%3A0&lon=116.2692666074009&luicode=10000001&containerid=231619_3&featurecode=10000001&uicode=10000772&fid=231583&need_head_cards=1&lat=40.04029177746782&feed_mypage_card_remould_enable=1&lfid=100012771122141&moduleID=pagecard&client=inf&infoType=cardlistInfo&ip=10.235.21.33&cip=10.235.21.33&uid=3009551200&page="
    J_online=Jseq(urlonline,"")
    # X topic_hot_dict,errs=J_online.j_dict(1,2,"cards",("card_group",0,"title"),(("card_group",0,"tag_img"),))
    topic_hot_dict,errs=J_online.j_dict(1,4,"cards",("card_group",0,"title"),("card_group",0,"tag_img"))
    print topic_hot_dict

def test4():
    urlocr="http://10.85.169.108:8001/4289289690957127,4289481991632354"
    J_ocr=Jseq(urlocr,"")
    ocrdict,errs=J_ocr.j_dict(0,0,"","mid","pic_words")
    print ocrdict

test_list()
