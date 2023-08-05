通过命令行生成tmuxinator需要的配置文件

**Important:**大量代码来自于小米云存储FDS/EMQ/EMR组的大神yepeng1, 我只是重新抄了一遍

Usage:

Setup `~/.config/xiaomi/config` and put this message in it:

```
{
...
  "xiaomi_minos1_config_path": "/home/hujianxin/Xiaomi/deployment-config/",
  "xiaomi_minos2_config_path": "/home/hujianxin/Xiaomi/deployment/",
  "xiaomi_username": "your_name"
...
}
```

`sudo pip install muxminos`

```
> mm
Type:        MuxMinos
String form: <muxminos.cmd.MuxMinos object at 0x7f38ca214b38>
File:        /usr/local/lib/python3.5/dist-packages/muxminos/cmd.py

Usage:       mm 
             mm g
             mm u

```
