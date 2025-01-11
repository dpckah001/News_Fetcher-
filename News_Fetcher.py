import feedparser
import sys
import argparse
from html import unescape
import re
import requests

def clean_html(raw_html):
    """清理HTML标签和解码HTML实体"""
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', raw_html)
    return unescape(cleantext)

def fetch_news(url, max_retries=3, retry_delay=5):
    """从给定的RSS URL获取新闻，支持重试机制"""
    retries = 0
    while retries <= max_retries:
        try:
            # 发送HTTP请求获取RSS源内容
            response = requests.get(url)
            response.encoding = 'utf-8'  # 显式指定编码为utf-8
            feed = feedparser.parse(response.text)
            
            if feed.bozo:
                print(f"解析错误: {feed.bozo_exception}")
                if retries < max_retries:
                    print(f"重试中... ({retries + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retries += 1
                else:
                    print("重试次数已达上限，解析失败。")
                    return
            else:
                break
        except Exception as e:
            print(f"解析错误: {e}")
            if retries < max_retries:
                print(f"重试中... ({retries + 1}/{max_retries})")
                time.sleep(retry_delay)
                retries += 1
            else:
                print("重试次数已达上限，解析失败。")
                return

    if not feed.entries:
        print("没有找到任何新闻条目")
        return

    for i, entry in enumerate(feed.entries, start=1):
        print(f"{i}. {entry.title}")
        print(f"   链接: {entry.link}")
        print(f"   发布日期: {entry.published}")
        print("-" * 80)

    while True:
        choice = input("请输入要查看的新闻编号（或输入'q'退出）: ")
        if choice.lower() == 'q':
            break
        try:
            choice = int(choice)
            if 1 <= choice <= len(feed.entries):
                entry = feed.entries[choice - 1]
                print(f"标题: {entry.title}")
                print(f"链接: {entry.link}")
                print(f"发布日期: {entry.published}")
                print(f"摘要: {clean_html(entry.summary)}")
                print("-" * 80)
            else:
                print("无效的编号，请重新输入。")
        except ValueError:
            print("无效的输入，请重新输入。")

def main():
    parser = argparse.ArgumentParser(description="从RSS源获取最新新闻")
    parser.add_argument("url", help="新闻源的RSS URL")
    args = parser.parse_args()

    fetch_news(args.url)

if __name__ == "__main__":
    main()
