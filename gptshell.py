import random, os

try:
    import openai
except ModuleNotFoundError:
    print("[*] install missing module: openai")
    os.system("pip3 install openai")
    import openai

openai_api_key_store = ""             # put SK here to avoid duplicated initialize 
openai_model_dict = {'a': "gpt-4", 'b': "gpt-3.5-turbo", 'c': "gpt-4-0314", 'd': "gpt-3.5-turbo-0301"}

class Chat:
    def __init__(self, openai_model, conversation_list=[]) -> None:
        # 初始化对话列表，可以加入一个key为system的字典，有助于形成更加个性化的回答
        # self.conversation_list = [{'role':'system','content':'你是一个非常友善的助手'}]
        self.conversation_list = []
        self.openai_model = openai_model 

    # print
    def show_conversation(self, msg_list):
        for msg in msg_list:
            if msg['role'] == 'user':
                print(f"\U0001f47b: {msg['content']}\n")
            else:
                print(f"\U0001f47D: {msg['content']}\n")

    def clear_context(self,):
        self.conversation_list = []

    # prompt
    def ask(self, prompt):
        self.conversation_list.append({"role":"user", "content":prompt})
        response = openai.ChatCompletion.create(model=self.openai_model, messages=self.conversation_list)
        answer = response.choices[0].message['content']
        # build context
        self.conversation_list.append({"role":"assistant", "content":answer})
        self.show_conversation(self.conversation_list)

class Image:
    def __init__(self, number=1, size="1024x1024") -> None:
        self.number = number
        self.size = size

    def ask(self, prompt):
        image = openai.Image.create(
            prompt = prompt,
            n=self.number,
            size=self.size,
            response_format='url'
        )
        print(image)

def banner():
	padding = '  '
	S = [[' ','┌','─','┐'],
	     [' ','└','─','┐'],
	     [' ','└','─','┘']]
	H = [[' ','┬',' ','┬'],
	     [' ','├','─','┤'],
	     [' ','┴',' ','┴']]
	E = [[' ','┌','─','┐'],
	     [' ','├','┤',' '],
	     [' ','└','─','┘']]
	L = [[' ','┬',' ',' '],
	     [' ','│',' ',' '],
	     [' ','┴','─','┘']]
	G = [[' ','┌','─','┐'],
	     [' ','│',' ','┬'],
	     [' ','└','─','┘']]
	P = [[' ','┌','─','┐'],
	     [' ','│','─','┘'],
	     [' ','┴',' ',' ']]
	T = [[' ','┌','─','┐'],
	     [' ',' ','│',' '],
	     [' ',' ','┴',' ']]
	
	banner = [G,P,T,S,H,E,L,L]
	final = []
	print('\r')
	init_color = random.randint(10,40)
	txt_color = init_color
	cl = 0

	for charset in range(0, 3):
		for pos in range(0, len(banner)):
			for i in range(0, len(banner[pos][charset])):
				clr = f'\033[38;5;{txt_color}m'
				char = f'{clr}{banner[pos][charset][i]}'
				final.append(char)
				cl += 1
				txt_color = txt_color + 36 if cl <= 3 else txt_color

			cl = 0

			txt_color = init_color
		init_color += 31

		if charset < 2: final.append('\n   ')

	print(f"   {''.join(final)}")
	print(f'{padding}                           by OpenGVLab\n')


if __name__=="__main__":
    banner()
    if not openai_api_key_store:
        openai.api_key = input("Please Input Your API Key -> ")
    else:
        print("Successfully Loaded Stored API Key!\n")
        openai.api_key = openai_api_key_store
    print("Please choose your interactive type ->\na. Chat\nb. Image\n")
    model_type = input("Your Choice -> ")
    if model_type == 'a':
        print("Please choose your GPT version (input a-d) ->\na. GPT4\nb. gpt-3.5-turbo\nc. GPT4-0314\nd. gpt-3.5-turbo-0301\n")
        model_select = input("Your Choice -> ")
        try:
            openai_model = openai_model_dict[model_select]
            print(f"Initialized Model Version {openai_model}")
            print("="*150)
            print("Warning! Input \"clear\" to clear chat history. Remeber to use this command to save money if contextual information are currently unnecessary.")
            print("="*150)
        except:
            raise NotImplementedError(f"Unsupported Choice {model_select}!")
        bot = Chat(openai_model) 
        while True:
            interact = input(f"[{openai_model}]╼> ")
            if interact == "exit":
                exit()
            elif interact == "clear":
                print(f"Chat history successfully cleared!")
                bot.clear_context()
            else:
                bot.ask(interact)
    else:
        bot = Image()
        print("Successfully Initialize DALL-E!")
        while True:
            interact = input("[DALL-E]╼> ")
            if interact == "exit":
                exit()
            else:
                bot.ask(interact)