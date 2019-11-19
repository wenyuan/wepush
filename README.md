# WePush
> 微信推送通知服务（WeChat notification service）

## 一、环境
* Ubuntu 16.04
* Python 2.7

## 二、部署
### 1. 检查Python环境
　　确保Python2.7和pip9.0.1左右
```bash
python -V
pip -V
```

### 2. 上传项目并安装依赖软件库
```bash
sudo pip install -r requirements.txt
```

### 3. 安装和配置nginx
　　安装和配置过程省去。

### 4. 安装和配置supervisor
　　让supervisor管理进程，可以在进程发生意外的情况下，自动重启服务。

### 5. 配置文件
　　从 `settings.examples.py` 拷贝一份 `settings.py`。
```bash
cp settings.examples.py settings.py
```
　　编辑配置文件。
```bash
vim settings.py
```
　　设置如下几个参数：
```bash
SECRET_KEY = '新建Django项目会自动生成SECRET_KEY'

DEBUG = False

WECHAT_TOKEN = '填写你的令牌(Token)'
WECHAT_APPID = '填写你的开发者ID(AppID)'
WECHAT_APPSECRET = '填写你的开发者密码(AppSecret)'
```

### 6. 启动nginx和supervisor
　　启动前创建几个目录。
```bash
# nginx需要
sudo mkdir -p /var/log/nginx/
sudo mkdir -p /var/log/nginx/access/
# supervisor需要
sudo mkdir -p /var/log/supervisor/
# 该django项目需要，和static目录平级
sudo mkdir -p /var/log/uwsgi/
sudo chmod 777 /var/log/uwsgi/
sudo mkdir -p /var/run/uwsgi/
sudo chmod 777 /var/run/uwsgi/
mkdir all_static_files
```
　　启动网站前初始化一下，首先进入 `wepush` 目录，执行下列命令
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py compilemessages
python manage.py collectstatic
python manage.py project_helper/createsuperuser
```
　　测试运行，前台启动服务并访问网站测试。
```bash
python manage.py runserver 0:8080
```

### 7. 登录微信公众平台进行一些设置
　　过程省去。

### 8. 启动nginx和supervisor
　　过程省去。


## 三、主要更新记录
* 2019.11.13
  * 功能实现：对接微信公众平台接口测试帐号


## 四、参考链接
* [微信公众平台开发文档](https://mp.weixin.qq.com/ "微信公众平台开发文档")
* [微信公众平台接口测试平台](https://mp.weixin.qq.com/debug/cgi-bin/sandbox?t=sandbox/login "微信公众平台接口测试平台")
