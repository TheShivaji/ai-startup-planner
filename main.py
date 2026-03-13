from openai import OpenAI
import time
from rich.console import Console
from rich.markdown import Markdown as RichMarkdown

# Rich console ko initialize kiya terminal formatting ke liye
console = Console()

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
model = "llama3.2:latest"

system_prompt = "You are a successful startup founder with experience building profitable companies. Your job is to generate startup ideas for students who want to build simple but useful products. Generate exactly the number of ideas requested by the user and do not generate more or fewer ideas than requested. The ideas must be unique and practical, and should not include common concepts like ChatGPT clones, generic AI tools, or very basic apps. Each idea should be simple enough for a student developer to build and should focus on real problems students face in areas such as learning, productivity, career growth, or college life. Each idea must be clear and concise, limited to 1–2 lines only. Do not include explanations, introductions, or any extra text. The output must contain only the requested number of ideas and nothing else."

def startup_idea(user_input):
    user_prompt = f"Generate 3 startup ideas for students who want to build simple but useful products. {user_input}"
    res = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    output = res.choices[0].message.content
    return output

def roadmap_generator(idea):
    roadmap_prompt = "You are an experienced startup product strategist who helps founders turn ideas into structured product roadmaps. Your task is to convert a startup idea into a simple and realistic development roadmap for a student developer. Rules you must follow: The roadmap must be practical and beginner-friendly. Assume a single student developer building an MVP. Break the roadmap into clear stages or weeks. Focus only on building the first working version (MVP). Each step must be short and actionable. Avoid long explanations. Output only the roadmap steps."
    roadmap_user = f"Create a simple development roadmap for the following startup idea. The roadmap should show the steps a student developer should follow to build the first MVP. Startup Idea: {idea}. Return only the roadmap steps."
    res = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": roadmap_prompt},
            {"role": "user", "content": roadmap_user}
        ]
    )
    output = res.choices[0].message.content
    return output

def stack_adviser(idea, roadmap):
    system_architect = "You are a senior software architect who helps startups choose the right technology stack for building MVP products. Your task is to analyze a startup idea and its development roadmap, then recommend a practical tech stack. Rules you must follow: Assume the product will be built by a single student developer. The stack must be simple, practical, and beginner-friendly. Choose technologies that are popular and well documented. Focus on tools needed for building the first working MVP. Avoid complex enterprise architectures. Keep the answer short and structured. The tech stack must include: Frontend, Backend, Database, AI tools or APIs (if needed), Deployment. Return only the tech stack."
    user_architect = f"Recommend a suitable technology stack based on the following startup idea and development roadmap. Startup Idea: {idea}. Product Roadmap: {roadmap}. The stack should help a student developer build the MVP quickly. Return only the tech stack."
    res = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_architect},
            {"role": "user", "content": user_architect}
        ]
    )
    output = res.choices[0].message.content
    return output

# user input
user_input = input('\nAny help to you to find startup idea? ')

print("\nAI is thinking", end="")
for i in range(3):
    time.sleep(1)
    print(".", end="", flush=True)
print("\n")

ideas = startup_idea(user_input)
console.print("[bold cyan]Startup Ideas:[/bold cyan]\n")
console.print(RichMarkdown(ideas))

roadmap = roadmap_generator(ideas)
console.print("\n[bold yellow]Roadmap:[/bold yellow]\n")
console.print(RichMarkdown(roadmap))

stack = stack_adviser(ideas, roadmap)
console.print("\n[bold green]Recommended Tech Stack:[/bold green]\n")
console.print(RichMarkdown(stack))
console.print("\n")