import os
import requests
from bs4 import BeautifulSoup  # 确保导入BeautifulSoup用于HTML解析
from datetime import datetime  # 导入datetime模块以获取当前日期
from hacker_llm import HackerLLM  # HackerLLM
from logger import LOG  # 导入日志模块

class HackerFetch:
    def __init__(self, hacker_llm):
        self.url = 'https://news.ycombinator.com/'
        # 设置浏览器的 header 和 referer
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            'Referer': 'https://news.ycombinator.com/',
        }
        self.hacker_llm = hacker_llm

    def fetch_top_stories(self):
        """获取 Hacker News 的热门帖子."""
        response = requests.get(self.url, headers=self.headers)
        
        if response.status_code == 200:
            return self.parse_stories(response.text)
        else:
            LOG.info(f"Error fetching page: {response.status_code}")
            return []

    def parse_stories(self, html):
        """解析 HTML 内容并提取标题和链接."""
        stories = []
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.select('.titleline > a'):
            title = item.get_text()
            link = item['href']
            stories.append({'title': title, 'link': link})
        
        return stories

    def top_stories(self):
        return self.fetch_top_stories()
    
    def top_stories_summarize(self):
        """获取 Hacker News 热门帖子并生成总结."""
        titles = self.fetch_top_stories()
        markdown_content = "\n".join(f"- [{story['title']}]({story['link']})" for story in titles)
        return self.hacker_llm.generate_daily_report(markdown_content) 
    
    def write_to_file(self, content):
        directory = "daily_progress/hacker_news"
        os.makedirs(directory, exist_ok=True)
        # 获取当前日期并格式化为isodate
        current_date = datetime.now().isoformat().replace(":","_")
        output_filename = f"hackernews_content_{current_date}.md"
        # 写入文件
        full_file_path = os.path.join(directory, output_filename)
        self.current_file = full_file_path
        with open(full_file_path, "w", encoding='utf-8') as file:
            file.write(content)
        LOG.info(f"Content written to {full_file_path}")

    def summarize(self):
        """获取网站数据并生成总结."""
        titles = self.fetch_top_stories()
        markdown_content = "\n".join(f"- [{story['title']}]({story['link']})" for story in titles)
        self.write_to_file(markdown_content)

if __name__ == "__main__":
    hacker_llm = HackerLLM()
    fetch = HackerFetch(hacker_llm)
    fetch.summarize()