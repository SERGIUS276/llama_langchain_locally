import sys
sys.path.append("C:/Users/shymk/anaconda3/envs/llms/Lib/site-packages")

import pyttsx3




def request(prompt):
    # if len(sys.argv) > 1:
    #     prompt = sys.argv[1]
    # else:
    #     prompt = "Default prompt value if not provided from C++"


    engine = pyttsx3.init()
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    print (rate) 
    engine.setProperty('rate', 200) 
    voices = engine.getProperty('voices')
    for voice in voices:
        print("ID:", voice.id, "Name:", voice.name, "Lang:", voice.languages)
    
    engine.setProperty('voice', voices[4].id)  #changing index, changes voices. o for male
    engine.save_to_file(prompt, 'C:/Users/shymk/Documents/vsc prog/llama_langchain_locally/test.wav')
    engine.runAndWait()
    engine.stop()
    return "result"

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: your_script.py <text_to_speak>")
    # else:
    text = "I'm here to help and answer all of your questions"
    request(text)
# if __name__ == "__main__":
#     main()

@echo off
setlocal enabledelayedexpansion

SET "_sox=sox.exe"
SET "prev_size=0"
SET "temp_file=clipboard_temp.txt"

:monitor
REM Run the VBScript to update the temporary file with current clipboard content
cscript //nologo getclipboard.vbs >NUL 2>&1

REM Get the current size of the temporary file to detect changes
FOR %%F IN (!temp_file!) DO SET "current_size=%%~zF"

REM Check if the file size has changed
IF NOT "!current_size!"=="!prev_size!" (
    REM Clipboard content has changed, update previous size
    SET "prev_size=!current_size!"
    
    REM Wait a short time to ensure the clipboard data is stable
    TIMEOUT /T 1 /NOBREAK > NUL
    
    REM Use Piper TTS to convert the text from the temporary file to speech and suppress its output
    piper --model en_GB-jenny_dioco-medium.onnx --output_file test.wav  < !temp_file! | "%_sox%" -t raw -b 16 -e signed-integer -r 22050 -c 1 - -t waveaudio pad 0 0.010 >NUL 2>&1
    
    IF %ERRORLEVEL% NEQ 0 (
        ECHO Piper TTS conversion failed
        GOTO monitor
    )
)

REM Wait for a short time before checking again
TIMEOUT /T 1 /NOBREAK > NUL

GOTO monitor