# import sys
# import dill
# sys.path.append("C:/Users/shymk/anaconda3/envs/llms/Lib/site-packages")
# from langchain.llms import LlamaCpp
# from langchain import PromptTemplate, LLMChain
# from langchain.callbacks.manager import CallbackManager
# from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
# import pyttsx3
# # def main():

# def request():
#     if len(sys.argv) > 1:
#         prompt = sys.argv[1]
#     else:
#         prompt = "Default prompt value if not provided from C++"

#     MODEL_PATH = "/Users/shymk/Downloads/llama-2-7b-chat.Q5_K_M.gguf"


#     def load_model():
#         callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

#         Llama_model = LlamaCpp(
#             model_path=MODEL_PATH,
#             temperature=0.5,
#             max_tokens=30,
#             top_p=1,
#             n_gpu_layers=9,
#             n_batch=512,
#             n_ctx=1024,
#             f16_kv=True,
#             callback_manager=callback_manager,
#             verbose=True
#         )

#         return Llama_model

#     llm = load_model()
#     model_prompt: str = f"""
#     Speak from the side of Second person and answer the First peson's question.
#     First person: Hi are you a local?
#     Second person: Yes I am.
#     First person: {prompt}
#     """

#     result = llm(model_prompt)



#     # Write the result to a file
#     result = result.replace('\n', ' ')
#     with open("C:/Users/shymk/Documents/vsc prog/llama_langchain_locally/result.txt", "w") as f:
#         f.write(result)

#     model_prompt: str = f"""
#     Speak from the side of Second person and answer the First peson's question.
#     First person: Hi are you a local?
#     Second person: Yes I am.
#     First person: What year it is now?
#     """

#     result = llm(model_prompt)



#     # Write the result to a file
#     result = result.replace('\n', ' ')
#     with open("C:/Users/shymk/Documents/vsc prog/llama_langchain_locally/result.txt", "w") as f:
#         f.write(result)

# if __name__ == "__main__":
#     # If you run this script directly, call the function
#     request()

#     # Your Python logic here
    


# # res = request("How can I get to city center?")
#     # engine = pyttsx3.init()
#     # rate = engine.getProperty('rate')   # getting details of current speaking rate
#     # voices = engine.getProperty('voices')       #getting details of current voice
#     # engine.setProperty('voice', voices[1].id)  #changing index, changes voices. o for male
#     # engine.save_to_file(result, 'test.wav')
#     # engine.runAndWait()
#     # engine.stop()


# #     print(response)

# # if __name__ == "__main__":
# #     main()
# ------------------------------------------------------------------------------------------------
import os
import subprocess
import http.server
import socketserver
import json
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import pyttsx3

MODEL_PATH = "/Users/shymk/Downloads/tinyllama-2-1b-miniguanaco.Q5_K_M.gguf"



def load_model():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

    Llama_model = LlamaCpp(
        model_path=MODEL_PATH,
        temperature=0.5,
        max_tokens=100,
        top_p=1,
        n_gpu_layers=35,
        n_batch=128,
        n_ctx=256,
        f16_kv=True,
        callback_manager=callback_manager,
        verbose=True
    )

    return Llama_model

llm = load_model()

class LLMServer(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        try:
            # Parse the request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)

            # Extract the prompt from the request
            prompt = data.get('prompt', '')

            # Use the llm to generate a response
            print(prompt)
            print("----")
            system_message = "Imagine a situation when you meet the stranger on the street of New York, you are in your local area and he or she asks you a question which you should answer it. You know that it is possible to get to the city center by using a subway which will take 20 minutes or bus which will take 30 minutes."
            model_prompt: str = f"""
                ### Instruction: {system_message}
                ### Human: How can I get to the city center?
                ### Assistant:
            """
            response = llm(model_prompt)
            response = response.replace('\n', ' ')
            parts = response.split(':', 1)  # Split at the first occurrence of ':'

            if len(parts) > 1:
                response = parts[1].strip()  # Take the content after ':' and remove leading/trailing spaces
            with open("C:/Users/shymk/Downloads/piper_win_finalv3/piper_win_final/clipboard_temp.txt", "w") as f:
                f.write(response)
            # engine = pyttsx3.init()
            # rate = engine.getProperty('rate')   # getting details of current speaking rate
            # voices = engine.getProperty('voices')       #getting details of current voice
            # engine.setProperty('voice', voices[1].id)  #changing index, changes voices. o for male
            # engine.save_to_file(response, 'C:/Users/shymk/Documents/vsc prog/llama_langchain_locally/test.wav')
            # engine.runAndWait()
            # engine.stop()

            batch_file_path = 'C:/Users/shymk/Downloads/piper_win_finalv3/piper_win_final/clipboard_tts.bat'
            working_directory = 'C:/Users/shymk/Downloads/piper_win_finalv3/piper_win_final/'

            # Use subprocess to call the batch file
            try:
                subprocess.run(batch_file_path, shell=True, check=True, cwd=working_directory)
                print("Batch file executed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error executing batch file: {e}")

            # Send the response back to the client
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response_data = {'response': response}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))

        except json.JSONDecodeError:
            self.send_error(400, "Bad Request: Invalid JSON")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {e}")

if __name__ == '__main__':
    
    # Set up the server
    PORT = 8080
    handler = LLMServer
    httpd = socketserver.TCPServer(("", PORT), handler)

    print(f"Server running on port {PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
        httpd.server_close()



