import concurrent
import itertools
import json
import os
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
from typing import Sequence, List, Iterator, Tuple, Optional, Any, Callable, TypeVar

import requests


def assert_input_type(*types):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) != len(types):
                raise TypeError(f"{func.__name__} expects {len(types)} arguments, but got {len(args)}")
            for a, t in zip(args, types):
                if not isinstance(a, t):
                    raise TypeError(f"Argument {a} does not match expected type {t}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


class _BaseApiConfig:
    def __repr__(self):
        return json.dumps(self.__dict__)

    def dump_to_json(self, json_path="./config.json"):
        if os.path.exists(json_path):  # avoid overwrite
            raise FileExistsError
        with open(json_path, 'w') as f:
            json.dump(self.__dict__, f, indent=4)
        print(f"Configuration dumped to {json_path}")

    @staticmethod
    def from_json_file(json_file) -> 'ApiConfig':
        with open(json_file, 'r') as f:
            data = json.load(f)
        return ApiConfig(**data)


@assert_input_type(str, str, str, int, int, float)
def _make_data(model_type, prompt, system_prompt, max_tokens, n, temperature):
    data = {
        'model': model_type,
        'messages': [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        'max_tokens': max_tokens,
        'n': n,
        'stop': None,
        'temperature': temperature
    }
    return data


def _make_header(api_key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    return headers


class ApiConfig(_BaseApiConfig):
    def __init__(self, *, model_type: str, api_url: str, api_keys: Sequence[str]):
        self.model_type = model_type
        self.api_url = api_url
        self.api_keys = api_keys


def generate_response(api_key, model_type, api_url, prompt: Any, system_prompt="You are a helpful assistant.",
                      max_tokens=150, temperature=0.7, n=1, key=None):
    prompt: str = prompt if key is None else key(prompt)
    headers = _make_header(api_key)
    data = _make_data(model_type, prompt, system_prompt, max_tokens, n, temperature)
    response = requests.post(api_url, headers=headers, json=data)
    assert response.status_code == 200, f"Error: {response.status_code} - {response.text}"
    result = response.json()
    time.sleep(0.5)
    return result['choices'][0]['message']['content'].strip()


def process_prompts(api_config: ApiConfig, prompts: List[Any], **kwargs) -> Iterator[Tuple[str, Optional[str]]]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(api_config.api_keys)) as executor:
        # Use itertools.cycle to cycle through api_keys
        api_key_cycle = itertools.cycle(api_config.api_keys)
        future_to_prompt = {
            executor.submit(partial(generate_response, next(api_key_cycle), api_config.model_type, api_config.api_url,
                                    prompt, **kwargs)): prompt
            for prompt in prompts
        }

        for future in concurrent.futures.as_completed(future_to_prompt):
            prompt = future_to_prompt[future]
            try:
                result = future.result()
                yield prompt, result
            except Exception as exc:
                print(f"Prompt {prompt} generated an exception: {exc}")
                yield prompt, None


PromptType = TypeVar('PromptType')  # Define a type variable


def process_prompts_with_retries(api_config: ApiConfig, prompts: List[PromptType], max_retries=3, **kwargs) -> Iterator[
    Tuple[PromptType, Optional[str]]]:
    prompts_copy = prompts.copy()
    retries = defaultdict(int)
    while len(prompts_copy):
        input_prompts = prompts_copy.copy()
        prompts_copy.clear()
        for prompt, response in process_prompts(api_config, input_prompts, **kwargs):  # process failed prompts
            if response is None:
                retries[prompt] += 1
                if retries[prompt] < max_retries:
                    prompts_copy.append(prompt)
                    print(f"prompt {prompt} tried = {retries[prompt]}")
                else:
                    print(f"prompt {prompt} reached max retries {max_retries}")
            else:
                yield prompt, response


if __name__ == "__main__":
    api_config = ApiConfig.from_json_file("./config.json")
    prompts = [
        "What is the capital of France?",
        "Explain the theory of relativity.",
        "How does quantum computing work?",
        "Hi, say this is a test."
    ]

    for prompt, response in process_prompts_with_retries(api_config, prompts):
        response = response.strip().replace("\n", "")
        print(f"Prompt: {prompt}\nResponse: {response}\n")

