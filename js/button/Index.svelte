<script context="module" lang="ts">
	export { default as BaseButton } from "./shared/Button.svelte";
</script>

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { type FileData } from "@gradio/client";

	import Button from "./shared/Button.svelte";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: string | null;
	export let variant: "primary" | "secondary" | "stop" = "secondary";
	export let interactive: boolean;
	export let size: "sm" | "lg" = "lg";
	export let scale: number | null = null;
	export let icon: FileData | null = null;
	export let link: string | null = null;
	export let min_width: number | undefined = undefined;
	export let scroll_on_click: boolean = false;
	export let gradio: Gradio<{
		click: never;
	}>;
	
	// Function to handle scrolling to output
	function handleClick() {
			gradio.dispatch("click");
    
			if (scroll_on_click) {
					// Need to find the output components and scroll to them
					// This is similar to what happens on completion but triggered immediately
					const outputBlocks = document.querySelectorAll('.output-html, .output-markdown, .output-image, .output-video, .output-audio, .gradio-container > div > div > div.output');
        
					if (outputBlocks.length > 0) {
							setTimeout(() => {
									outputBlocks[0].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
							}, 10);
					}
			}
	}
</script>

<Button
	{value}
	{variant}
	{elem_id}
	{elem_classes}
	{size}
	{scale}
	{link}
	{icon}
	{min_width}
	{visible}
	disabled={!interactive}
	on:click={handleClick}
>
	{value ?? ""}
</Button>
