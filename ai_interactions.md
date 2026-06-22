# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

I asked the AI assistant to help connect my backend classes in 
pawpal_system.py to my Streamlit app in app.py.

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

The agent helped update app.py so the UI could use the Owner, Pet, Task, 
and Scheduler classes. It helped add session state, task creation, schedule 
generation, filtering, conflict checking, and task completion.

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

I manually tested the app by running streamlit run app.py and clicking 
through the main features. I checked that pets and tasks were saved 
correctly, that the schedule displayed properly, and that recurring 
tasks created the next task when completed.

## Prompt Comparison (SF11)

| Questions | Option A | Option B |

| --------------------- | -------- | -------- |

| **Model / tool used** | VS Code AI assistant | ChatGPT |

| **Prompt** | "Review my scheduler design, point out weak spots." | "Help me keep the scheduler simple but still meet the project requirements." |

| **Response summary** | Suggested more advanced changes like stronger pet references and overlap-based conflict detection. | Suggested simpler improvements like adding 'pet_name', normalizing time, and documenting tradeoffs. |

| **What was useful** | Helped me notice possible design problems. | Helped me choose changes that fit the project scope. |

| **Problems noticed** | Some suggestions felt too complex for the assignment. | Some suggestions still needed to be tested manually. |

| **Decision** | I used only the simple parts that improved the design. | I used this approach for the final implementation. |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->

I used the simpler approach because it matched the project requirements 
better. I kept the scheduler readable, added time normalization, filtering, 
recurring tasks, and exact-time conflict detection without making the system 
too complicated.
