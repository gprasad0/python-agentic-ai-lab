1. **Difference bw system and user prompts**

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

2. **what is pydantic**

Its a library that validates an object for the correct types  
Pydantic lets you trust your data before your code touches it.

Ex:

```
from pydantic import BaseModel

userObj = {
    name: "Guru",
    age: 30
}
class User(BaseModel)
    age: int
    nam: str

user = User(**userObj)
```

So if the name is not a string , it will throw an error
It also does type conversion

Ex:

```
user = {age:"1"}
age = user.age + 1  // crash


```

```
USING PYDANTIC:
from pydantic import BaseModel
class User(BaseModel):
age: int

    user = User({age: "1"})
    print(User.age + 1)  // 2 Works

```

3. **what is a decorator**

```
from pydantic import field_validator

class Address(BaseModel):
    pincode: int

    @field_validator("pincode")
    def check_pincode(cls, v):
        if len(str(v)) != 6:
            raise ValueError("pincode must be 6 digits")
        return v
```

@field_validator("pincode") - This is a decorator.  
@ is Python’s syntax for a decorator.  
A decorator means:

"Before or after this function runs, modify its behavior."  
Attach this function to the pincode validation pipeline.

4. **what is ** in python**  
   The symbol \* is used for unpacking or spreading lists or tuple
   the symbol ** is used for unpacking or spreading dict[dictionary]
