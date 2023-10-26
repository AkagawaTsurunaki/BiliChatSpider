# BiliChatSpider 
By AkagawaTsurunaki.

A spider script which can crawl the comments under videos from Bilibili. 
Supports automatic checkpoint recovery of historical records, basic data cleaning, and basic data statistics.

## Requirement


### Firefox Browser

You can download and install Firefox browser through the following link:

https://www.firefox.com.cn/

### Firefox Geckodriver

You can download Firefox geckodriver through the following link:

https://github.com/mozilla/geckodriver/releases

Remember that the version of browser and driver should correspond.

Use pip command to install all of required libs.

### Python

We suppose you have installed Python in your computer. 
Then you should install all dependencies through this command.

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
python ./bili.py `
-l 672328094 672346917 672342685 351609538`
```

And BiliChatSpider will automatically start and save comments data.

`-l` or `--list`: A string list about the uid you want to crawl.

`-f` or `--force`: Force the script to update the history cache, default to `'N'`, opposite to `Y`.
BiliChatSpider will first open a page to get `up_name` 
and then traverse the whole space to get the video list and store it in default path `.\dataset\history.json`. 

`-t` or `--time`: Set the time BiliChatSpider will start automatically.

If you want to crawl the videos related to specified uid. 
In terminal please use command like following:

```shell
python ./bili.py `
-u 672328094 `
-b BV14m4y1V7oj BV1Mm4y1V7R BV1Jw41117Zk
```

`-u` or `--uid`: The ID of an UP.

`-b` or `--bv`: A string list of bv number related to the videos you want to crawl.

## Data Clean

You should clean data with using command following
```shell
python clean.py
```
Remember we set `./dataset` as default save path!

The cleaned data will be written in default directory
`./data_clean/train.json`.

## Print Statistic Result
Use command following to print what you have collected from Bilibili.
```shell
python ./bilibili_statistic.py
```

The output format will be as follows.
```
{index} ({uid}): {number_of_comments}
...
Total: {total_number_of_all_comments}
```

## Author
### AkagawaTsurunaki 

E-mail: <a>AkagawaTsurunaki@outlook.com</a>

Github: <a>https://github.com/AkagawaTsurunaki </a>

If you have any questions, please raise them in the issue or contact me via E-mail.
Thank you for your support and contributions to this project.
## License
APACHE LICENSE, VERSION 2.0

For more details, please refer to https://www.apache.org/licenses/LICENSE-2.0.html