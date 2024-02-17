@echo off
set CMAKE_ARGS=-DLLAMA_CUBLAS=on
set FORCE_CMAKE=1

pip install --upgrade --force-reinstall llama-cpp-python --no-cache-dir