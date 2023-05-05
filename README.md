# AI Text Evaluation

This repository contains a Python script that demonstrates how to make asynchronous calls to the OpenAI API. It takes a dataframe as input, processes the text values in the `text` column, and sends them to the API for processing. The resulting responses are stored in the `response` column of the output dataframe.

Warning: Asynchronous code behaves differently in standard Python and in Jupyter Notebook. This version is designed for standard Python.

## Setup

Before running the script, make sure to set your OpenAI API key and organization code in the following variables:

`openai.organization` = ""

`openai.api_key` = ""


Also, provide the path to your input data file by setting the `PATH` variable:

`PATH` = ""


## Customization

In the `process_dataframe(df)` function, you can optionally provide the following parameters to customize the evaluation process:

- `model`: The name of the AI model to use for evaluation
- `temperature`: Sampling temperature for generating text
- `max_tokens`: Maximum number of tokens to generate
- `top_p`: Top probability for selecting the next token

Furthermore, you can set the system prompt and the detection prompt in the variables:

`prompt_template` = ""

`system_prompt` = ""

## Usage

The script inputs a dataframe, evaluates all the text values in the `text` column, and assigns a score between 0 and 100 for each text value. The output is a dataframe containing the original text and the corresponding scores in the `score` column.
