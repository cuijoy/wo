# -*- coding: utf-8 -*-
import json,re,requests

keyurl=[
    {
      "womail_url": "https://nyan.mail.wo.cn/cn/sign/index/index?mobile=MC6qDoe=&openId=L9uZXQLqCrW%2F9p7VLJfItHgt2fWtM8L5nTSw%3D"  #1手机号
    },
    {
      "womail_url": "https://nyan.mail.wo.cn/cn/sign/index/index?mobile=ahtGjqz8OD&userName=&openId=pT9AwnkRFfb%2FIW%2BBiNCPFGeUM%2F%2B6SzRSWudpE%3D"  #2手机
    },
    {
      "womail_url": "https://nyan.mail.wo.cn/cn/sign/index/index?mobile=FxSmqJctRuserName=&openId=whrMGx6RNoL8AjPuxz4lJgBQ6G2NQ%3D"  #3手机号
    },
    {
      "womail_url": "https://nyan.mail.wo.cn/cn/sign/index/index?mobile=fIV2&userName=&openId=sKL2cviF7GrimgavlTdnyGkLcu9Q85J6%2BFNoo7uCGQk%3D"  #4
    },
    {
      "womail_url": "https://nyan.mail.wo.cn/cn/sign/index/index?mobile=YTJrZVeQD%3D&userName=&openId=9olc65zn2z5F2p8hOGwl%2BM37M%3D"  #5手机
    },
    {
      "womail_url": "https://nyan.mail.wo.cn/cn/sign/index/index?mobile=6ldserName=&openId=%2BqnGvZFklxGo9AEFuPTaK2U%3D"  #6手机号
    }
]

class WoMailCheckIn:
    def __init__(self, check_item):
        self.check_item = check_item

    @staticmethod
    def login(womail_url):
        # 登录获取Cookie
        try:
            url = womail_url
            headers = {
                "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"
            }
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("YZKF_SESSION.*?;", set_cookie)[0]
            if "YZKF_SESSION" in cookies:

                return cookies

            else:
                print("沃邮箱获取 cookies 失败")
                return None
        except Exception as e:
            print("沃邮箱错误:", e)
            return None

    @staticmethod
    def dotask(cookies):
        msg = ""
        headers = {
            "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
            "Cookie": cookies,
        }
        # 获取用户信息
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/index/userinfo.do?rand=0.8897817905278955"
            res = requests.post(url=url, headers=headers)
            result = res.json()
            wxName = result.get("result").get("wxName")
            userMobile = result.get("result").get("userMobile")
            userdata = f"帐号信息: {wxName} - {userMobile[:3]}****{userMobile[-4:]}\n"
            msg += userdata
        except Exception as e:
            print("沃邮箱获取用户信息失败", e)
            msg += "沃邮箱获取用户信息失败\n"
        # 执行签到任务
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/checkin.do?rand=0.913524814493383"
            res = requests.post(url=url, headers=headers).json()
            result = res.get("result")
            if result == -2:
                msg += "每日签到: 已签到\n"
            elif result is None:
                msg += f"每日签到: 签到失败\n"
            else:
                msg += f"每日签到: 签到成功~已签到{result}天！\n"
        except Exception as e:
            print("沃邮箱签到错误", e)
            msg += "沃邮箱签到错误\n"
        # 执行其他任务
        try:
            url = "https://nyan.mail.wo.cn/cn/sign/user/doTask.do?rand=0.8776674762904109"
            data_params = {
                "每日首次登录手机邮箱": {"taskName": "loginmail"},
                "和WOWO熊一起寻宝": {"taskName": "treasure"},
                "去用户俱乐部逛一逛": {"taskName": "club"},
                "小积分抽大奖": {"taskName": "clubactivity"},
                "每日答题赢奖": {"taskName": "answer"},
            }
            for key, data in dict.items(data_params):
                try:
                    res = requests.post(url=url, data=data, headers=headers).json()
                    result = res.get("result")
                    if result == 1:
                        msg += f"{key}: 做任务成功\n"
                    elif result == -1:
                        msg += f"{key}: 任务已做过\n"
                    elif result == -2:
                        msg += f"{key}: 请检查登录状态\n"
                    else:
                        msg += f"{key}: 未知错误\n"
                except Exception as e:
                    print(f"沃邮箱执行任务【{key}】错误", e)
                    msg += f"沃邮箱执行任务【{key}】错误"

        except Exception as e:
            print("沃邮箱执行任务错误", e)
            msg += "沃邮箱执行任务错误错误"
        return msg

    @staticmethod
    def dotask2(womail_url):
        msg = ""
        userdata = re.findall("mobile.*", womail_url)[0]
        url = "https://club.mail.wo.cn/clubwebservice/?" + userdata
        headers = {
            "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400"

        }
        # 获取俱乐部cookies
        try:
            res = requests.get(url=url, headers=headers, allow_redirects=False)
            set_cookie = res.headers["Set-Cookie"]
            cookies = re.findall("SESSION.*?;", set_cookie)[0]
            if "SESSION" in cookies:
                headers = {
                    "User-Agent": "User-Agent: Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3868.400 QQBrowser/10.8.4394.400",
                    "Cookie": cookies,
                    "Referer": "https://club.mail.wo.cn/clubwebservice/club-user/user-info/mine-task"
                }
                # 获取俱乐部用户信息
                try:
                    url = "https://club.mail.wo.cn/clubwebservice/club-user/user-info/get-user-score-info/"
                    res = requests.get(url=url, headers=headers)
                    result = res.json()
                    integralTotal = result.get("integralTotal")
                    userMobile = result.get("userPhoneNum")
                    userdata = f"帐号信息: {userMobile[:3]}****{userMobile[-4:]} - 当前积分:{integralTotal}\n"
                    msg += userdata
                    # url_params = {
                    #     "每日签到": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create",
                    #     "参与活动": f"https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum={userMobile}&resourceType=huodong",
                    #     "沃邮箱邮件查看": f"https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum={userMobile}&resourceType=lookMail",
                    #     "沃门户": f"https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum={userMobile}&resourceType=womenhuzhuye",
                    # }

                    # 优先从云端获取积分任务
                    datas = requests.get(
                        url="https://api.github.com/repos/rbzan/womail/issues?state=open&labels=integralTaskData").json()

                    integralTaskData = datas[0]["body"]
                    if integralTaskData:
                        integralTaskData = json.loads(integralTaskData)
                        print("云端获取积分任务")
                        #msg += "云端获取积分任务\n"
                    else:
                        print("本地获取积分任务")
                        #msg += "本地获取积分任务\n"
                        integralTaskData = [
                            {
                                "resourceName": "每日签到（积分）",
                                "url": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create"
                            },
                            {
                                "irid": 539,
                                "resourceName": "参与俱乐部活动",
                                "resourceFlag": "Web_canyujulebuhuodong+2jifen",
                                "taskState": 0,
                                "scoreNum": 1,
                                "scoreResourceType": "add",
                                "attachData": "{\"jumpLink\":\"/clubwebservice/club-index/activity-scope?currentPage=activityScope\"}",
                                "description": "Web端参与俱乐部活动+1积分"
                            },
                            {
                                "irid": 545,
                                "resourceName": "俱乐部积分兑换",
                                "resourceFlag": "Web_jifenduihuan+2jifen",
                                "taskState": 0,
                                "scoreNum": 1,
                                "scoreResourceType": "add",
                                "attachData": "{\"jumpLink\":\"/clubwebservice/score-exchange/into-score-exchange?currentPage=js-hover\"}",
                                "description": "Web端积分兑换+1积分"
                            }
                        ]

                    lenth = len(integralTaskData)
                    #msg+="--------积分任务--------\n"
                    # 执行积分任务
                    for i in range(lenth):

                        resourceName = integralTaskData[i]["resourceName"]

                        try:
                            if "每日签到" in resourceName:
                                url = integralTaskData[i]["url"]
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                if "success" in result:
                                    continuousDay = res["data"]["continuousDay"]
                                    msg += f"{resourceName}: 签到成功~已连续签到{str(continuousDay)}天！\n"
                                else:
                                    msg += f"{resourceName}: {result}\n"
                            else:
                                resourceFlag = integralTaskData[i]["resourceFlag"]
                                resourceFlag = resourceFlag.replace("+", "%2B")
                                url = f"https://club.mail.wo.cn/clubwebservice/growth/addIntegral?phoneNum={userMobile}&resourceType={resourceFlag}"
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                msg += f"{resourceName}: {result}\n"
                        except Exception as e:
                            print(f"沃邮箱俱乐部执行任务【{resourceName}】错误", e)
                            msg += f"沃邮箱俱乐部执行任务【{resourceName}】错误"
                    # 优先云端获取成长值任务
                    datas = requests.get(
                        url="https://api.github.com/repos/rbzan/womail/issues?state=open&labels=growthtaskData").json()

                    growthtaskData = datas[0]["body"]
                    if growthtaskData:
                        growthtaskData = json.loads(growthtaskData)
                        print("云端获取成长值任务")
                        #msg += "云端获取积分任务\n"
                    else:
                        print("本地获取成长值任务")
                        #msg += "本地获取积分任务\n"
                        growthtaskData = [
                            {
                                "resourceName": "每日签到（积分）",
                                "url": "https://club.mail.wo.cn/clubwebservice/club-user/user-sign/create"
                            },
                            {
                                "irid": 539,
                                "resourceName": "参与俱乐部活动",
                                "resourceFlag": "Web_canyujulebuhuodong+2jifen",
                                "taskState": 0,
                                "scoreNum": 1,
                                "scoreResourceType": "add",
                                "attachData": "{\"jumpLink\":\"/clubwebservice/club-index/activity-scope?currentPage=activityScope\"}",
                                "description": "Web端参与俱乐部活动+1积分"
                            },
                            {
                                "irid": 545,
                                "resourceName": "俱乐部积分兑换",
                                "resourceFlag": "Web_jifenduihuan+2jifen",
                                "taskState": 0,
                                "scoreNum": 1,
                                "scoreResourceType": "add",
                                "attachData": "{\"jumpLink\":\"/clubwebservice/score-exchange/into-score-exchange?currentPage=js-hover\"}",
                                "description": "Web端积分兑换+1积分"
                            }
                        ]

                    # 执行成长值任务
                    lenth = len(growthtaskData)
                    #msg += "--------成长值任务--------\n"
                    for i in range(lenth):

                        resourceName = growthtaskData[i]["resourceName"]

                        try:
                            if "每日签到" in resourceName:
                                url = growthtaskData[i]["url"]
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                if "success" in result:
                                    continuousDay = res["data"]["continuousDay"]
                                    msg += f"{resourceName}: 签到成功~已连续签到{str(continuousDay)}天！\n"
                                else:
                                    msg += f"{resourceName}: {result}\n"
                            else:
                                resourceFlag = growthtaskData[i]["resourceFlag"]
                                resourceFlag = resourceFlag.replace("+", "%2B")
                                url = f"https://club.mail.wo.cn/clubwebservice/growth/addGrowthViaTask?phoneNum={userMobile}&resourceType={resourceFlag}"
                                res = requests.get(url=url, headers=headers).json()
                                result = res.get("description")
                                msg += f"{resourceName}: {result}\n"
                        except Exception as e:
                            print(f"沃邮箱俱乐部执行任务【{resourceName}】错误", e)
                            msg += f"沃邮箱俱乐部执行任务【{resourceName}】错误"



                except Exception as e:
                    print("沃邮箱俱乐部获取用户信息失败", e)
                    msg += "沃邮箱俱乐部获取用户信息失败\n"
            else:
                msg += "沃邮箱俱乐部获取SESSION失败\n"


        except Exception as e:
            print("沃邮箱俱乐部获取cookies失败", e)
            msg += "沃邮箱俱乐部获取cookies失败\n"

        return msg

    def main(self):
        womail_url = self.check_item.get("womail_url")
        try:
            cookies = self.login(womail_url)
            if cookies:
                msg = self.dotask(cookies)
                msg1 = self.dotask2(womail_url)
                msg += f"\n【沃邮箱俱乐部】\n{msg1}"
            else:
                msg = "登录失败"
        except Exception as e:
            print(e)
            msg = "登录失败"
        return msg

def main_handler(event, context):
    for i in keyurl:
        print(WoMailCheckIn(check_item=i).main())

if __name__ == '__main__':
    main_handler("", "")