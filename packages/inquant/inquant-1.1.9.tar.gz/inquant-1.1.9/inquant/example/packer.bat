@echo off

echo 输入Anaconda根目录，(如C:\ProgramData\Anaconda3）: 
set /p anacondapath=%~1

echo 输入python文件路径，(如C:\inquant\example\MyStrategy.py）: 
set /p pythonfile= %~2

echo 开始打包
pyinstaller -F --add-data=%anacondapath%\Lib\site-packages\inquant\libs\InQuant.OpenApi.dll;. --add-data=%anacondapath%\Lib\site-packages\inquant\libs\Newtonsoft.Json.dll;. --add-data=%anacondapath%\Lib\site-packages\Python.Runtime.dll;. %pythonfile%

echo 拷贝json文件
xcopy %pythonfile%\..\*.json  dist /dy

pause