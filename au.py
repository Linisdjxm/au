import os
import pywikibot
from pywikibot import pagegenerators
from collections import abc
import aufunc as f
import time
import copy
import re

class c1:
    dic = {};
class c2:
    rbn = 0;
    lts = "";
    un = "";
    revid = [];
    page = "";

def ndi(nested):
    for key, value in nested.items():
        if isinstance(value, abc.Mapping):
            yield from ndi(value)
        else:
            yield key, value
site = pywikibot.Site()
d1 = {}
d2 = {}
kx = 0;
l1 = []
l2 = []
ccount = -1;
lock = {}
l3 = {}
rmax = 4 #4
lcount = -1
ts1 = pywikibot.Timestamp.isoformat(site.server_time())
time.sleep(3)
ts2 = pywikibot.Timestamp.isoformat(site.server_time())
while True:
    gen = site.recentchanges(end = ts2,changetype="edit",start=f.msec(ts1,5),reverse=True)
    for item in gen:
        if ((("mw-rollback" in item["tags"]) or ("mw-undo" in item["tags"]) or ("mw-manual-revert" in item["tags"])) and (item["title"] not in lock)):
            print(l2)
            if (item["user"] not in d1):
                l1.append(c1())
                l2.append(c2())
                lcount += 1
                ccount = lcount
                l2[ccount].rbn = 1
                l2[ccount].lts = copy.deepcopy(item["timestamp"])
                l2[ccount].un = copy.deepcopy(item["user"])
                l2[ccount].revid.append(copy.deepcopy(item['old_revid']))
                l2[ccount].page = copy.deepcopy(item["title"])
                #l2.append(copy.deepcopy(l2[ccount]))
                d1[l2[ccount].un] = copy.deepcopy(l1[ccount])
                d1[l2[ccount].un].dic[item["title"]] = copy.deepcopy(l2[ccount])
                #d2[l2[ccount].un] = len(l1) - 1;
                print(d1[item["user"]].dic[item["title"]].un + ": " + item["title"] +" " +str(d1[item["user"]].dic[item["title"]].rbn) + " " + d1[item["user"]].dic[item["title"]].lts + " " + str(item['old_revid']))
                l3[item["user"]] = copy.deepcopy(ccount);
                #lcount += 1;
                #ccount = lcount;
            else:
                if(item["title"] not in d1[item["user"]].dic):
                    ccount = l3[item["user"]]
                    l2[ccount] = c2()
                    l2[ccount].rbn = 1
                    l2[ccount].lts = copy.deepcopy(item["timestamp"])
                    l2[ccount].un = copy.deepcopy(item["user"])
                    l2[ccount].page = copy.deepcopy(item["title"])
                    l2[ccount].revid.append(copy.deepcopy(item['old_revid']))
                    d1[l2[ccount].un].dic[item["title"]] = copy.deepcopy(l2[ccount])
                    print(d1[item["user"]].dic[item["title"]].un + ": " + item["title"] + " " + str(d1[item["user"]].dic[item["title"]].rbn) + " " + d1[item["user"]].dic[item["title"]].lts+ " " + str(item['old_revid']))
                    ccount = lcount
                else:
                    if(item['old_revid'] not in d1[item["user"]].dic[item["title"]].revid):
                        d1[item["user"]].dic[item["title"]].rbn += 1
                        d1[item["user"]].dic[item["title"]].lts = item["timestamp"]
                        d1[item["user"]].dic[item["title"]].revid.append(item['old_revid'])
                        print(d1[item["user"]].dic[item["title"]].un + ": " + item["title"] + " " +str(d1[item["user"]].dic[item["title"]].rbn) + " " + d1[item["user"]].dic[item["title"]].lts+ " " + str(item['old_revid']))
                        if(d1[item["user"]].dic[item["title"]].rbn >= rmax):
                            print("3RR: " + item["user"] + ": " + item["title"])
                            f.alog("3RR: " + item["user"] + ": " + item["title"])
                            for k1 in list(d1.keys()):
                                for k2 in list(d1[k1].dic.keys()):
                                    if(d1[k1].dic[k2].page == item["title"]):
                                        print("DEL: " + k1 + ": " + k2)
                                        f.alog("DEL: " + k1 + ": " + k2)
                                        del d1[k1].dic[k2]
                                        if not(d1[k1].dic):
                                            f.alog("DEL: " + k1 + ": ALL")
                                            print("DEL: " + k1 + ": ALL")
                                            del d1[k1]
                            print("ADDLOCK: " + item["title"])
                            f.alog("ADDLOCK: " + item["title"])
                            lock[item["title"]] = item["timestamp"]
                            rfp = pywikibot.Page(site,u"Wikipedia:请求保护页面")
                            if(rfp.text.find(item["title"]) == -1):
                                pt1 = rfp.text[13:]
                                pt2 = "\n{{/header}}\n=== " + item["title"] + " ===\n请检查此页面的编辑历史。可能有一名或多名用户在此页面执行了多于3次的回退操作。~~~~\n:: <small>目前保護狀態：{{protection status|" + item["title"] + "}}</small>\n" + pt1
                                site.editpage(page=rfp,summary="add",notminor=True,text=pt2)
                    else:
                        print("DONE!")
    for k1 in list(d1.keys()):
        for k2 in list(d1[k1].dic.keys()):
            if(f.mwts2uts(f.psec(d1[k1].dic[k2].lts,86400)) <= f.mwts2uts(pywikibot.Timestamp.isoformat(site.server_time()))):
                print("DEL: " + k1 + ": " + k2)
                os.system('echo "' + "DEL: " + k1 + ": " + k2 + '" >> log.txt')
                del d1[k1].dic[k2]
                if not(d1[k1].dic):
                    os.system('echo "' + "DEL: " + k1 + ": ALL" + '" >> log.txt')
                    print("DEL: " + k1 + ": ALL")
                    del d1[k1]
    for k1 in list(lock.keys()):
        if(f.mwts2uts(f.psec(lock[k1],86400)) <= f.mwts2uts(pywikibot.Timestamp.isoformat(site.server_time()))):
            print("UNLOCK: " + k1)
            f.alog("UNLOCK: " + k1)
            del lock[k1]
    ts1 = ts2
    print("sleeping...")
    time.sleep(20)
    ts2 = pywikibot.Timestamp.isoformat(site.server_time());
    print(ts1)
    print(ts2)
