# AutoLabel_GPT

一个使用基于 GPT 模型的接口自动化数据标注的项目。支持使用多个 API 密钥来组成 API 池, 允许并发访问 API，提高效率并减少触及速率限制的风险。
通过循环使用提供的 API 密钥，该工具可以同时处理更大量的请求，使数据标注过程更快速。
该项目可以作为数据处理工具包拿来使用

## 配置

### `config.json` 格式

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

## 使用方法

### 示例用法
1. **创建 `config.json`**：
   创建一个包含必要配置详情的 `config.json` 文件, 或者直接通过参数字典构造ApiConfig实例

2. **运行脚本**：
   使用提供的脚本为一组提示生成响应。

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

