RankIt
=======

RankIt 是一个微信平台相关的web应用，基于 FLASK，用于起床签到、抢票等与排名相关的活动。

依赖
----

Flask 和 Flask-SQLAlchemy

你可以通过`pip install flask`来获取 Flask

通过`pip install flask-sqlalchemy`来获取 Flask-SQLAlchemy

部署
----

RankIt 分为一般版本和 SAE 版本。

对于一般版本，建议使用 virtualenv 创建虚拟环境并安装依赖，再通过 uWSGI 和 Nginx 搭建生产环境。

对于 SAE 版本，你可以直接将 SAE 分支下的文件上传，开启 MYSQL 服务后即可运行。

使用
----

首先要进行初始化，进入部署的地址下的`/init`按提示来初始化。

管理界面在部署的地址下的`/manage`。

对于起床请求，请求地址为部署的地址下`/req?event=wakeup&id=xxx`

对于普通的请求，请求地址为部署的地址下`/req?event=normal&event_id=xxx&id=xxx`

其中 id 均为用户的 id

日志
----

2014/02/07  初步完成

2014/02/08  修改数据库操作

2014/02/14  修复并发安全

2014/02/18  增加说明一栏
