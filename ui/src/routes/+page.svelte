

<svelte:head>
	<title>Chat Bot</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<script>
	import {
		beforeUpdate,
		afterUpdate
	} from 'svelte';
	import { marked } from 'marked';

	let div;
	let autoscoll = false;
	const pause = (ms) => new Promise((fulfil) => setTimeout(fulfil, ms));
	const typing = { author: 'system', content: '...' };
	let pdfFile = null;
	let pdfPreviewUrl = null;

	beforeUpdate(() => {
		if(div){
			const scrollableDistance = div.scrollHeight - div.offsetHeight;
			autoscoll = div.scrollTop > scrollableDistance - 20;
		}
		// determine whether we should auto-scroll
		// once the DOM is updated...
	});

	afterUpdate(() => {
		if(autoscoll){
			div.scrollTo(0,div.scrollHeight)
		}
		// ...the DOM is now in sync with the data
	});

	const BASE_URL="http://localhost:8000"
	let messages = [];
	let currentMessage = "";
	async function sendMessage(message){
		const formData = new FormData();
		formData.append('model',"llama3");
		formData.append('message', message);
		if (pdfFile) {
			formData.append('pdf_file', pdfFile);
		}
		const response = await fetch(`${BASE_URL}/v1/qa-create-pdf-stream`, {
			method: 'POST',
			body: formData
		});
		const reader = response.body?.getReader();
		let accumulatedResponse = ''
		const readChunk = async () => {
			try {
				while (true) {
					const { value, done } = await reader.read();
					if (done) break;

					const chunkString = new TextDecoder().decode(value);
					console.log(chunkString);
					const lines = chunkString.split('\n');
					for (const line of lines) {
						if (line.startsWith('data: ')) {
							const jsonString = line.slice(6);
							const jsonData = JSON.parse(jsonString);
							accumulatedResponse += jsonData.content;
							
							messages[messages.length - 1].content = accumulatedResponse;
							messages = messages;
						}
					}
				}
			} catch (error) {
				console.error('Error reading stream:', error);
			}
		}
		pdfFile = null;
		pdfPreviewUrl = null;
		return readChunk();
	}
	async function handleKeyDown(e){
		if (e.key == "Enter" && e.target.value) {
			e.preventDefault();
			const userMessage = e.target.value;
			e.target.value = "";
			messages = [...messages, { author: 'user', content: userMessage }];
			
			messages = [...messages, { author: 'system', content: '' }];
			
			await sendMessage(userMessage);
		}
	}
	function openFile() {
		let input = document.createElement('input');
		input.type = 'file';
		input.accept = 'application/pdf';
		input.onchange = _ => {
			let files = Array.from(input.files);
			if (files.length > 0) {
				pdfFile = files[0];
				pdfPreviewUrl = URL.createObjectURL(pdfFile);
			}
		};
		input.click();
	}
</script>
<div class="container">
	<div class="chat">
		<div class="chats" bind:this={div}>
			{#each messages as message}
				<article class={message.author}>
					<span>{@html marked(message.content)}</span>
				</article>
			{/each}
		</div>
		
		<div class="chat-input">
			<button class="upload-btn" on:click={openFile}>Upload</button>
			{#if pdfPreviewUrl}
				<embed src={pdfPreviewUrl} width="250" height="200" />
			{/if}
			<textarea placeholder="Enter your message" class="chatbox chatbox-input" on:keydown={handleKeyDown} bind:value={currentMessage}></textarea>
		</div>
	</div>
</div>
<style>
	.container {
		display: grid;
		place-items: center;
		height: 100%;
	}
	.chat-input{
		display: flex;
		flex-direction: row;
		align-items: center;
	}
	.upload-btn{
		width: 5%;
		height: 50%;
		border: none;
		border-radius: 30px;
		padding:10px;
		background-color: rgb(56, 56, 56);
		color: rgb(248, 248, 248);
		box-shadow:-1px 0px 4px 0px #ffffff78;
		margin-left:20px;
		margin-bottom:20px;
	}
	.upload-btn:hover{
		cursor: pointer;
	}
	.chat{
		background-color: rgb(56, 56, 56);
		box-shadow:inset -9px 1px 8px 4px #151515;
		height: 95vh;
		width: 95vw;
		border-radius: 20px;
		margin:auto;
		margin-top:20px;
		padding:auto;
		position: relative;
		display: flex;
		flex-direction: column;
	}
	.chats{
		height: 0;
		flex: 1 1 auto;
		padding: 0 1em;
		overflow-y: auto;
		scroll-behavior: smooth;
	}
	article {
		margin: 0 0 0.5em 0;
	}

	.user {
		text-align: right;
	}
	.user span {
		background-color: #0074d9;
		color: white;
		border-radius: 1em 1em 0 1em;
		word-break: break-all;
	}

	span {
		padding: 0.5em 1em;
		display: inline-block;
	}
	.system span {
		background-color: #000000;
		color:white;
		border-radius: 1em 1em 1em 0;
	}
	
	.chatbox{
		width: 90%;
		height: 7vh;
		border: 1px solid #1818188c;
		box-shadow:-1px 0px 4px 0px #f9f9f9a5;
		border-radius: 25px;
		position:relative;
		bottom: 0;
	}

	textarea.chatbox-input{
    	background-color: rgb(56, 56, 56);
		font-size: 19px;
		margin-left:20px;
		margin-bottom:25px;
		margin-right: 100px;
		border: none;
		border-radius: 25px;
		resize: none;
		padding-left:50px;
		box-sizing: border-box;
		padding-top: 10px;
		color: rgb(248, 248, 248);
	}
	textarea:focus{
		outline: none;
	}
	@media (prefers-reduced-motion) {
		.chat {
			scroll-behavior: auto;
		}
	}
</style>
