<script>

</script>

<svelte:head>
	<title>Chat Bot</title>
	<meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
	<div class = "chat">
		<div class="chats">
			<div class="user-chat">
				
			</div>	
			<div class="bot-chat">
			</div>
		</div>
		<div class="chatbox">
			<textarea placeholder="Enter your message" class ="chatbox-input"/>
		</div>
		
	</div>

</section>
<style>
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
	}
	.chatbox{
		width: 98%;
		height: 7vh;
		border: 1px solid #1818188c;
		box-shadow:-5px -1px 4px 0px #151515;
		border-radius: 25px;
		position: absolute;
		bottom: 0;
		margin:8px;
	}

	textarea.chatbox-input{
    	background-color: rgb(56, 56, 56);
		width: 90%;
		height: 70%;
		font-size: 19px;
		margin-left:50px;
		margin-top:8px;
		margin-bottom: 50px;
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

</style>
