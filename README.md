> ### 项目架构

项目基于python3+mysql进行搭建的一个web爬虫，主要用于爬取天眼通的企业数据。
架子已经基本搭建起来，git clone之后修改配置即可运行，在此基础上可进行二次开发。

- python 开发语言，基于python3
- mysql 数据库

关于python方面，主要使用了requests、sqlalchemy、xlwt包。
项目主要运行于Linux系统上，本人使用测试机Mac，线上服务器为Centos7.0。

> ### 项目运行

- Centos7.0系统服务器
- 不需要数据库存储数据的可以忽略此步，安装Mysql/MariaDB，创建数据库并配置，最后执行db目录下的sql文件（table create sql）
- git clone https://github.com/GIS90/spider_tycweb_enterprise.git
- 更新web配置文件：etc/config.py，根据不同需求进行项目更改
- 安装项目运行的环境：python install_env.py，建立项目独立的运行环境，安装了virtualenv、python、packages等操作，了解具体详情请参考代码
- 启动项目：项目root目录，执行python run.py

> ### 配置说明

位置：etc/config.yaml
- SERVER: 服务基础信息
其中，KEYS为查询关键字，可以设置多个，建议3 ～ 6个，并且用英文逗号","进行分割
RUN_MODE（运行模式）项目可采用不同的模式进行数据抓取，包含3种模式：single单进程 process多进程 gevent多协程，使用process模式时，建议关键字的个数 < CPU-1
IS_TEST_BREAK是否开启测试模式，测试模式是只获取每页的一条数据
- PAGINATION
PAGINATION为page的分割数，用于single模式，到达指定的分割数为一个分割excel文件
MIN_PAGE最小页数
MAX_PAGE最大页数
- LOG: 日志，如果无LOG_DIR默认会在项目root目录下建立log文件夹进行日志存放
- DB: 数据库连接，项目中包含数据库信息（请勿乱更改或者操作数据库）
- FILES: 文件输出位置，如果无默认会在项目root目录下建立excel文件夹进行数据存放
- STORE: 输出方式，excel与db
- APIS: 天眼查的APIS，模式API_MODE: pro专业版 tyc普通版，默认tyc普通版，不同版本请求服务地址不同
- PROXY: 代理相关的API，如果无代理API接口，IS_RUN设置False

> ### 问题

1、需要在etc/config.yaml进行配置相关信息，cookie建议填写，否则爬取的数据电话、邮箱等信息是带有**号的。

2、未注册的用户只能查找遍历5页，目前这个没什么好的方案解决。

3、需要手动进行验证码验证

> ### 已完善功能

- 数据爬取、解析、excel/DB存储
- 多进程模式运行
- 支持普通版（www.tianyancha.com）、专业版（pro.tianyancha.com）
- 支持请求代理，需要配置指定代理API

> ### 开发中功能

1、解决手动验证的问题

2、多协程数据抓取，协程gevent安装出现问题（Mac）


> ### 结果说明

- 7个进程跑数据，1w条数据大概2.5h（本人亲测）

> ### 特别声明

- 项目部分代码借鉴了我的web脚手架代码（https://github.com/GIS90/base_webframe）
- 在请求获取详情数据时候，设置time.sleep，以免反爬机制认为是恶意爬取


> ### 联系方式

* ***Github:*** https://github.com/GIS90

* ***Email:*** gaoming971366@163.com

* ***Blog:*** http://pygo2.cn

* ***WeChat:*** PyGo90


Enjoy the good lift everyday！欢迎大家跟我一起来完善这个爬虫项目！！
