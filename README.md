# AutoLabel-GPT

使用 GPT 模型的接口完成自动化数据标注。

支持使用**多个 API 密钥**来组成 API 池, 允许**并发访问** API，提高效率并减少触及速率限制的风险。循环使用提供的 API 密钥，该工具可以同时处理更大量的请求，使数据标注过程更快速。

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

### 安装依赖
```
pip install requests
```

### 示例用法
1. **创建 `config.json`**：
   创建一个包含必要配置详情的 `config.json` 文件, 或者直接通过参数字典构造ApiConfig实例

2. **运行脚本**：
   使用提供的脚本为一组提示生成响应。

```python
if __name__ == "__main__":
    api_config = ApiConfig.from_json_file("./config.json")
    system_prompt = "You are a helpful assistant."

    prompts = [
        "What is the capital of France?",
        "Explain the theory of relativity.",
        "How does quantum computing work?",
        "Hi, say this is a test."
    ]

    for prompt, response in process_prompts_with_retries(api_config, prompts, system_prompt=system_prompt):
        response = response.strip().replace("\n", "")
        print(f"Prompt: {prompt}\nResponse: {response}\n")
```

