
# UESTC 研究生每日报平安 打卡脚本

 
## 背景
```angular2html
由于自己经常忘了打卡，于是写了一个脚本挂在服务器上帮我打卡……
由于技术比较菜，破解不来信息门户的登录，所以只有用selenium这种资源消耗比较大的方式来完成
代码中也有比较多的BUG，欢迎提PR
```
## 依赖
* Python 3
* requests
* selenium

## 准备工作
```angular2html
1. pip install -r requirements.txt
2. 百度server酱官网注册获取sckey(vx推送信息比较方便)

```
 
## 使用方法
1. 编辑 config.py 文件里面的信息
2. 定时执行脚本 python mrbpa.py
    - linux crontab 定时执行
    - windows 右键"我的电脑"，选择"管理"，里面有任务计划程序，配置成开机启动就OK
 
## 联系方式      
* leeejjjie@gmail.comm
 
## 常见问题
```angular2html
1. vx推送有时候会失败，如果配置server酱后没有接到打卡成功或者失败的通知，请及时检查打卡信息
2. sm.ms图床有些时候会挂掉，而且使用有一定信息泄露的风险。使用该模块的目的是将本日打卡详情通过server酱发送到vx。同时程序设置了会自动删除上一日上床的图片。请用户自己权衡是否使用
3. 验证码识别服务器是自己建的一个小水管，可能会挂掉。还是推荐大家使用打码平台
