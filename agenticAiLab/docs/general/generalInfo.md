# **Difference bw system and user prompts**

System Prompt — "WHO the AI is and HOW it should behave"  
Purpose:  
Sets the rules, personality, constraints, and style for the assistant.
This is internal instruction to the AI.  
Think:  
System prompt = Operating System  
Ex :

```
    {
  "role": "system",
  "content": "You are a startup advisor. Always analyze ideas by market size, feasibility, profit potential, and scalability. Give structured output."
  }
```

User Prompt — "WHAT the user wants right now"  
Purpose:
It contains:
The actual question
The data
The user’s request
This is your runtime input.

```
{
  "role": "user",
  "content": f"tell me the best idea... {businessResults}"
}

```

# **load_dotenv(override=True)**

The command load_dotenv(override=True) is used in Python with the python-dotenv library to load environment variables from a .env file and, importantly, force them to replace any existing environment variables in your system's current session.  
 By default, when you use load_dotenv() without the override parameter (which defaults to False), existing system environment variables take precedence over those defined in your .env file

# **Whats the use of paranthesis in a list + expression format for prompts**

```
   messages = (
        [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        + history
        + [
            {"role": "user", "content": message},
        ]
    )
```

The parentheses don’t create a tuple here.
They’re only used to make the expression span multiple lines cleanly. SO basically , it allows to write in multiple lines but the list addition will be the same
Ex : [1,3] + [4,5] + [6,9] => [1,3,4,5,6,9] -> so it allows multiple lines . One long expression

# \*\* \*\*
