import gradio as gr
import os

with gr.Blocks() as demo:
    # Example 1: Sorting with individual Tab.sort_order
    with gr.Tabs() as dynamic_tabs:
        with gr.Tab("Lion", sort_order=3):
            gr.Image(os.path.join(os.path.dirname(__file__), "images/lion.jpg"))
        with gr.Tab("Tiger", sort_order=1):
            gr.Image(os.path.join(os.path.dirname(__file__), "images/tiger.jpg"))
        with gr.Tab("Cheetah", sort_order=2):
            gr.Image(os.path.join(os.path.dirname(__file__), "images/cheetah1.jpg"))
    
    # Example 2: Sorting with Tabs.sort_order (initial setup)
    # Child tabs need explicit 'id' for this to work reliably with parent sort_order
    with gr.Tabs(sort_order=["tiger_tab", "lion_tab", "cheetah_tab"]) as tabs_parent_sorted:
        with gr.Tab("Lion", id="lion_tab") as tab1:
            gr.Image(os.path.join(os.path.dirname(__file__), "images/lion.jpg"))
        with gr.Tab("Tiger", id="tiger_tab") as tab2:
            gr.Image(os.path.join(os.path.dirname(__file__), "images/tiger.jpg"))
        with gr.Tab("Cheetah", id="cheetah_tab") as tab3:
            gr.Image(os.path.join(os.path.dirname(__file__), "images/cheetah1.jpg"))

    # Example 3: Dynamic sorting with an event
    def reorder_parent_sorted_tabs():
        # New order: Cheetah, Lion, Tiger
        return gr.Tabs.update(sort_order=["cheetah_tab", "lion_tab", "tiger_tab"])

    reorder_button = gr.Button("Reorder Second Set of Tabs")
    reorder_button.click(fn=reorder_parent_sorted_tabs, inputs=None, outputs=tabs_parent_sorted)

if __name__ == "__main__":
    demo.launch(share=True)
