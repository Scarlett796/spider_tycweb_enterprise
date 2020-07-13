> ### 项目架构

项目基于python3+mysql进行搭建的一个web爬虫，主要用于爬取天眼通的企业数据。
架子已经基本搭建起来，git clone之后修改配置即可运行，在此基础上可进行二次开发。

- python 开发语言，基于python3
- mysql 数据库

关于python方面，主要使用了requests、sqlalchemy、xlwt包。
项目主要运行于Linux系统上，本人使用测试机Mac，线上服务器为Centos7.0。

> ### 项目运行

- Centos7.0系统服务器
- git clone https://github.com/GIS90/spider_tycweb_enterprise.git
- 更新web配置文件：etc/config.py，根据不同需求进行项目更改
- 安装项目运行的环境：python install_env.py，建立项目独立的运行环境，安装了virtualenv、python、packages等操作，了解具体详情请参考代码
- 启动项目：项目root目录，执行python run.py

> ### 配置说明

位置：etc/config.yaml
- SERVER: 服务基础信息
- LOG: 日志，如果无LOG_DIR默认会在项目root目录下建立log文件夹进行日志存放
- DB: 数据库连接，项目中包含数据库信息（请勿乱更改或者操作数据库）
- FILES: 文件输出位置，如果无默认会在项目root目录下建立excel文件夹进行数据存放
- STORE: 输出方式，excel与db
- APIS: 天眼查的APIS
- PROXY: 代理相关的API

> ### 问题

1、需要在etc/config.yaml进行配置相关信息，cookie建议填写，否则爬取的数据电话、邮箱等信息是带有**号的。
2、未注册的用户只能查找遍历5页，目前这个没什么好的方案解决。
3、需要手动进行验证码验证

> ### 已完善功能

- 数据爬取
- 数据写入excel
- 数据写入DB

> ### 开发中功能

1、解决手动验证的问题


> ### 特别声明

项目部分代码借鉴了我的web脚手架代码（https://github.com/GIS90/base_webframe）


> ### 联系方式

* ***Github:*** https://github.com/GIS90

* ***Email:*** gaoming971366@163.com

* ***Blog:*** http://pygo2.cn

* ***WeChat:*** PyGo90


Enjoy the good lift everyday！欢迎大家跟我一起来完善这个爬虫项目！！
