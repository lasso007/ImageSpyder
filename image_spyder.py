#coding=utf-8
import argparse
import os
import urllib
import urllib2
import time
import random
import re
import csv
import socket
import threading
import sys
import subprocess
import glob
import Image
import pdb
parser = argparse.ArgumentParser()
parser.add_argument('-s','--source',type=int, nargs='+',
						default=1, help="选择爬取图片的来源,"+
						"1: 百度	 2：必应   3：360.")
parser.add_argument('-n','--threads',type=int,
						default=20, help="下载图片的线程数量.")
parser.add_argument('-k','--keyword',type=str, nargs='+',
						help="所需要爬取的关键词.")
parser.add_argument('-i','--inputfile',type=str,
						help="存放关键词的文本文件.")
parser.add_argument('-d','--targetDir',type=str,
						default='.',help='存放爬虫结果的目录.')
args = parser.parse_args()
def check_args():
    flag = True
    if args.inputfile and not(os.path.isfile(args.inputfile)):
        flag = False
        print("不存在{}这个文件,请检查输入文件名和路径".format(args.inputfile))
    if args.threads<1:
        flag = False
        print("线程数量应大于0")
    if (not args.keyword)and(not args.filename):
        flag = False
        print("请输入关键词或者存放关键词的文件")
    if not args.source:
        flag = False
        print("请选择所需要爬取图片的来源")
    s={1:"百度图片搜索", 2:"必应图片搜索", 3:"360图片搜索"}
    source = (s[i] for i in args.source)
    print("########################################")
    print("#  source: {}".format('\t'.join(source)))
    print("#  kewords: {}".format('\t'.join(args.keyword)))
    print("#  inputfile: {}".format(args.inputfile))
    print("#  threads: {}".format(args.threads))
    print("#  target directory: {}".format(args.targetDir))
    print("########################################")
    print("Waiting...")
    time.sleep(2)
    return flag
def getHtml(url, interval=True):
    if(interval):
        time.sleep(random.random()*0.8)
    res_html = []
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    try:
        res_data = urllib2.urlopen(req)
        res_html = res_data.read()
    except Exception as e:
        print(e)
    finally:
        return res_html
def download_single(image_link,file_name):
    urllib.URLopener.version = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
    n=3
    socket.setdefaulttimeout(3)
    IsException = True
    while(n>0)and IsException:
        try:
            n = n-1
            print(file_name+' downloading...')
            urllib.urlretrieve(image_link,file_name)
            IsException = False
        except Exception as e:
            IsException = True
            print(e)
def downlowder(url_links,begin_id,target_path):
    i=begin_id;
    for image_link in url_links:
        file_name = os.path.join(target_path,('%0*d'%(4,i))+'.jpg')
        t = threading.Thread(target=download_single,args=(image_link,file_name))
        t.setDaemon(True)
        t.start()
        t.join(9)
        i = i+1
def find_image_links_baidu(page_data):	# Extract image links in page from baidu
    image_links = re.findall(r"objURL\":\"(.+?)\"",page_data)
    return image_links
def spider_baidu(term):
    base_dir = os.path.join(args.targetDir,'baidu/')
    if not(os.path.exists(base_dir)):
        os.mkdir(base_dir)
    base_dir += term.strip()
    if not(os.path.exists(base_dir)):
        os.mkdir(base_dir)
    url_links = []
    selectedIndex = 0
    while(len(url_links)<500 and selectedIndex<800):
        url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word='
        url =url + urllib.quote(term)+'&rn=60&pn='+str(selectedIndex)
        print(url)
        selectedIndex = selectedIndex + 1
        page = getHtml(url)
        if len(page)<300:
            break
        links = find_image_links_baidu(page)
        for l in links:
            if l not in url_links:
                url_links.append(l)
	links_file = os.path.join(base_dir,term+'.txt')
    with open(links_file,'wb') as f:
        f.write('\n'.join(url_links))
    thread_number = args.threads	# Begin downloading images
    gap = len(url_links)/thread_number+1
    begin_id = 0
    threads = []	#threads list
    while begin_id<len(url_links):	#create threads
        single_thread=threading.Thread(target=downlowder,args=(url_links[begin_id:(begin_id+gap)],begin_id,base_dir))
        threads.append(single_thread)
        begin_id = begin_id + gap
    for t in threads:	#begin threads
        t.start()
    for t in threads:	#waiting for all threads ending
        t.join()
    return url_links
def find_image_links_360(page_data):
    image_links = re.findall(r"img\":\"(.+?)\"",page_data)
    image_links = list(a.replace('\\','') for a in image_links)
    return list(image_links)
def spider_360(term):
    base_dir = os.path.join(args.targetDir,'360/')
    if not(os.path.exists(base_dir)):
        os.mkdir(base_dir)
    base_dir += term.strip()
    if not(os.path.exists(base_dir)):
        os.mkdir(base_dir)
    url_links = []
    image_index = 0
    while(len(url_links)<800 and image_index<1000):
        url = 'http://image.so.com/j?q='+urllib.quote(term);
        url = url+'&src=srp&sn='+str(image_index)+'&pn=50'
        print(url)
        image_index = image_index + 50
        print(url)
        page = getHtml(url)
        if(len(page)<300):
            break
        links = find_image_links_360(page)
        for l in links:
            if l not in url_links:
                url_links.append(l)
	links_file = os.path.join(base_dir,term+'.txt')
    with open(links_file,'wb') as actor_links:
        actor_links.write('\n'.join(url_links))
    thread_number = args.threads	# Begin downloading images
    gap = len(url_links)/thread_number+1
    begin_id = 0
    threads = []	#threads list
    while begin_id<len(url_links):	#create threads
        single_thread = threading.Thread(target=downlowder,args=(url_links[begin_id:(begin_id+gap)],begin_id,base_dir))
        threads.append(single_thread)
        begin_id = begin_id + gap
    for t in threads:	#begin threads
        t.start()
    for t in threads:	#waiting for all threads ending
        t.join()
    return url_links
def find_image_links_bing(json_data):	# Extract image links in page from bing
    image_links = []
    x = json_data
    while 'jpg' in x:
        a = x.find('jpg')
        cut_x = x[:a+3]
        while(cut_x.count('http')>1):
            cut_x = cut_x[cut_x.find('http')+4:]
        b = cut_x.find('http')
        x = x[a+3:]
        image_links.append(cut_x[b:])
    result = []
    for x in image_links:
        if x not in result:
            result.append(urllib.unquote(x))
    return result
def spider_bing(term):
    base_dir = os.path.join(args.targetDir,'bing/')
    if not(os.path.exists(base_dir)):
        os.mkdir(base_dir)
    base_dir += term.strip()
    if not(os.path.exists(base_dir)):
        os.mkdir(base_dir)
    url_links = []
    driver = webdriver.PhantomJS(service_args=['--load-images=false'])
    selectedIndex = 0
    while(len(url_links)<100)and(selectedIndex<800):
        url = 'http://www.bing.com/images/search?q='+urllib.quote(term)
        url = url + '&view=detailv2&selectedIndex='+str(selectedIndex)
        print(url)
        try:
            driver.get(url)
        except Exception as e:
            print(e)
            selectedIndex = selectedIndex+1
        page = driver.page_source.encode('utf-8')
        if len(page)<300:
			break
        x = re.findall(r"json-data=\"(.+?)\"></span>",page)
        links = []
        if(len(x)>0):
            x = urllib.unquote(x[0])
            x = urllib.unquote(x)
            links = find_image_links_bing(x)
        selectedIndex = selectedIndex+len(links)
        if(len(links)<1):
            selectedIndex = selectedIndex+1
        for l in links:
            if l not in url_links:
                url_links.append(l)
	links_file = os.path.join(base_dir,term+'.txt')
    with open(links_file,'wb') as f:
        f.write('\n'.join(url_links))
    thread_number = args.threads	# Begin downloading images
    gap = len(url_links)/thread_number+1
    begin_id = 0
    threads = []	#threads list
    while begin_id<len(url_links):	#create threads
        single_thread = threading.Thread(target=downlowder,args=(url_links[begin_id:(begin_id+gap)],begin_id,base_dir))
        threads.append(single_thread)
        begin_id = begin_id + gap
    for t in threads:	#begin threads
        t.start()
    for t in threads:	#waiting for all threads ending
        t.join()
    return url_links
if __name__=='__main__':
    keywords = []
    check_args()
    print(args.source)
    if not os.path.exists(args.targetDir):
	    if subprocess.call(['mkdir','-p',args.targetDir])!=0:
		    raise(AssertionError("Can not make the target directory:{}".format(args.targetDir)))
    image_links_dir = os.path.join(args.targetDir,'links_file')
    if not os.path.exists(image_links_dir):
        os.mkdir(image_links_dir)
    if(args.inputfile):
        with open(args.inputfile,'r') as f:
            keywords = f.read().split('\n')
    for k in args.keyword:
        keywords.append(k)
    assert(len(keywords)>0) 
    if 3 in args.source:
        from selenium import webdriver
    for k in keywords:
        image_links = set()
        if 1 in args.source:
            links = spider_baidu(k)
        image_links = image_links | set(links)
        if 2 in args.source:
            links = spider_360(k)
        image_links = image_links | set(links)
        if 3 in args.source:
            spider_bing(k)
        image_links = image_links | set(links)
        links_file = os.path.join(image_links_dir,k+'.txt')
        with open(links_file,'w') as f:
            f.write('\n'.join(image_links))

