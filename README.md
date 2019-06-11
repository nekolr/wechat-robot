## 设计灵感
没啥，被女朋友吐槽整天就知道写代码，人家程序员男朋友还知道做个微信聊天机器人陪女朋友聊天等等等。机器人我写不了，但是我可以调用别人家的机器人然后说是我写的呀。微信聊天也有现成的库，废话不多说，直接开撸，写了一会儿偶然发现了一个兄弟项目 [EverydayWechat](https://github.com/sfyc23/EverydayWechat)（做的比我好，抄一点🙈）。

## 主要依赖库
- [ItChat](https://github.com/littlecodersh/ItChat) - 微信个人号收发消息
- [APScheduler](https://github.com/agronholm/apscheduler) - 定时任务
- [requests](https://github.com/kennethreitz/requests) - 网络请求
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) - 页面解析

## 功能
- [x] 定时给女朋友发送微信消息
- [ ] 陪聊机器人

## 数据来源
- [天气 API](https://www.tianqiapi.com/api) - 天气信息
- [ONE · 一个](http://wufazhuce.com/) - 一句话格言
- [金山词霸](http://open.iciba.com/dsapi/) - 金山词霸每日一句