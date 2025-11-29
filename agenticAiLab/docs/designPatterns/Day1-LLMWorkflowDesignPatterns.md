LLM WORKFLOW DESIGN PATTERNS

1. # PROMPT CHAINING
   its just a chaining of LLMS that finally gives an output. There can be a code block in between but its a simple chaining
   Prompt chaining is simply a sequential pipeline of multiple LLM calls.
   A code block can exist between steps, but the flow is strictly linear.

```
input -> llm1 -> llm2 -> (code block) -> llm3 -> output
```

2. ROUTING
   for a given input , there is a LLM router that routes the action or input to various other specialized llms. The LLM router has the autonomy of selecting which LLM should perform the tasks . SO only a single LLM is selected for its specialized subtasks.

```
                    -> SPECIALIZED LLM 1
input -> LLMROUTER  -> SPECIALIZED LLM 2 -> output
                    -> SPECIALIZED LLM 3
```

3. # PARALLELIZATION
   This will have a code block that sperates the tasks into multiple sections and feeds it to multiple LLMS that work parallely. These LLMS then give their outputs to another code block that stitches all the LLM outputs into single result and spits it out - This is concurrently running the LLMS

```
                                -> LLM1 ->
input -> CodeBlock/Co-ordinator -> LLM2 -> -> CodeBlock/Aggregator -> output
                                -> LLM3 ->
```

4. # ORCHESTRATOR-WORKER
   This is similar to the PARALLELIZATION workflow pattern but instaed of the codeblock there is a LLM that decides what subtasks should go to which LLM. Later there is a LLM that stitches together all the results from the LLMS and gives an output
   Complex tasks are broken down dynamically and combined

```
                          -> LLM1 ->
input -> LLM/Orchestrator -> LLM2 -> -> LLM/synthesizer -> output
                          -> LLM3 ->
```

5. # EVALUATOR - OPTIMIZER
   This is basically a feedback loop . An iput comes in, the LLM takes it and processes it. Then the LLMS output is given to a different LLM for feedback and evaluate the results. It can either take it as correct/accepts and gives the output or sends it back with a rejection and a reason to the earlier LLM .

```
            solution
              ->
input -> LLMl     LLM2 -> output
              <-
    Rejected with feedback
```
