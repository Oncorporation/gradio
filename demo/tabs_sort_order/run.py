import gradio as gr
import os

with gr.Blocks() as demo:
    with gr.Tabs() as dynamic_tabs:
        with gr.Tab("Lion", sort_order=3):
            gr.Image(os.path.join(os.path.dirname(__file__), "images/lion.jpg"))
        with gr.Tab("Tiger", sort_order=1):
            gr.Image(os.path.join(os.path.dirname(__file__), "images/tiger.jpg"))
        with gr.Tab("Cheetah", sort_order=2):
            gr.Image(os.path.join(os.path.dirname(__file__), "images/cheetah1.jpg"))
        gr.update(sort_order=[tab._id for tab in dynamic_tabs.children if isinstance(tab, gr.Tab)])

    with gr.Tabs() as tabs:
        with gr.Tab("Lion") as tab1:
            gr.Image(os.path.join(os.path.dirname(__file__), "images/lion.jpg"))
        with gr.Tab("Tiger") as tab2:
            gr.Image(os.path.join(os.path.dirname(__file__), "images/tiger.jpg"))
        with gr.Tab("Cheetah") as tab3:
            gr.Image(os.path.join(os.path.dirname(__file__), "images/cheetah1.jpg"))
        gr.update(sort_order=[tab2._id, tab1._id, tab3._id])

if __name__ == "__main__":
    demo.launch(share=True)
