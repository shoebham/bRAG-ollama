

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
		 const response = await fetch(`${BASE_URL}/v1/completion-stream`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message, model: "llama3" }),
                });
		// const data = await response
		const reader = response.body?.getReader();
		let accumulatedResponse = ''
		const readChunk = async () => {
			try {
            while (true) {
                const { value, done } = await reader.read();
                if (done) break;

                const chunkString = new TextDecoder().decode(value);
				console.log(chunkString);
				// Split the chunkString by new lines
				const lines = chunkString.split('\n');
				for (const line of lines) {
					if (line.startsWith('data: ')) {
						const jsonString = line.slice(6); // Remove 'data: ' prefix
						const jsonData = JSON.parse(jsonString);
						accumulatedResponse += jsonData.content;
						
						// Update the last message in the messages array
						messages[messages.length - 1].content = accumulatedResponse;
						messages = messages; // Trigger Svelte reactivity
					}
				}
            }
			} catch (error) {
				console.error('Error reading stream:', error);
			}
		}
		// readChunk();
		// console.log(data);
		return readChunk();
	}
	async function handleKeyDown(e){
		if (e.key == "Enter" && e.target.value) {
			e.preventDefault();
			const userMessage = e.target.value;
			e.target.value = "";
			messages = [...messages, { author: 'user', content: userMessage }];
			
			// Add an initial empty message for the system response
			messages = [...messages, { author: 'system', content: '' }];
			
			await sendMessage(userMessage);
		}
	}
</script>
<div class="container">
	<div class = "chat">
		<div class="chats" bind:this={div}>
			{#each messages as message}
				<article class={message.author}>
					<span>{@html marked(message.content)}	</span>
				</article>
			{/each}
		</div>

		<textarea placeholder="Enter your message" class ="chatbox chatbox-input" on:keydown={handleKeyDown} bind:value={currentMessage}/>
		
	</div>

</div>
<style>
	.container {
		display: grid;
		place-items: center;
		height: 100%;
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
		box-shadow:-5px -1px 4px 0px #151515;
		border-radius: 25px;
		position:relative;
		bottom: 0;
	}

	textarea.chatbox-input{
    	background-color: rgb(56, 56, 56);
		font-size: 19px;
		margin-left:75px;
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
