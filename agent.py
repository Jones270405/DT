import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # OpenAI package not installed

class RevisionAIAgent:
    def __init__(self):
        self.state = {
            "last_topic": None,
            "last_prompt_type": None
        }
        self.journal_keywords = [
            "career", "stress", "motivation", "relationships", "study", "confusion", "goals",
            "success", "failure", "friendship", "family", "anxiety", "happiness", "learning"
        ]
        self.qa_keywords = [
            "photosynthesis", "newton's laws", "world war ii", "mitosis", "climate change",
            "pythagorean theorem", "evolution", "gravity", "cell division", "ecosystem"
        ]
        self.cheatsheet_keywords = [
            "cheatsheet", "formula sheet", "quick reference", "summary sheet"
        ]
        self.weak_area_forms = [
            "struggle", "struggling", "difficult", "difficulty", "hard", "problem", "challenge", "trouble", "stuck"
        ]
        self.study_plan_keywords = [
            "study plan", "schedule", "revision plan", "timetable"
        ]

        self.knowledge_base = {
            "mitosis": (
                "Mitosis is a process of cell division in eukaryotic cells that results in two identical daughter cells, "
                "each with the same number of chromosomes as the parent cell. It's essential for growth and tissue repair."
            ),
            "photosynthesis": (
                "Photosynthesis is the process by which green plants and some organisms use sunlight to synthesize foods "
                "from carbon dioxide and water. It produces oxygen as a byproduct."
            ),
            "pythagorean theorem": (
                "The Pythagorean theorem states that in a right-angled triangle, the square of the hypotenuse "
                "is equal to the sum of the squares of the other two sides: a² + b² = c²."
            ),
            "world war ii": (
                "World War II was a global conflict from 1939 to 1945 involving most of the world's nations. "
                "It was marked by significant events like the Holocaust, atomic bombings, and the formation of the United Nations."
            ),
            "newton's laws": (
                "Newton's laws of motion describe the relationship between the motion of an object and the forces acting on it. "
                "They are fundamental to understanding classical mechanics."
            ),
            "cell division": (
                "Cell division is the process by which a parent cell divides into two or more daughter cells. "
                "It includes processes like mitosis and meiosis."
            ),
            "ecosystem": (
                "An ecosystem is a community of living organisms interacting with each other and their non-living environment."
            ),
            "evolution": (
                "Evolution is the process by which different kinds of living organisms develop and diversify from earlier forms "
                "over generations, primarily through natural selection."
            ),
            "gravity": (
                "Gravity is the force that attracts two bodies toward each other. On Earth, it gives weight to physical objects "
                "and causes them to fall toward the ground when dropped."
            ),
            "climate change": (
                "Climate change refers to long-term shifts in temperatures and weather patterns, mainly caused by human activities "
                "like burning fossil fuels."
            ),
            "photosynthesis equation": (
                "The photosynthesis equation is 6 CO2 + 6 H2O + light energy"
                "→ C6H12O6 (glucose) + 6 O2."
            ),
            "artificial intelligence":(
            "AI refers to the simulation of human intelligence by machines, enabling them to learn, reason, and make decisions.",
            ),
            "mental health":(
            "Mental health refers to cognitive, behavioral, and emotional well-being. It is essential for daily living and overall quality of life.",
            ),
            "agriculture":(
            "Agriculture is the practice of cultivating plants and livestock for food, fiber, and other products.",
            ),
            "sports":(
            "Sports involve physical activity and competition, often organized and governed by rules and regulations.",
            ),
            "education":(
            "Education is the process of facilitating learning, or the acquisition of knowledge, skills, values, morals, beliefs, and habits.",
            ),
            "technology":(
            "Technology encompasses the tools, machines, techniques, and systems that make human life easier and more efficient.",
            ),
            "healthcare":(
            "Healthcare refers to the maintenance or improvement of health via the prevention, diagnosis, treatment, recovery, or cure of disease, illness, injury, and other physical and mental impairments in people.",
            ),
            "environment":(
            "The environment encompasses all living and non-living things occurring naturally on Earth or some region thereof.",
            ),
            "economy":(
            "An economy is a region where goods and services are made and traded.",
            ),
            "society":(
            "Society is a group of people who live in the same geographical area and share common values, norms, and customs.",
            ),
            "space":(
            "Space is the boundless three-dimensional extent in which objects and events have relative position and direction.",
            ),
            "travel":(
            "Travel is the movement of people between distant geographical locations.",
            ),
            "food":(
            "Food is any substance consumed to provide nutritional support for an organism.",
            ),
            "art":(
            "Art is a diverse range of human activities in creating visual, auditory, or performing artifacts (artworks), expressing the author's imaginative, conceptual ideas, or technical skill, intended to be appreciated for their beauty or emotional power.",
            ),
            "ai ethics":(
            "AI ethics is the study of the ethical implications of artificial intelligence.",
            ),
            "biotechnology":(
            "Biotechnology is the use of biological organisms, systems, or processes to create or modify products for specific use.",
            ),
            "digital privacy":(
            "Digital privacy refers to the ability of individuals to control the collection, use, and dissemination of their personal data.",
            ),
            "space colonization":(
            "Space colonization involves the establishment of human settlements in outer space, such as on the Moon or Mars.",
            ),
            "neurotechnology":(
            "Neurotechnology is the use of technology to study, understand, and manipulate the brain and nervous system.",
            ),
            "renewable energy":(
            "Renewable energy is energy that is collected from renewable resources, which are naturally replenished on a human timescale.",
            ),
            "smart cities":(
            "Smart cities use digital technology to improve the quality of life for their citizens.",
            ),
            "personalized medicine":(
            "Personalized medicine is a medical approach that uses an individual's genetic profile to guide treatment decisions.",
            ),
            "virtual reality":(
            "Virtual reality is a simulated experience that can be similar to or completely different from the real world.",
            ),
            "sustainable technology":(
            "Sustainable technology is technology that is designed to minimize environmental impact and promote sustainability.",
            ),
            "mHealth":(
            "mHealth is the use of mobile devices and wireless technology to improve health outcomes.",
            ),
            "telemedicine":(
            "Telemedicine is the use of telecommunications and information technology to provide clinical health care from a distance.",
            ),
            "healthcare innovation":(
            "Healthcare innovation is the introduction of new ideas, processes, or products into healthcare."
            )
        }

        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and OpenAI is not None:
            self.client = OpenAI(api_key=api_key)
            self.llm_enabled = True
        else:
            self.client = None
            self.llm_enabled = False

    def input_understanding(self, user_input):
        user_input = user_input.strip().lower()
        if not user_input:
            return "invalid", None

        if "journal" in user_input or "prompt" in user_input:
            for keyword in self.journal_keywords:
                if keyword in user_input:
                    return "journal_prompt", keyword
            return "journal_prompt", None

        if any(word in user_input for word in self.cheatsheet_keywords):
            for keyword in self.qa_keywords + self.journal_keywords:
                if keyword in user_input:
                    return "cheatsheet", keyword
            return "cheatsheet", None

        if any(word in user_input for word in self.weak_area_forms):
            for keyword in self.qa_keywords + self.journal_keywords:
                if keyword in user_input:
                    return "weak_area", keyword
            return "weak_area", None

        if any(word in user_input for word in self.study_plan_keywords):
            for keyword in self.qa_keywords + self.journal_keywords:
                if keyword in user_input:
                    return "study_plan", keyword
            return "study_plan", None

        if "question" in user_input or "q&a" in user_input or "what is" in user_input or "explain" in user_input:
            for keyword in self.qa_keywords + self.journal_keywords:
                if keyword in user_input:
                    return "qna", keyword
            return "qna", None

        if "summarize" in user_input or "summary" in user_input:
            for keyword in self.qa_keywords + self.journal_keywords:
                if keyword in user_input:
                    return "summarize", keyword
            return "summarize", None

        if "think about" in user_input or "something" in user_input:
            return "vague", None

        return "vague", None

    def state_tracker(self, intent, topic):
        if topic:
            self.state["last_topic"] = topic
        self.state["last_prompt_type"] = intent

    def build_llm_prompt(self, intent, topic, user_input):
        if intent == "journal_prompt":
            return f"Create a journaling prompt about {topic or 'a general topic'}."
        elif intent == "cheatsheet":
            return f"Create a concise cheatsheet for {topic or 'a general subject'}."
        elif intent == "weak_area":
            return f"Give advice and resources for a student struggling with {topic or 'a subject'}."
        elif intent == "study_plan":
            return f"Make a 4-day study plan for {topic or 'a subject'}."
        elif intent == "qna":
            return f"Answer this question for a student: {user_input}"
        elif intent == "summarize":
            return f"Summarize the following topic or text: {topic or user_input}"
        else:
            return f"Help a student revise for exams. Input: {user_input}"

    def task_planner(self, intent, topic, user_input):
        # Normalize topic key for lookup
        if topic:
            topic_key = topic.lower().replace("-", " ").replace("_", " ").strip()
        else:
            topic_key = None

        # 1. Try local knowledge base for Q&A
        if intent == "qna" and topic_key and topic_key in self.knowledge_base:
            return "output", self.knowledge_base[topic_key]

        # 2. Try local knowledge base for summary
        if intent == "summarize" and topic_key and topic_key in self.knowledge_base:
            return "output", f"Summary of {topic_key}: {self.knowledge_base[topic_key]}"

        # 3. Use LLM if enabled and not handled by local KB
        if self.llm_enabled:
            prompt = self.build_llm_prompt(intent, topic, user_input)
            try:
                completion = self.client.chat.completions.create(
                    model="gpt-4o",  # or "gpt-3.5-turbo"
                    messages=[
                        {"role": "system", "content": "You are a helpful study assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=300,
                )
                return "output", completion.choices[0].message.content.strip()
            except Exception as e:
                return "output", f"(LLM error: {e}) Falling back to built-in response."

        # 4. Built-in responses fallback
        if intent == "journal_prompt":
            if topic:
                return "output", (
                    f"Here's a journaling prompt about {topic}:\n"
                    f"*Reflect on your experiences with {topic}. What challenges have you faced, and what have you learned from them?*"
                )
            else:
                return "output", (
                    "Here's a general journaling prompt:\n"
                    "*Write about a recent experience that challenged your perspective and what you learned from it.*"
                )
        elif intent == "cheatsheet":
            if topic:
                return "output", (
                    f"Here's a quick cheatsheet for {topic}:\n"
                    f"- Key concepts\n- Important formulas\n- Common mistakes\n- Quick tips\n"
                    f"(For a detailed cheatsheet, specify which part of {topic} you want summarized!)"
                )
            else:
                return "output", (
                    "Please specify the subject or topic for your cheatsheet."
                )
        elif intent == "weak_area":
            if topic:
                return "output", (
                    f"It seems you're struggling with {topic}. Try reviewing your notes, practicing problems, or asking a friend/teacher for help. "
                    f"Would you like a summary or practice questions on {topic}?"
                )
            else:
                return "output", (
                    "Tell me which topic or concept you find difficult, and I'll help you focus your revision there."
                )
        elif intent == "study_plan":
            if topic:
                return "output", (
                    f"Here's a simple study plan for {topic}:\n"
                    f"- Day 1: Review basic concepts\n- Day 2: Practice problems\n- Day 3: Take a mock quiz\n- Day 4: Revise weak areas\n"
                    f"Adjust the plan based on your exam date and comfort level!"
                )
            else:
                return "output", (
                    "Let me know which subject or topic you want a study plan for."
                )
        elif intent == "qna":
            if topic:
                return "output", (
                    f"Here's a quick answer about {topic}:\n"
                    f"(This is a placeholder. For richer answers, connect to an LLM or expand the knowledge base.)"
                )
            else:
                return "output", (
                    "Ask me any study question, and I'll do my best to answer."
                )
        elif intent == "summarize":
            if topic:
                return "output", (
                    f"Here's a summary of {topic}:\n"
                    f"(Main points, key facts, and a brief overview go here.)"
                )
            else:
                return "output", (
                    "Please provide the text or topic you'd like summarized."
                )
        elif intent == "vague":
            return "output", (
                "Here's something to think about:\n"
                "*What is one belief you hold that you’ve never questioned, and how might your perspective change if you explored it further?*"
            )
        elif intent == "invalid":
            return "output", (
                "It looks like your request is empty. Please tell me what you’d like help with—such as a topic, question, or area you want to revise."
            )
        else:
            return "output", (
                "I'm not sure how to help with that. Could you please clarify your request?"
            )

    def output_generator(self, action, content):
        if action == "output":
            return content

    def respond(self, user_input):
        intent, topic = self.input_understanding(user_input)
        self.state_tracker(intent, topic)
        action, content = self.task_planner(intent, topic, user_input)
        return self.output_generator(action, content)


if __name__ == "__main__":
    agent = RevisionAIAgent()
    print("Hey, enter your request, I will try to help! (or type 'exit' to quit):")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.respond(user_input)
        print("AI:", response)
