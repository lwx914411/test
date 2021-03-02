@echo off
echo 接口自动化-Mock服务准备启动......
@echo on

java -jar moco-runner-1.1.0-standalone.jar http -p 9999 -c test00.json

@echo off
echo Mock服务准备启动成功-端口号-9999
pause