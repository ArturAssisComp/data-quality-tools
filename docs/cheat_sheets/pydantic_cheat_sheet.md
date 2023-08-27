# Pydantic Cheat Sheet

<details>
<summary>Table of Contents</summary>

 - [Basics](#basics)
 - [Validators](#validators)
    - [Pre-validators](#pre-validators)
    - [Post-validators](#post-validators)
 - [Field Customization](#field-customization)
 - [Nested Models](#nested-models)
 - [Recursive Models](#recursive-models)
 - [Model Config](#model-config)
 - [Error Handling](#error-handling)
</details>

Pydantic is a Python library for data validation and settings management using Python type annotations. Pydantic ensures that the data adheres to the type hints you provide.

## Basics

Defining a basic Pydantic model:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int
    height: float = None
```
In the example above, a `Person` class is defined with `name` and `age` as required fields and `height` as an optional field with a default value of `None`.

Creating an instance of the model:

```python
p = Person(name='John', age=30)
```
Accessing the fields:

```python
print(p.name)  # Outputs: John
print(p.age)  # Outputs: 30
```

[(back-to-top)](#pydantic-cheat-sheet)
## Validators

Validators are used to add custom validation to the fields.

Example of a validator:

```python
from pydantic import BaseModel, validator

class Person(BaseModel):
    name: str
    age: int

    @validator('age')
    def check_age(cls, age):
        if age < 18:
            raise ValueError('Age must be 18 or older')
        return age
```
In the example above, the `check_age` validator ensures that `age` is 18 or older.

[(back-to-top)](#pydantic-cheat-sheet)
### Pre-validators

Pre-validators are run before the field is set. They are defined using the `pre` argument in the `@validator` decorator:

```python
from pydantic import BaseModel, validator

class Person(BaseModel):
    name: str
    age: int

    @validator('age', pre=True)
    def convert_age_to_int(cls, age):
        return int(age)
```
In the example above, the `convert_age_to_int` pre-validator converts `age` to an integer before it's set.

[(back-to-top)](#pydantic-cheat-sheet)
### Post-validators

Post-validators are run after all the fields have been processed. They are defined by using the `@root_validator` decorator:

```python
from pydantic import BaseModel, root_validator

class Person(BaseModel):
    name: str
    age: int

    @root_validator
    def check_name_and_age(cls, values):
        name = values.get('name')
        age = values.get('age')
        if name == 'John' and age < 30:
            raise ValueError('If the name is John, age must be 30 or more')
        return values
```
In the example above, the `check_name_and_age` post-validator ensures that if the `name` is 'John', the `age` must be 30 or more.

[(back-to-top)](#pydantic-cheat-sheet)
## Field Customization

Fields can be customized using the `Field` function:

```python
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, le=130)
```
In the example above, `name` must be a string between 2 and 50 characters long, and `age` must be an integer greater than 0 and less than or equal to 130.

[(back-to-top)](#pydantic-cheat-sheet)
## Nested Models

Pydantic models can be nested to represent complex data structures:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    zip: str

class Person(BaseModel):
    name: str
    age: int
    address: Address
```

In the example above, `Person` has an `Address` field, which is another Pydantic model.

[(back-to-top)](#pydantic-cheat-sheet)
## Recursive Models

Pydantic supports models that refer to themselves, which is useful for recursive data structures:

```python
from typing import List
from pydantic import BaseModel

class Category(BaseModel):
    name: str
    children: List['Category'] = []

Category.update_forward_refs()
```

In the example above, `Category` has a `children` field that is a list of `Category` instances.

[(back-to-top)](#pydantic-cheat-sheet)
## Model Config

Each Pydantic model has a `Config` class where you can configure its behavior:

```python
from pydantic import BaseModel

class Person(BaseModel):
    name: str
    age: int

    class Config:
        allow_mutation = False
```
In the example above, `allow_mutation` is set to `False` in the `Config` class, which makes `Person` instances immutable.

[(back-to-top)](#pydantic-cheat-sheet)
## Error Handling

When a Pydantic model fails to validate, it raises a `ValidationError`:

```python
from pydantic import BaseModel, ValidationError

class Person(BaseModel):
    name: str
    age: int

try:
    p = Person(name='John', age='thirty')
except ValidationError as e:
    print(e)
```
In the example above, attempting to set `age` to a non-integer value raises a `ValidationError`.

[(back-to-top)](#pydantic-cheat-sheet)

This cheat sheet covers the main features of Pydantic but the library has many more features to offer. Refer to the [official Pydantic documentation](https://pydantic-docs.helpmanual.io/) for more detailed information.