from env import CloudEnv
from agent import get_action
from datasets import Dataset
from unsloth import FastLanguageModel
from transformers import TrainingArguments
from trl import SFTTrainer
import matplotlib.pyplot as plt

# --------- DATA GENERATION ---------
data = []

for difficulty in ["easy", "medium", "hard"]:
    env = CloudEnv(difficulty)

    for episode in range(200):
        state = env.reset()

        while True:
            action = get_action(state)

            data.append({
                "input": f"cpu={state.cpu}, servers={state.servers}, requests={state.requests}, trend={state.trend}",
                "output": str(action)
            })

            state, reward, done, _ = env.step(action)

            if done:
                break

print("Samples:", len(data))

dataset = Dataset.from_list(data)

def format_prompt(example):
    return {
        "text": f"State: {example['input']}\nAction: {example['output']}"
    }

dataset = dataset.map(format_prompt)

# --------- MODEL ---------
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/mistral-7b-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    target_modules=["q_proj","k_proj","v_proj","o_proj"],
    lora_alpha=16,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing=True,
)

# --------- TRAINING ---------
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=2048,
    args=TrainingArguments(
        per_device_train_batch_size=4,
        gradient_accumulation_steps=2,
        num_train_epochs=3,
        learning_rate=1e-4,
        logging_steps=20,
        output_dir="final_outputs",
    ),
)

trainer.train()

# --------- SAVE LOSS CURVE ---------
losses = [log["loss"] for log in trainer.state.log_history if "loss" in log]

plt.plot(losses)
plt.title("Final Training Loss")
plt.xlabel("Steps")
plt.ylabel("Loss")
plt.savefig("final_loss.png")