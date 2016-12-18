# crontab-python3
自动运行定时任务

##使用方法
1. 编辑同目录下的crontab.txt
2. 添加crontab.py到开机自启动

##规则格式
基本格式 : crontab的简化版

时间标准 : Greenwich Mean Time(GMT)

*　　*　　*　　*　　*　　command

分　时　日　月　周　命令

第1列表示分钟0～59

第2列表示小时0～23

第3列表示日期1～31

第4列表示月份1～12

第5列标识号星期0～6（0表示星期天）

第6列要运行的命令

示例 :
30 21 * * * /usr/local/etc/rc.d/lighttpd restart 
每晚的21:30重启apache。 