import argparse
import base64
import json
import random
import sys
import os
import contextlib
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Llava15ChatHandler

from pathlib import Path

default_messages = [
    {
        'role': 'system', 
        'content': ( 'You are an award-winning AI assistant that helps to create room and item descriptions for adventure games. '
                     'Your output will be placed directly into variables on virtual objects, so you must: '
                       'present only one description at a time,'
                       'not lead your descriptions with headers, greetings, bullets, list numbers, etc, or'
                       'include any other content that cannot be read directly as a description. '
                     'This is important to avoid breaking immersion from our users. Be concise.' )
    }, 
    {
        'role': 'user', 
        'content': [
            {
                'type': 'text', 
                'text': ( 'Using advanced natural language generation, create a vivid and atmospheric description of an indoor or outdoor scene for a role-playing game. '
                          'The game has a colourful, abstract theme. '
                          'Your description should be two to three sentences long, rich in visual sensory details, and include the objects, decorations, and colors that can be seen in the scene. '
                          'You shouldn\'t describe aspects of the scene related to smell, taste, and hearing. '
                          'Focus on creating a specific mood and atmosphere without referencing characters or the game context, and aim for a variety of settings in your work.' )
            }]
    }
]

def makeImagePrompt(prompt, image_path):
    with open(image_path, 'rb') as image_file:
        encoded = base64.b64encode(image_file.read()).decode('utf-8')
    image_url = f'data:image/png;base64,{encoded}'
    image_parsing_messages = [
        {
            'role': 'system', 
            'content': 
                'You are an assistant who describes the content and composition of images. '
                'Describe only what you see in the image, not what you think the image is about. '
                'Be factual and literal. Do not use metaphors or similes. Be concise.'
        },
        {
            'role': 'user',
            'content': [
                {'type': 'image_url', 'image_url': image_url},
                {"type": "text", "text": prompt},
            ]
        }
    ]
    return image_parsing_messages

def getLLM(args):
    llm = Llama(
        model_path = str(args.model_path),
        chat_handler = Llava15ChatHandler(clip_model_path = str(args.clip_model_path)),
        n_gpu_layers = args.gpu_layers, 
        n_ctx = args.n_ctx,
        chat_format = "llava-1-5", 
        seed = args.seed,
        logits_all = True, 
        verbose = False
    )
    return llm

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('message', type=str, nargs='?')
    parser.add_argument('--gpu_layers', type=int, nargs='?', default=-1)
    parser.add_argument('--max_tokens', type=int, nargs='?', default=200)
    parser.add_argument('--n_ctx', type=int, nargs='?', default=2048)
    parser.add_argument('--seed', type=int, nargs='?', default=-1)
    parser.add_argument('--stdin', action='store_true', default=False)
    parser.add_argument('--image-file', type=Path, nargs='?'),
    parser.add_argument('--temp', type=float, nargs='?', default=0.3)
    parser.add_argument('--model-path', type=Path, default=Path('E:/VirtualBox VMs/comfy/ComfyUI/custom_nodes/ComfyUI-LLaVA-Captioner/models/llama/llava-v1.5-7b-Q4_K.gguf'), help = 'Path to the main LLAVA model.')
    parser.add_argument('--clip-model-path', type=Path, default=Path('E:/VirtualBox VMs/comfy/ComfyUI/custom_nodes/ComfyUI-LLaVA-Captioner/models/llama/llava-v1.5-7b-mmproj-Q4_0.gguf'), help = 'Path to the mmproj model.')
    args = parser.parse_args()
    
    if args.image_file:
        messages = makeImagePrompt(args.message, args.image_file)
    elif args.message:
        messages = json.loads(args.message)
    elif args.stdin:
        messages = json.loads(sys.stdin.read())
    else:
        messages = default_messages
    
    llm = getLLM(args)
    results = llm.create_chat_completion(
        max_tokens=args.max_tokens,
        messages=messages,
        temperature=args.temp
    )
    del(llm)
    result = random.choice(results['choices'])
    print(result['message']['content'])