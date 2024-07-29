import os
import anthropic
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set the input and output folder paths
input_folder_path = r"CHOOSE INPUT FOLDER"
output_folder_path = r"CHOOSE OUTPUT FOLDER"

# Authenticate with the Anthropic API using your API key
client = anthropic.Client(api_key="YOUR CLAUDE 3 Haiku API")

# Specify the Claude model to use
model = "claude-3-haiku-20240307"

def make_api_call(prompt):
    messages = [{"role": "user", "content": prompt}]
    
    try:
        logging.info("Connecting to API")
        response = client.messages.create(
            model=model,
            messages=messages,
            max_tokens=4000,
            stop_sequences=["\n\nHuman:"],
        )
        result = response.content[0].text
        logging.info("Successfully connected to API")
        return result
    except Exception as e:
        logging.error(f"API request failed: {str(e)}")
        return None

def process_title(title):
    prompt = f"""{title}\n\nHuman: Make an 2000 word article from the title provided and make sure to go into detail with sub topics and headings for each sub topic"""
    return prompt

def save_document(result, title):
    try:
        clean_title = re.sub(r'[^\w\s]', '', title)
        clean_title = re.sub(r'\s+', ' ', clean_title).strip()

        filename = clean_title + ".txt"
        new_doc_path = os.path.join(output_folder_path, filename)
        with open(new_doc_path, 'w', encoding='utf-8') as f:
            f.write(result)
        logging.info(f"Saved document: {filename}")
    except Exception as e:
        logging.error(f"Error saving document {title}: {str(e)}")

def main():
    try:
        titles_file = os.path.join(input_folder_path, "titles.txt")
        with open(titles_file, 'r', encoding='utf-8') as f:
            titles = f.readlines()
        
        for title in titles:
            title = title.strip()
            if title:
                prompt = process_title(title)
                result = make_api_call(prompt)
                if result:
                    save_document(result, title)
        
        logging.info("All titles processed and saved.")
    except Exception as e:
        logging.error(f"Error processing titles: {str(e)}")

if __name__ == "__main__":
    main()