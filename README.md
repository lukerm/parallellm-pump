# Pump Your LLMs In Parallel

This code base allows you to configure and run prompts to multiple LLMs in parallel, via their APIs. You be the judge
of which provider returns the best result to your prompt (use `pump`). Or, you can ask the LLMs which one is the best
(user `prefer`).

## Technical Details

- It makes use of `asyncio` to make sure you're only waiting for the slowest model to finish.
- Requires configuration of API keys for each provider you want to use.
- Thin set of dependencies (mostly the vendor libraries for calling the LLMs).
- Very simple interface to run the pump. 

## Installation & Setup

Dependencies: 

```bash
git clone git@github.com:lukerm/parallellm-pump.git
cd parallellm-pump
pip install -r requirements.txt
```

Configuration:

Make a JSON file to store your API keys. The format is:

```bash
mkdir -p config/secret
cp config/api-keys-template.json config/secret/api-keys.json
# then edit the file to include your personal API keys
```

_Please never commit your API keys to the repository!_

## Usage

The vanilla usage is simply to run `pump.py` to prompt multiple LLMs in parallel:

```bash
$ python -m src.pump --prompt "What is the significance of the number 42? Explain in 50 words max." --providers chatgpt claude
2025-01-28 15:57:17,903 INFO:Running the pump for the following providers: openai, anthropic
2025-01-28 15:57:19,884 INFO:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
2025-01-28 15:57:19,927 INFO:OpenAI response time: 1.96s
2025-01-28 15:57:20,103 INFO:HTTP Request: POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
2025-01-28 15:57:20,134 INFO:Anthropic response time: 2.13s
2025-01-28 15:57:20,135 INFO:Total run time: 2.23s
2025-01-28 15:57:20,135 INFO:Results

chatgpt
_______

The number 42 is famously known as the 'Answer to the Ultimate Question of Life, the Universe, and Everything' in Douglas Adams\' science fiction series, "The Hitchhiker's Guide to the Galaxy." Its absurdity and humor symbolize the complexity of existence, prompting philosophical reflection on the search for meaning.

claude
______

42 is famously the "Answer to the Ultimate Question of Life, the Universe, and Everything" in Douglas Adams\' "The Hitchhiker's Guide to the Galaxy." It\'s become a popular cultural reference symbolizing the search for meaning, though in the book, the answer is deliberately meaningless.

```

Note that the total run time is reported - you can see that it took 2.23s to get responses from both models and
process them, which is only a little longer than the slower of the two responses (Claude). This is a big benefit of using 
asyncio. 

A fun extension is to use the `prefer` command to ask the models which one they think is the best:

```bash
$ python -m src.prefer --prompt "What is the significance of the number 42? Explain in 50 words max." --providers chatgpt claude
#... truncated output
2025-01-28 16:04:11,092 INFO:Total run time: 8.23s
2025-01-28 16:04:11,092 INFO:Final preference results:

chatgpt
_______

1. Response 2 (claude)  
2. Response 1 (chatgpt)  

- **Factuality**: Both responses accurately reference Douglas Adams\' work, but Response 2 (claude) includes the cultural impact and significance of cosmic irony, providing a broader context.
- **Writing Style**: Response 2 (claude) is more concise and clear, adhering to the 50-word limit effectively without any additional explanation, whereas Response 1 (chatgpt) adds some unnecessary detail.
- **Clarity**: Response 2 (claude) presents the information in a straightforward manner, making it easier to understand the significance of the number 42 quickly.

claude
______

Rankings:
1. Response 2 (claude)
2. Response 1 (chatgpt)

Reasoning:
* Response 2 (claude) is more concise while maintaining all essential information
* Response 2 (claude) includes the clever additional detail about the question being unknown, which is an important part of the story\'s irony
* Response 1 (chatgpt) slightly exceeds the 50-word limit given in the prompt
* Both responses are factually accurate, but Response 2 (claude) delivers the information more efficiently and elegantly
* Response 2 (claude) better captures the essence of the reference while staying within the word limit constraint

The difference between the responses is subtle, but Response 2 (claude)\'s adherence to the word limit while including a key detail about the unknown question makes it the superior answer.
```

The same principle of running in parallel applies here, too, except that we proceed in two stages: first the original prompt,
then second collect those responses to form a new prompt and ask all models which model they preferred (anonymously).

In this example, both Claude _and_ ChatGPT prefer Claude's response. Sorry OpenAI. Ironically, Claude's response is based
somewhat on a miscalculation of the word count - ChatGPT does _not_ exceed the 50-word limit. It does use 42 words in
its response though 🤯

## Contributing

Contributions are welcome! Please open an issue or PR if you have any suggestions or improvements. There are many ideas 
to improve this codebase, such as:

- Integrating more LLM providers
- Configuration for using different models from the same provider (e.g.GPT-4o vs GPT-o1) 
- Creating a python module and/or command-line tool
- Support for prompt files and response files (input/output)
- Support for Docker
- More unit testing
