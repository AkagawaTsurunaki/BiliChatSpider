# BiliChatSpider 
By AkagawaTsurunaki.

## Introduction

A spider script which can crawl the comments under videos from Bilibili.

## Requirement

Use pip command to install all of required libs.

```shell
pip install -r requirements.txt
```
## Configuration

You can find the configuration file in `.\config\chat_spider_config.py`,

`firefox_profile_dir`: path of the profile folder of Firefox, 
which contains your personal information, 
for instance, your login cookies. 
Without login, you may only check 3 comments below for each specified video in Bilibili. 
So you should login first and then start BiliChatSpider.

`firefox_driver_dir`: path of the driver of Firefox. 
To launch Selenium successfully, 
you must download driver with corresponding Firefox version. 

`save_path`: path where the comments data will be stored. We default it to `.\dataset`.

`sleep_time_before_job_launching`: the seconds a process will sleep before a job launches.

`sleep_time_after_job_launching`: the seconds a process will sleep after a job launched. 

`max_parallel_job_num`: BiliChatSpider uses multiprocess, 
this argument specifies how many processes will be started in parallel.

## How to Start?

For instance, you want to crawl 4 hosts, which names are `嘉然今天吃什么`, `向晚大魔王`, `乃琳Queen` and `珈乐Carol`.
In terminal please use command like following:
```shell
cd D:\AkagawaTsurunaki\WorkSpace\PycharmProjects\BiliChatSpider
conda activate BiliChatSpider
python ./main.py `
-l 672328094 672346917 672342685 351609538`
```

And BiliChatSpider will automatically start and save comments data.

`-l` or `--list`: a string list about the uid you want to crawl.

`-f` or `--force`: Force the script to update the history cache, default to `'N'`, opposite to `Y`.
BiliChatSpider will first open a page to get `up_name` 
and then traverse the whole space to get the video list and store it in default path `.\dataset\history.json`. 

`-t` or `--time`: Set the time BiliChatSpider will start automatically.

## License
APACHE LICENSE, VERSION 2.0

More detail to see https://www.apache.org/licenses/LICENSE-2.0.html