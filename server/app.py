from fastapi import FastAPI
from pydantic import BaseModel
from env import CloudEnv

app = FastAPI()

env = None

class Action(BaseModel):
    action: int

@app.get("/")
def home():
    return {"message": "Cloud OpenEnv is running "}

@app.post("/reset")
def reset():
    global env
    env = CloudEnv("easy")  # default
    state = env.reset()
    return state.__dict__

@app.post("/step")
def step(action: Action):
    global env
    state, reward, done, _ = env.step(action.action)
    return {
        "state": state.__dict__,
        "reward": reward,
        "done": done
    }

@app.get("/state")
def get_state():
    global env
    return env.state().__dict__

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()