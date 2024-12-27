import time
import datetime
import schedule
from hacker_llm import HackerLLM
from hacker_fetch import HackerFetch
from report_generator import ReportGenerator


class HackerDaemon:
    def __init__(self):
        self.llm = HackerLLM()
        self.fetch = HackerFetch(self.llm)
        self.report_generator = ReportGenerator(self.llm)
        # 每分钟运行
        schedule.every().minute.do(self.run_hacker)

    def run_hacker(self):
        """运行 Hacker News 抓取和报告生成."""
        # 执行爬虫任务
        self.fetch.summarize()
        current_file = self.fetch.current_file
        # 生成报告
        self.report_generator.generate_daily_report(current_file)

    def run(self):
        """运行调度循环."""
        # 立即执行一次爬取任务
        self.run_hacker()

        while True:
            schedule.run_pending()  # 运行所有待定的任务
            time.sleep(1)  # 等待一秒

def main():
    daemon = HackerDaemon()  # 创建HackerNewsDaemon实例
    daemon.run()  # 启动调度循环

if __name__ == "__main__":
    main()