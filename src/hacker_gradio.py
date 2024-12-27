import gradio as gr
from hacker_llm import HackerLLM
from hacker_fetch import HackerFetch

llm = HackerLLM()
fetch = HackerFetch(llm)

class HackerPageData:
    def __init__(self, new_fetcher):
        self.hn = new_fetcher 
        self.markdown_height=500
    
    # 获取数据
    def fetch_hacker_data(self, limit=10):
        top_stories = fetch.top_stories()[:limit]
        articles = []
        for story in top_stories:
            if story and "title" in story and "link" in story:
                articles.append({
                    "title": story["title"],
                    "link": story["link"]
                })
        return articles

    # 显示总结
    def display_article(self, index, articles):
        selected_article = articles[index]
        return selected_article["summary"]

pageData = HackerPageData(fetch)

# 抓取数据
def getNews(slider):
    print(slider)
    md = "\n".join(f"- [{story['title']}]({story['link']})" for story in pageData.fetch_hacker_data(slider))
    return md 

def updatePageData(news, summary, slider):
    news = gr.Markdown(value=getNews(slider), height=pageData.markdown_height)
    summary = gr.Markdown(value=fetch.top_stories_summarize(), height=pageData.markdown_height)

# 创建Gradio
with gr.Blocks() as demo:

    gr.Markdown("Hacker News")
    
    reload_button=gr.Button(value="刷新")

    with gr.Row():
        report_period_slider = gr.Slider(
            value=10,
            minimum=1,
            maximum=30,
            step=1,
            label="TOP条数",
            info="生成TOP条数，单位：条"
        )
    
    with gr.Row():
        with gr.Column():
            news_list = gr.Markdown(value=getNews(10), height=pageData.markdown_height)
        with gr.Column():
            summary_display = gr.Markdown(value=fetch.top_stories_summarize(), height=pageData.markdown_height)

    reload_button.click(lambda: updatePageData(news_list, summary_display, report_period_slider.value))

demo.launch()