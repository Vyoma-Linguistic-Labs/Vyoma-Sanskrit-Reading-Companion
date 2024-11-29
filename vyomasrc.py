import os
import csv
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Serve static files from the 'csv' directory
@app.route('/csv/<path:filename>')
def serve_staticfile(filename):
    try:
        # Define the path to the csv folder
        csv_folder = os.path.join(os.getcwd(), 'csv')
        return send_from_directory(csv_folder, filename)
    except Exception as e:
        print(f"Error serving file: {e}")
        return f"Error serving file: {e}"

# Function to load menu items from menu.csv
def load_menu_items():
    menu_csv_path = os.path.join('csv', 'menu.csv')
    menu_items = []
    try:
        with open(menu_csv_path, mode='r', encoding='utf-8-sig') as menufile:
            reader = csv.DictReader(menufile)
            for row in reader:
                # Ensure menu items are properly populated with fallbacks if needed
                main_menu = row.get('Main Menu', 'Unknown Menu')
                sub_menu = row.get('Sub Menu', '')
                sub_menu_link = row.get('Sub Menu Link', '')

                # Only append if main menu is valid, to avoid None or undefined issues
                if main_menu:
                    menu_items.append({
                        'Main Menu': main_menu,
                        'Sub Menu': sub_menu,
                        'Sub Menu Link': sub_menu_link
                    })
    except Exception as e:
        print(f"Error loading menu: {e}")
    return menu_items

@app.route('/')
def home():
    try:
        # Path to the texts.csv file
        csv_file_path = os.path.join('csv', 'texts.csv')
        
        # Load and parse texts.csv
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            texts = list(reader)

        # Load menu items using the reusable function
        menu_items = load_menu_items()

        # Render the home page with the list of texts and menu items
        return render_template('index.html', texts=texts, menu_items=menu_items)
    
    except Exception as e:
        return f"Error loading data: {e}"

@app.route('/csv/<text_name>/contents.csv')
def load_text(text_name):
    try:
        # Load menu items for consistency across all pages
        menu_items = load_menu_items()

        # Path to the texts.csv file to get the Display Name and Subtitle
        texts_csv_path = os.path.join('csv', 'texts.csv')
        display_name = text_name  # Default value if not found
        subtitle = ''  # Default empty subtitle

        # Fetch the Display Name and Subtitle for the current text from texts.csv
        with open(texts_csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Contents File'] == f"{text_name}/contents.csv":
                    display_name = row['Display Name']
                    subtitle = row.get('Subtitle', '')  # Subtitle may be optional
                    break

        # Path to the contents.csv in the selected text's folder
        csv_file_path = os.path.join('csv', text_name, 'contents.csv')

        if not os.path.exists(csv_file_path):
            return f"Error: contents.csv not found for {text_name}"

        # Load and parse contents.csv
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            essays = list(reader)

        # Render the components page with the essays list, Display Name, Subtitle, and menu items
        return render_template('components.html', essays=essays, text_name=text_name, display_name=display_name, subtitle=subtitle, menu_items=menu_items)

    except Exception as e:
        return f"Error loading contents: {e}"

@app.route('/csv/<text_name>/components/<component_name>')
def load_essay(text_name, component_name):
    try:
        # Load menu items for consistency across all pages
        menu_items = load_menu_items()

        # Path to the general texts.csv file, NOT inside the text_name folder
        texts_csv_path = os.path.join('csv', 'texts.csv')  # Corrected path
        display_name = text_name  # Default value if not found
        
        # Fetch the Display Name from texts.csv
        with open(texts_csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Contents File'] == f"{text_name}/contents.csv":
                    display_name = row['Display Name']
                    break

        # Path to the contents.csv file to get the Essay Name inside the text folder
        contents_csv_path = os.path.join('csv', text_name, 'contents.csv')
        essay_name = component_name  # Default value if not found
        
        # Fetch the Essay Name from contents.csv
        with open(contents_csv_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['Essay Filename'] == component_name:
                    essay_name = row['Essay Name']
                    break

        # Path to the selected component's CSV file inside the text_name folder
        essay_file_path = os.path.join('csv', text_name, 'components', component_name, f'{component_name}.csv')
        
        # Load and parse the essay's CSV file
        with open(essay_file_path, mode='r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            essay_content = list(reader)

        # Get the available languages from the CSV column names (excluding 'Sanskrit Line')
        languages = [key for key in essay_content[0].keys() if key != 'Sanskrit Line']

        # Load the audio files, starting from line-00.mp3 for the heading
        audio_folder = os.path.join('csv', text_name, 'components', component_name)
        audio_files = [f'/csv/{text_name}/components/{component_name}/line-{str(i).zfill(2)}.mp3' for i in range(len(essay_content) + 1)]  # Include line-00.mp3

        # Load word explanations from word_explanations.csv
        explanations_file_path = os.path.join('csv', text_name, 'word_explanations.csv')
        word_explanations = {}
        if os.path.exists(explanations_file_path):
            with open(explanations_file_path, mode='r', encoding='utf-8-sig') as expfile:
                reader = csv.DictReader(expfile)
                word_explanations = {row['Word']: row['Explanation'] for row in reader}

        # Check for quiz files (c1_q1.csv, c1_q2.csv, etc.)
        quizzes = []
        for quiz_type in ['q1', 'q2', 'q3']:  # For each quiz type
            quiz_file_path = os.path.join('csv', text_name, 'components', component_name, f'{component_name}_{quiz_type}.csv')
            if os.path.exists(quiz_file_path):
                quizzes.append(quiz_type)

        # Render the essay page with the parsed content, languages, audio files, word explanations, and quiz availability
        return render_template('component.html', 
                               essay_content=essay_content, 
                               text_name=text_name,  # Keep text_name as is
                               component_name=component_name,  # Keep component_name as is (e.g., c1)
                               display_name=display_name,  # Use the display name for text
                               essay_name=essay_name,  # Use the essay name
                               languages=languages, 
                               audio_files=audio_files, 
                               word_explanations=word_explanations,
                               quizzes=quizzes,  # Pass available quizzes to the frontend
                               menu_items=menu_items)  # Pass menu items to the template
    except Exception as e:
        return f"Error loading essay: {e}"




if __name__ == '__main__':
    app.run(debug=True)
