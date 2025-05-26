import gradio as gr

def slow_function(text):
    # Simulate a slow operation
    import time
    time.sleep(5)
    return f"Processed: {text}"

with gr.Blocks() as demo:
    with gr.Row():
        text_input = gr.Textbox(label="Input")
        with gr.Column():
            btn1 = gr.Button("Process with scroll_on_click only", variant="primary")
            btn2 = gr.Button("Process with scroll_to_output only", variant="secondary")
            btn3 = gr.Button("Process with Both scrolling", variant="secondary")
            btn4 = gr.Button("Process with no scrolling", variant="secondary")
    with gr.Row():
        gr.HTML(f"<p>gradio version:{gr.__version__}</p>")
    
    output = gr.Textbox(label="Output")
    
    btn1.click(fn=slow_function, inputs=text_input, outputs=output, scroll_on_click=True, scroll_to_output=False)
    btn2.click(fn=slow_function, inputs=text_input, outputs=output, scroll_on_click=False, scroll_to_output=True)
    btn3.click(fn=slow_function, inputs=text_input, outputs=output, scroll_on_click=True, scroll_to_output=True)
    btn4.click(fn=slow_function, inputs=text_input, outputs=output, scroll_on_click=False, scroll_to_output=False)

demo.launch()