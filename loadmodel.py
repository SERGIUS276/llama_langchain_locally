import sys
import dill
sys.path.append("C:/Users/shymk/anaconda3/envs/llms/Lib/site-packages")
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

MODEL_PATH = "/Users/shymk/Downloads/llama-2-7b-chat.Q5_K_M.gguf"

callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

llm = LlamaCpp(
    model_path=MODEL_PATH,
    temperature=0.5,
    max_tokens=30,
    top_p=1,
    n_gpu_layers=35,
    n_batch=512,
    n_ctx=1024,
    f16_kv=True,
    callback_manager=callback_manager,
    verbose=True
)



# Save the llm instance using dill
with open("llm_instance.pkl", "wb") as file:
    dill.dump(llm, file)
