import argparse
from hacker_llm import HackerLLM
from hacker_fetch import HackerFetch

def print_usage():
    """打印使用说明"""
    usage_info = """
    使用说明:
    -----------------------
    1. 获取热门故事: fetch 
    2. 生成趋势分析报告: gensumm
    3. 退出: exit
    -----------------------
    请根据指示输入命令。
    """
    print(usage_info)

def main():
    llm = HackerLLM()
    scraper = HackerFetch(llm)
    while True:
        print_usage()
        command = input("请输入命令: ").strip().lower()
        if command == 'fetch':
            print("Fetching...")
            stories = scraper.top_stories()
            if stories:
                for idx, story in enumerate(stories, start=1):
                    print(f"{idx}. {story['title']} (链接: {story['link']})")
            else:
                print("Not Found...")
        elif command == 'gensumm':
            print("Generating...")
            scraper.summarize()
            print("saved to file...")
        elif command == 'exit':
            print("退出程序。")
            break
        else:
            print("无效命令，请重试。")

if __name__ == "__main__":
    main()