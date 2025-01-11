### News Fetcher

#### 介绍

**News Fetcher** 是一个命令行工具，用于从指定的RSS源获取最新新闻。它通过解析RSS源，提取新闻标题、链接、发布日期和摘要，并允许用户选择查看特定新闻的详细内容。

#### 原理

1. **RSS解析**：
   - 使用 `feedparser` 库解析RSS源。`feedparser` 是一个强大的Python库，可以自动处理多种RSS和Atom源的解析。
   - 通过发送HTTP请求获取RSS源的XML内容，并解析为Python对象。

2. **编码处理**：
   - 使用 `requests` 库发送HTTP请求，并显式指定响应内容的编码为UTF-8，以确保解析过程中的编码一致性。
   - 使用正则表达式和 `html.unescape` 函数去除HTML标签并解码HTML实体，使输出内容更易读。

3. **用户交互**：
   - 提供一个简单的命令行菜单，用户可以输入新闻编号来查看详细内容。
   - 用户可以输入 `q` 退出程序。

#### 制作流程

1. **安装必要的库**：
   - 安装 `feedparser` 和 `requests` 库：
     ```sh
     pip install feedparser requests
     ```

2. **编写脚本**：
   - 创建一个Python脚本文件，例如 `news_fetcher.py`。
   - 导入必要的模块：
     ```python
     import feedparser
     import sys
     import argparse
     from html import unescape
     import re
     import requests
     import time
     ```

3. **定义清理HTML标签的函数**：
   - 使用正则表达式去除HTML标签，并解码HTML实体：
     ```python
     def clean_html(raw_html):
         cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
         cleantext = re.sub(cleanr, '', raw_html)
         return unescape(cleantext)
     ```

4. **定义获取新闻的函数**：
   - 发送HTTP请求获取RSS源内容，解析RSS源，并处理编码问题：
     ```python
     def fetch_news(url, max_retries=3, retry_delay=5):
         retries = 0
         while retries <= max_retries:
             try:
                 response = requests.get(url)
                 response.encoding = 'utf-8'
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
     ```

5. **定义主函数**：
   - 使用 `argparse` 库处理命令行参数：
     ```python
     def main():
         parser = argparse.ArgumentParser(description="从RSS源获取最新新闻")
         parser.add_argument("url", help="新闻源的RSS URL")
         args = parser.parse_args()

         fetch_news(args.url)

     if __name__ == "__main__":
         main()
     ```

6. **运行脚本**：
   - 保存脚本并运行：
     ```sh
     python news_fetcher.py http://www.people.com.cn/rss/politics.xml
     ```

#### 使用说明(示例)

1. **安装必要的库**：
   ```sh
   pip install feedparser requests
   ```

2. **运行脚本**：
   ```sh
   python news_fetcher.py http://www.people.com.cn/rss/politics.xml
   ```

3. **查看新闻**：
   - 脚本将列出所有新闻条目，用户可以输入编号查看详细内容，或输入 `q` 退出程序。

#### 示例输出

```
1. 【央视快评】坚定法治自信 强化使命担当
   链接: http://politics.people.com.cn/n1/2025/0111/c1001-40399947.html
   发布日期: 2025-01-11
--------------------------------------------------------------------------------
2. 看图学习丨对这支特殊队伍 总书记关心关怀、寄予厚望
   链接: http://politics.people.com.cn/n1/2025/0111/c1001-40399948.html
   发布日期: 2025-01-11
--------------------------------------------------------------------------------
3. 习近平：聚焦主责主业深化改革创新加强自身建设 以高质量审计监督护航经济社会高质量发展
   链接: http://politics.people.com.cn/n1/2025/0111/c1024-40399941.html
   发布日期: 2025-01-11
--------------------------------------------------------------------------------
请输入要查看的新闻编号（或输入'q'退出）: 1
标题: 【央视快评】坚定法治自信 强化使命担当
链接: http://politics.people.com.cn/n1/2025/0111/c1001-40399947.html
发布日期: 2025-01-11
摘要: 坚持党的全面领导，坚持走中国特色社会主义法治道路，坚持服务党和国家工作大局，进一步加强自身建设，更好发挥桥梁纽带作用，扎实做好繁荣法学研究、服务法治实践、加强法治宣传、培养法治人才等工作，努力开创法学会事业发展新局面。”在中国法学会第九次全国会员代表大会召开之际，习近平总书记致信大会，向全国广大法学法律工作者致以问候，并对做好法学会工作提出希望。
--------------------------------------------------------------------------------
请输入要查看的新闻编号（或输入'q'退出）: 
```

希望这个文档能帮助您更好地理解和使用 **News Fetcher** 工具。如果您有任何问题或需要进一步的帮助，请随时告诉我。
联系：u2074426447@163.com
