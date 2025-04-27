# Using scroll_on_click in Gradio

The `scroll_on_click` parameter allows you to automatically scroll to the output components when a button is clicked, rather than waiting for the function to complete (which is what `scroll_to_output` does).

## Example Usage

import gradio as gr

def slow_function(text):
    # Simulate a slow operation
    import time
    time.sleep(3)
    return f"Processed: {text}"

with gr.Blocks() as demo:
    with gr.Row():
        text_input = gr.Textbox(label="Input")
        with gr.Column():
            btn1 = gr.Button("Process with scroll_on_click", variant="primary")
            btn2 = gr.Button("Process with scroll_to_output", variant="secondary")
            btn3 = gr.Button("Process with no scrolling", variant="secondary")
    
    output = gr.Textbox(label="Output")
    
    btn1.click(fn=slow_function, inputs=text_input, outputs=output, scroll_on_click=True)
    btn2.click(fn=slow_function, inputs=text_input, outputs=output, scroll_to_output=True)
    btn3.click(fn=slow_function, inputs=text_input, outputs=output)

demo.launch()


## When to use scroll_on_click vs scroll_to_output

- **scroll_on_click**: Use when you want to immediately scroll to the output area as soon as the user clicks a button. This is useful for long forms where the output area is below the fold.

- **scroll_to_output**: Use when you want to scroll to the output area only after the function has completed and results are ready to display.
