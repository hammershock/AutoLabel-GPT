# AutoLabel_GPT README

## Overview
AutoLabel_GPT is a project designed to automate the process of data annotation using GPT-based models. This tool leverages the OpenAI API to generate responses for a given set of prompts, facilitating efficient and scalable data labeling.

## Configuration

### `config.json` Format
To use AutoLabel_GPT, you need to create a `config.json` file that includes the necessary configuration details for the API. Below is an example of a `config.json` file:

```json
{
    "model_type": "gpt-3.5-turbo",
    "api_url": "https://api.openai.com/v1/chat/completions",
    "api_keys": [
        "YOUR_API_KEY_1",
        "YOUR_API_KEY_2"
    ]
}
```

## Usage

### Example Usage
1. **Create `config.json`**:
   Create a `config.json` file with the necessary configuration details.

2. **Run the Script**:
   Use the provided script to generate responses for a list of prompts.

```python
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
```

## Key Features

### Concurrent API Access with Multiple API Keys
AutoLabel_GPT supports using multiple API keys to form an API pool. This allows for concurrent API access, improving efficiency and reducing the risk of hitting rate limits. By cycling through the provided API keys, the tool can handle a higher volume of requests simultaneously, making the data annotation process faster and more robust. 

By following these steps and using the provided functions and classes, you can effectively automate the data annotation process using GPT-based models.