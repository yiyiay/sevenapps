# Problem 1: Is using the Gemini 1.5 Flash that has 1 Million 
context size enough or Retrieval-Augmented Generation (RAG) is a
better approach?

- 1 million context size is quite large.
- RAG is a different technique.
- Increased context size is more similar to a system which is on steroids
- RAG is a technique which provides relatively improved results under same conditions when compared to sending whole data.
- That being said, RAG is chunking and tagging the data, which may be seen as a efficiency booster.


# Problem 2: Having 1 Million context size is great but output
tokens are limited to 8196, how would you queries that has more
than 8196 tokens?

- Piping chunks of data may both for read and write may be seen as more output than 8196.
- Responses might be streamlined to increase inflow of responses.

 # Problem 3: Writing unit tests are great for ensuring the app works
just fine, but how would you evaluate the performance of the Large
Language Model?

- Evaluating anything is quite hard.
- Evaluating LLMs is quite hard too.
- In text books there are two main approaches:
-- Automated Evaluation
--- Calculated scores of evaluation point
--- BERT, ROUGE, BLUE are some of them.

-- Human Evaluation
--- Response evaluations
--- Consistency evaluations
--- Correctness evaluations

- Benchmark datasets specific to the use case to compare LLMs.
- Token usage metrics might be used to compare LLMs.