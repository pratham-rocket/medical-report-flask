from flask import Flask, request, render_template
import google.generativeai as genai  

genai.configure(api_key="AIzaSyBRcKgeCI9_3pUxpeMuzpHEekq9azWb9zs")
app = Flask(__name__, static_folder="assets", template_folder="templates")

def load_model(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        suggestion = response.text.strip()
        return suggestion
    except Exception as e:
        print(e)
        return "Sorry, but Gemini didn't want to answer that!"

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        try:
            disease_name = request.form['disease_name']
            years = request.form['years']
            age = request.form['age']
            history = request.form['history']
            addiction = request.form['addiction']
            medication = request.form['medication']
            constraint = (
                " give in bullets, do not add ** around titles, "
                "start each new point on a new line, "
                "and avoid giving the output as one long paragraph."
            )
            concept = (
                f"You are an expert medical healthcare specialist. You always give a report of the current condition. "
                f"There is a case of {disease_name} from {years} days. "
                f"The patient is {age} years old and has a family history of {history}. "
                f"They have an addiction of {addiction} and are currently on {medication} prescribed by a doctor."
            )
            suggestion1 = load_model(concept + " Give the description for this case." + constraint)
            suggestion2 = load_model(concept + " Give the diagnosis for this case." + constraint)
            suggestion3 = load_model(concept + " Give the precaution for this case." + constraint)
            suggestion4 = load_model(concept + " Give the follow-up recommendations for this case." + constraint)
            return render_template(
                "Index.html",
                suggestion1=suggestion1,
                suggestion2=suggestion2,
                suggestion3=suggestion3,
                suggestion4=suggestion4
            )
        except Exception as e:
            print(e)
            return "Sorry, but Gemini didn't want to answer that!"
    else:
        return render_template('form.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
