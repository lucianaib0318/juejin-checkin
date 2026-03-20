import requests
import time
import datetime
import json
import os

def check_sign_in_status(base_url, headers):
    """检查今日是否已签到"""
    api = "get_today_status"
    url = base_url + api
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data['err_no'] == 0:
            if data['data'] is True:
                print("【今日是否签到】", "已签到")
                return True
            elif data['data'] is False:
                print("【今日是否签到】", "未签到")
                return False
        else:
            print("【当前登录状态】", "未登录，请登录")
            return False
    else:
        print("【请求失败】", response.status_code)
        return False


def sign_in(base_url, params, headers):
    """执行签到"""
    data = ''
    url = f"{base_url}check_in"
    response = requests.post(url, headers=headers, data=data, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
            if data['err_no'] == 0 and data['err_msg'] == "success":
                print("【当前签到状态】", "签到成功")
                return True
            elif data['err_no'] == 3013 and data['err_msg'] == "掘金酱提示：签到失败了~":
                print("【当前签到状态】", data['err_msg'])
                return False
            elif data['err_no'] == 15001:
                print("【当前签到状态】", '重复签到')
                return True
            else:
                print("【当前签到状态】", data['err_msg'])
                return False
        except requests.JSONDecodeError:
            print("【签到功能】服务器返回的数据无法解析为 JSON 格式。")
            return False
    return False


def get_points(base_url, headers):
    """获取当前矿石余额"""
    api = "get_cur_point"
    url = base_url + api
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            if data['err_no'] == 0 and data['err_msg'] == "success":
                print("【矿石最新余额】", data['data'])
                return data['data']
        except requests.JSONDecodeError:
            print("【获取余额功能】服务器返回的数据无法解析为 JSON 格式。")
            return False
    return 0


def get_free(base_url, params, headers):
    """获取免费抽奖次数"""
    url = f"{base_url}lottery_config/get"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
            if data['err_no'] == 0 and data['err_msg'] == "success":
                if data['data']['free_count'] > 0:
                    print("【免费抽奖次数】", data['data']['free_count'])
                    return True
                else:
                    print("【免费抽奖次数】", data['data']['free_count'])
                    return False
        except requests.JSONDecodeError:
            print("【获取免费抽奖次数功能】服务器返回的数据无法解析为 JSON 格式。")
            return False
    return False


def draw(base_url, params, headers):
    """执行抽奖"""
    url = f"{base_url}lottery/draw"
    data = ''
    response = requests.post(url, headers=headers, data=data, params=params)
    if response.status_code == 200:
        try:
            data = response.json()
            if data['err_no'] == 0 and data['err_msg'] == "success":
                prize = data['data']['lottery_name']
                print("【今日抽奖奖品】", prize)
                return prize
        except requests.JSONDecodeError:
            print("【抽奖功能】服务器返回的数据无法解析为 JSON 格式。")
    return None


def get_win(base_url, aid, uuid, spider, headers):
    """获取幸运值"""
    api = "lottery_lucky/my_lucky"
    url = base_url + api
    data = {
        "aid": aid,
        "uuid": uuid,
        "spider": spider
    }
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            if data['err_no'] == 0 and data['err_msg'] == "success":
                total_value = data['data']['total_value']
                print("【当前幸运数值】：", total_value)
                return total_value
        except requests.JSONDecodeError:
            print("【获取幸运值功能】服务器返回的数据无法解析为 JSON 格式。")
    else:
        print("【请求失败】", response.status_code)
    return 0


if __name__ == "__main__":
    timestamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    
    # 从配置文件导入参数
    try:
        from config import COOKIE, AID, UUID, SPIDER, MS_TOKEN, A_BOGUS
    except ImportError:
        print("❌ 错误：请复制 config.example.py 为 config.py 并填写你的配置信息")
        exit(1)
    
    base_url = "https://api.juejin.cn/growth_api/v1/"
    common_params = {"aid": AID, "uuid": UUID, "spider": SPIDER, "msToken": MS_TOKEN, "a_bogus": A_BOGUS}
    header1 = {
        'Cookie': COOKIE,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
    }

    # 结果收集
    results = []
    
    # 签到逻辑
    if check_sign_in_status(base_url, header1):
        results.append("✅ 今日已签到")
        if get_free(base_url, common_params, header1):
            prize = draw(base_url, common_params, header1)
            results.append(f"🎁 已完成抽奖：{prize if prize else '无奖品'}")
        else:
            results.append("🎁 无免费抽奖次数")
    else:
        results.append("⏰ 开始签到...")
        if sign_in(base_url, common_params, header1):
            results.append("✅ 签到成功")
        if get_free(base_url, common_params, header1):
            prize = draw(base_url, common_params, header1)
            results.append(f"🎁 已完成抽奖：{prize if prize else '无奖品'}")
        else:
            results.append("🎁 无免费抽奖次数")
    
    # 获取余额和幸运值
    points = get_points(base_url, header1)
    results.append(f"💰 矿石余额：**{points}**")
    
    lucky_value = get_win(base_url, AID, UUID, SPIDER, header1)
    results.append(f"🍀 幸运值：**{lucky_value}**")
    
    # 构建报告（简洁版，只关注结果）
    sign_result = "✅ 签到成功" if any("签到成功" in r or "已签到" in r for r in results) else "❌ 签到失败"
    lottery_result = "无抽奖"
    for r in results:
        if "抽奖" in r:
            if "已完成抽奖" in r:
                lottery_result = r.replace("🎁 已完成抽奖：", "🎁 ")
            elif "无免费抽奖次数" in r:
                lottery_result = "🎁 无免费次数"
            break
    
    report = f"{sign_result}\n{lottery_result}\n💰 矿石余额：**{points}**\n🍀 幸运值：**{lucky_value}**"
    
    # 写入结果文件（供通知脚本读取）
    result_file = os.path.join(os.path.dirname(__file__), 'last_result.json')
    result_data = {
        "timestamp": timestamp.isoformat(),
        "report": report,
        "success": True,
        "points": points,
        "lucky_value": lucky_value
    }
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, ensure_ascii=False, indent=2)
    
    print("\n=== 本次执行完成 ===")
    print(f"结果已写入：{result_file}")
