import subprocess
import sys
import dill
sys.path.append("C:/Users/shymk/anaconda3/envs/llms/Lib/site-packages")
from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pyttsx3
# def main():

def request():
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        prompt = "what year it is now?"

    MODEL_PATH = "/Users/shymk/Downloads/llama-2-7b-chat.Q5_K_M.gguf"


    def load_model():
        callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

        Llama_model = LlamaCpp(
            model_path=MODEL_PATH,
            temperature=0.5,
            max_tokens=50,
            top_p=1,
            n_gpu_layers=35,
            n_batch=128,
            n_ctx=128,
            # f16_kv=True,
            callback_manager=callback_manager,
            verbose=True
        )

        return Llama_model

    llm = load_model()
    model_prompt: str = f"""
    Speak from the side of Second person and answer the First peson's question.
    First person: Hi are you a local?
    Second person: Yes I am.
    First person: {prompt}
    """

    result = llm(model_prompt)



    # Write the result to a file
    result = result.replace('\n', ' ')
    with open("C:/Users/shymk/Documents/vsc prog/llama_langchain_locally/result.txt", "w") as f:
        f.write(result)

    batch_file_path = 'C:/Users/shymk/Downloads/piper_win_finalv3/piper_win_final/clipboard_tts.bat'
    working_directory = 'C:/Users/shymk/Downloads/piper_win_finalv3/piper_win_final/'

    # Use subprocess to call the batch file
    try:
        subprocess.run(batch_file_path, shell=True, check=True, cwd=working_directory)
        print("Batch file executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing batch file: {e}")


if __name__ == "__main__":
    # If you run this script directly, call the function
    request()

    # Your Python logic here
    


# res = request("How can I get to city center?")
    # engine = pyttsx3.init()
    # rate = engine.getProperty('rate')   # getting details of current speaking rate
    # voices = engine.getProperty('voices')       #getting details of current voice
    # engine.setProperty('voice', voices[1].id)  #changing index, changes voices. o for male
    # engine.save_to_file(result, 'test.wav')
    # engine.runAndWait()
    # engine.stop()


#     print(response)

# if __name__ == "__main__":
#     main()

