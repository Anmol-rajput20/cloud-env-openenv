import random
from pydantic import BaseModel

class Action(BaseModel):
    action: int  # 0, 1, 2

class State(BaseModel):
    cpu: float
    servers : int
    requests : int
    cost : float

class CloudEnv:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        self.max_steps = 50

    def reset(self):
        self.servers = 3
        self.time = 0
        self._generate_requests()
        return self._get_state()
    
    def _generate_requests(self):
        base = 100 + 80 * (self.time % 5)

        if self.difficulty == "easy":
            self.requests = base + random.randint(-20,20)
        elif self.difficulty == "medium":
            self.requests = random.randint(-80,80)
        else:
            #Hard -> spikes
            if random.random() < 0.3:
                self.requests = random.randint(200,400)
            else:
                self.requests = base + random.randint(-120,120)

    def _get_state(self):
        cpu = (self.requests / (self.servers*50)) * 100
        cost = self.servers * 10


        return State(
            cpu = cpu,
            servers = self.servers,
            requests = self.requests,
            cost = cost
        )
    
    def step(self,action):
        """
        Actions : 
        0 = add_server
        1 = remove_server
        2 = do_nothing

        """

        self.time += 1

        if action == 0:
            self.servers += 1
        elif action == 1 and self.servers > 1:
            self.servers -= 1

        if random.random() < 0.05:  # 5% chance
            self.servers = max(1, self.servers - 1)

        
        self._generate_requests()

        state = self._get_state()

       # performance score (0 to 1)

        if state.cpu <= 70:
            performance = 1.0
        elif state.cpu <= 90:
            performance = 0.3
        else:
            performance = -1.0

        cost_penalty = state.servers * 0.05
        overload_penalty = max(0,(state.cpu - 100)/50)
       

        reward = performance - cost_penalty - overload_penalty

        done = self.time >= self.max_steps

        return state,reward, done, {}
    
    def state(self):
        return self._get_state()
    
if __name__=="__main__":
    env = CloudEnv("easy")
    state = env.reset()

    for _ in range(10):
        action = random.choice([0,1,2])
        next_state,reward,done, _ = env.step(action)

        print(f"State: {next_state}")
        print(f"Reward : {reward}")
        print("----")

        if done:
            break
        



        