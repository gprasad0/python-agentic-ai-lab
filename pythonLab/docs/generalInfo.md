1. # **what is pydantic**

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

2. # **what is a decorator**

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

3. # **what is ** in python\*\*

   The symbol \* is used for unpacking or spreading lists or tuple  
   the symbol \*\* is used for unpacking or spreading dict[dictionary]

4. # **Difference in importing files**

   import gradio as gr -> This imports the entire module/package and gives it an alias  
   from pypdf import PdfReader -> This imports only one class from the package.

5. # **Correct naming rules for Python files (modules)**
   Python file names must:
   - start with letter or underscore
   - contain only letters, numbers, underscores
   - cannot contain - or spaces
