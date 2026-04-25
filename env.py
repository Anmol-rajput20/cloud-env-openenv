import random
from pydantic import BaseModel

class Action(BaseModel):
    action: int  # 0, 1, 2

class State(BaseModel):
    cpu: float
    servers : int
    requests : int
    cost : float
    trend: float

class CloudEnv:
    def __init__(self, difficulty="easy"):
        self.difficulty = difficulty
        self.max_steps = 50

    def reset(self):
        self.servers = 3
        self.time = 0

        self.requests = 100
        self.trend = 0
        self.prev_requests = 100

        self._generate_requests()
        return self._get_state()
    
    def _generate_requests(self):
        prev_requests = self.requests


        if self.difficulty == "easy":
            self.requests = max(10,self.requests + random.randint(-20,20))
        elif self.difficulty == "medium":
            self.requests = max(10, self.requests + random.randint(-50,50))
        else:
            #Hard -> spikes
            if random.random() < 0.2:
                self.requests += random.randint(150,300)
            else:
                self.requests = max(10, self.requests + random.randint(-70,70))

        self.trend = self.requests - prev_requests

    def _get_state(self):
        cpu = (self.requests / (self.servers*50)) * 100
        cpu = min(cpu,150)
        cost = self.servers * 10

        return State(
            cpu = cpu,
            servers = self.servers,
            requests = self.requests,
            cost = cost,
            trend = self.trend
        )
    
    def step(self,action):
        """
        Actions : 
        0 = add_server
        1 = remove_server
        2 = do_nothing

        """

        self.time += 1
        prev_cpu = (self.requests / (self.servers * 50)) * 100

        if action == 0:
            self.servers += 1
        elif action == 1 and self.servers > 1:
            self.servers -= 1

        if random.random() < 0.05:  # 5% chance
            self.servers = max(1, self.servers - 1)

        self._generate_requests()

        state = self._get_state()

       # performance score (0 to 1)

        reward = 0

        if 50 <= state.cpu <= 75:
            reward += 3.5
        elif state.cpu < 30:
            reward -= 1.5
        elif 75 < state.cpu <= 90:
            reward -= 0.5
            

        reward -= state.servers * 0.03
        
        if abs(state.cpu - prev_cpu) > 20:
            reward -= 0.2


        if abs(state.cpu - prev_cpu) < 10:
            reward += 0.3 

        if state.cpu > 100:
            reward -= (state.cpu - 100) * 0.08
       

        if action in [0,1]:
            reward -= 0.05

        if state.trend > 20 and action == 0:
            reward += 0.8

        if state.trend < -20 and action == 1:
            reward += 0.8

        if state.trend > 40 and action == 0:
            reward += 0.8

        if state.trend > 40 and action != 0:
            reward -= 1.0


        done = self.time >= self.max_steps or state.cpu > 130

        return state, reward, done, {}

    
    def get_state(self):
        return self._get_state()
    
if __name__=="__main__":
    env = CloudEnv("hard")
    state = env.reset()

    for _ in range(20):
        action = random.choice([0,1,2])
        next_state,reward,done, _ = env.step(action)

        print(f"State: {next_state}")
        print(f"Reward : {reward}")
        print("----")

        if done:
            break
        



        