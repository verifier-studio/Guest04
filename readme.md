- 打包
```
pyinstaller -F -w win.py -n Guest04.exe
```
- 导出依赖

```
pip freeze > requirements.txt
```

- 安装依赖

```
pip install -r requirements.txt
```