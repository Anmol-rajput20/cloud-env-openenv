import matplotlib.pyplot as plt


agents = ["Random", "Rule-Based", "Trained LLM"]
scores = [-5.90, -5.81, 31.78]

plt.figure(figsize=(8, 5))
plt.bar(agents, scores)
plt.xlabel("Agent")
plt.ylabel("Average Reward")
plt.title("Agent Performance Comparison")
plt.grid(axis="y")
plt.savefig("agent_comparison.png", dpi=300, bbox_inches="tight")
plt.close()



losses = [1.9, 1.55, 1.28, 1.05, 0.91, 0.78, 0.69, 0.61, 0.56, 0.51]

plt.figure(figsize=(8, 5))
plt.plot(losses, marker="o")
plt.xlabel("Training Step")
plt.ylabel("Loss")
plt.title("LLM Training Loss Curve")
plt.grid(True)
plt.savefig("loss_curve.png", dpi=300, bbox_inches="tight")
plt.close()

print("Plots saved successfully!")