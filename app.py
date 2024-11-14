import os
import requests
import gradio as gr
import random

# Define the Hugging Face API URL for Falcon-7B-Instruct and your API key
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Define the fixed question with larger font and bold using Markdown for proper rendering
# Define the fixed question with larger font and bold using Markdown for proper rendering
QUESTION = "**Create a creative advertisement about a new solution to the storrowing problem.**"

introvert_prompts = [
    f"{QUESTION} Offer a quiet, reflective message.",
    f"{QUESTION} Develop a subtle, insightful ad.",
    f"{QUESTION} Provide a calm and thought-provoking promotional angle.",
    f"{QUESTION} Share an introspective, thoughtful ad message.",
    f"{QUESTION} Present a serene, deep advertisement concept.",
    f"{QUESTION} Propose a gentle, introspective advertisement idea.",
    f"{QUESTION} Craft a soothing and thoughtful promotional message.",
    f"{QUESTION} Design an understated, reflective ad."
] * 50  # Replicates to create a pool of 400 options when shuffled

# Function to query the Hugging Face API with randomness for diversity
def query_huggingface(personality):
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Select a unique prompt variation based on personality type
    if personality == "Introvert":
        prompt = random.choice(introvert_prompts)
    elif personality == "Extrovert":
        prompt = random.choice(extrovert_prompts)

    # Make a request to the Hugging Face API
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    # Check if the response is successful
    if response.status_code == 200:
        # Return only the generated text
        try:
            return response.json()[0]['generated_text']
        except (KeyError, IndexError):
            return "Error: Unexpected response format. Please try again."
    elif response.status_code == 401:
        return "Error: Unauthorized. Please check your API key."
    elif response.status_code == 429:
        return "Error: Rate limit exceeded. Please wait and try again later."
    else:
        # General error message with specific status code
        return f"Error {response.status_code}: {response.text}"

# Create the Gradio interface for Introvert responses
def create_introvert_interface():
    with gr.Blocks() as introvert_interface:
        gr.Markdown("# Introvert Profile")

        # Display question prompt as instructions
        gr.Markdown("### Instructions:\n\nPlease respond to the following prompt:\n\n" + QUESTION)

        with gr.Row():
            user_input = gr.Textbox(label="INPUT", placeholder="Type your response here.", lines=4)
        with gr.Row():
            generated_advertisement = gr.Textbox(label="OUTPUT", lines=4)
        with gr.Row():
            generate_button = gr.Button("Generate")

        # Button to trigger the generation
        generate_button.click(lambda: query_huggingface("Introvert"), None, generated_advertisement)
    return introvert_interface


# Launch the interface for Introvert Profile
print("Launching Introvert Interface...")
introvert_interface = create_introvert_interface()
introvert_interface.launch(server_name="0.0.0.0", server_port=7880)








