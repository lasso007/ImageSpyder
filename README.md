# 简易爬虫

依赖： PhantomJS和Selenium

![image](https://github.com/lasso007/ImageSpyder/blob/master/example.jpeg)


功能：
1. 系统使用这可以查看参数使用说明信息或提示信息；
2. 具有缺省参数，系统使用者的需求不严格的情况下部分参数采用默认值，并且具有参数检查；
3. 图片采集系统可以按照关键字采集图片，并且可以同时给出多个关键词；
4. 图片采集系统可以从文本中选择关键词，当系统使用者有数十个以上的关键词时，手动输入采集关键词比较麻烦，可以将关键词放入一个文本中，系统从文本中读取关键词；
5. 保存图片链接并下载图片，并且结果按图片搜索引擎返回结果排序，搜索结果排名靠前的结果比较可靠，方便进行图片的筛选；
6. 图片下载都是并发执行，程序不会在下载过程中被阻塞；
7. 图片下载超时尝试重新下载，下载次数超过三次数后放弃下载。
8. 目前只支持python2，简单改动是可以迁移到python3的

------
（代码简单，功能和可靠性还行；有任何修改意见，欢迎提出！）
![image](example.jpeg)
