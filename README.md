# invoke-llava
A wafer thin wrapper for [llama-cpp-python](https://github.com/abetlen/llama-cpp-python) primarily for my own convenience, and mostly in the context of invocation from ComfyUI. Interrogation in a single shot executable ensures that VRAM leaks don't pile up and eventually bring down the server process.

## arguments
Standard LLM related parameters such as gpu layers, token limit, context length, temperature, and seed can be specified using `--gpu_layers`, `--max_tokens`, `--n_ctx`, `--temp`, and `--seed` respectively.

The models should be specified using `--model-path` (for the main LLAVA model) and `--clip-model-path` (for the mmproj model). You need to specify both. There are defaults, but they are only useful to me.

You can provide a json encoded system message and prompt (including things like encoded images) on the command line, or specify `--stdin` to read the same from standard input. If you specify `--image-file`, your command line argument will be interpreted as a plain text prompt to be matched with the image.

## notes
llama.cpp dumps large amounts of debugging information to stderr - you probably want to redirect that somewhere in most cases.

## examples
When run with no arguments, a default testing prompt is used asking for a room description for an adventure game.

`PS C:\Users\curious\Documents\GitHub\invoke-llava> python .\invoke_llava.py --model-path 'E:\VirtualBox VMs\comfy\ComfyUI\custom_nodes\ComfyUI-LLaVA-Captioner\models\llama\llava-v1.5-7b-Q4_K.gguf' --clip-model-path 'E:\VirtualBox VMs\comfy\ComfyUI\custom_nodes\ComfyUI-LLaVA-Captioner\models\llama\llava-v1.5-7b-mmproj-Q4_0.gguf' 2>$null`

> 🌟 As you step into the room, you are greeted by a vibrant and abstract mural on the wall, painted in shades of pink, blue, and yellow. The room is filled with colorful furniture, including a rainbow-colored couch and a chair with a matching floral pattern. Above the couch, a kaleidoscope of colors hangs on the wall, casting a mesmerizing pattern on the floor below. The room is decorated with various items, such as a collection of colorful vases, a set of abstract paintings, and a few colorful sculptures. The overall atmosphere is lively, energetic, and full of creativity.

Interrogating an [image](https://x.com/reactjpg/status/1478426524617428995):

`PS C:\Users\curious\Documents\GitHub\invoke-llava> python .\invoke_llava.py "Describe this image." --image-file C:\Users\curious\Downloads\20230420_213607.jpg 2>$null`

> The image is a comic strip featuring a man and a boy standing in front of a sign. The man is wearing a tie and appears to be a teacher, while the boy is dressed in a suit. They are engaged in a conversation, with the man pointing at the sign. The sign reads "Free School for Dumb Adults." The comic strip is likely a part of a newspaper or magazine.

Specifying an exchange using JSON (not done in PowerShell for [reasons](https://stackoverflow.com/questions/6714165/powershell-stripping-double-quotes-from-command-line-arguments)):

`(invoke-llava-gGRk7yZG) C:\Users\curious\Documents\GitHub\invoke-llava>python invoke_llava.py "[ { \"role\": \"system\", \"content\": \"You are an award-winning AI assistant.\" }, { \"role\": \"user\", \"content\": [ { \"type\": \"text\", \"text\": \"Please provide marketing copy for Stilk, an imaginary beverage made out of milk and molten steel.\" } ] } ]" 2>NUL`

> 🚀 Introducing Stilk: The Ultimate Beverage for Steel Enthusiasts! 🚀
> Unleash your inner metalhead with Stilk, the groundbreaking beverage made from the perfect blend of milk and molten steel! 🤘
> Experience a symphony of flavors as Stilk's rich, creamy milk harmoniously combines with the intense, robust notes of molten steel. 🎶
> Not only is Stilk a delicious, one-of-a-kind beverage, but it's also packed with incredible benefits! 💪
> 🌟 Enhance your energy levels with the natural electrolytes found in milk and the iron-boosting properties of molten steel! 🌟

