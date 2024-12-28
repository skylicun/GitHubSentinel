import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime  # 导入datetime模块用于获取日期和时间
import os  # 导入os模块用于文件和目录操作
from logger import LOG  # 导入日志模块

class DoubanMovieClient:

    def __init__(self):
        self.url = 'https://movie.douban.com/top250'  # douban的URL
        # 消息头
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                       AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    def fetch_top_stories(self):
        LOG.debug("准备获取豆瓣电影的TOP数据。")
        try:
            page = urllib.request.Request(self.url, headers=self.headers)
            page = urllib.request.urlopen(page)
            contents = page.read()
            top_stories = self.parse_stories(contents)  # 解析数据
            return top_stories
        except Exception as e:
            LOG.error(f"获取豆瓣电影的TOP数据失败：{str(e)}")
            return []

    def parse_stories(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        top_stories = []
        for tag in soup.find_all(attrs={"class": "item"}):
            # 爬取序号
            num = tag.find('em').get_text()
            # 电影名称
            name = tag.find_all(attrs={"class": "title"})
            zwname = name[0].get_text()
            # 网页链接
            url_movie = tag.find(attrs={"class": "hd"}).a
            urls = url_movie.attrs['href']
            # 爬取评分和评论数
            info = tag.find(attrs={"class": "star"}).get_text()
            info = info.replace('\n', ' ')
            info = info.lstrip()
            print('[评分评论]', info)
            # 获取评语
            content = ''
            info = tag.find(attrs={"class": "inq"})
            if (info):  # 避免没有影评调用get_text()报错
                content = info.get_text()
            top_stories.append({'num': num, 'zwname': zwname, 'urls':urls, 'content': content})
        LOG.info(f"成功解析 {len(top_stories)} 条豆瓣电影。")
        return top_stories

    def export_top_stories(self, date=None, hour=None):
        LOG.debug("准备导出豆瓣电影的TOP数据。")
        top_stories = self.fetch_top_stories()  # 获取数据

        if not top_stories:
            LOG.warning("未找到任何豆瓣电影的数据。")
            return None

        # 如果未提供 date 和 hour 参数，使用当前日期和时间
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        if hour is None:
            hour = datetime.now().strftime('%H')

        # 构建存储路径
        dir_path = os.path.join('douban_movie', date)
        os.makedirs(dir_path, exist_ok=True)  # 确保目录存在
        file_path = os.path.join(dir_path, f'{hour}.md')  # 定义文件路径
        with open(file_path, 'w') as file:
            file.write(f"# douban movie top stories ({date} {hour}:00)\n\n")
            for idx, story in enumerate(top_stories, start=1):
                file.write(f"{idx}. [{story['num']}]({story['zwname']})\n")
        LOG.info(f"豆瓣电影文件生成：{file_path}")
        return file_path

if __name__ == "__main__":
    douban_movie_client = DoubanMovieClient()
    douban_movie_client.export_top_stories()