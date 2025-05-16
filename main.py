from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/hello")
def say_hello():
    return (
        {"message":"👋Hello from FastAPI"}
        )

#define input schema
class GreetInput(BaseModel):
    name :str

@app.post("/greet")
def greetUser(input:GreetInput):
    # input is now a Python object, not raw JSON
    return {"message":f"Hello {input.name}"}