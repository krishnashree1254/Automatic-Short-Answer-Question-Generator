import re
from flask import Flask, render_template, request, session
from flask_mail import Mail
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# NLTK Downloads (if not already downloaded)
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

app = Flask(__name__)
app.secret_key = 'mysecretkey'

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME='asqag.cutm@gmail.com',
    MAIL_PASSWORD='your_gmail_password'  # Replace with your actual password
)
mail = Mail(app)

app.debug = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        suggestion = request.form['suggestion']
        receipents = ['asqag.cutm@gmail.com']
        mail.send_message("ASQAG",
                          sender=email,
                          recipients=receipents,
                          body="NEW SUGGESTION FROM " + name + "\n--------------------\n\n\nSuggestion: " + suggestion
                          )
    return render_template('index.html')


@app.route("/mainPage")
def mainPage():
    return render_template('mainPage.html')


@app.route('/process_form', methods=['POST'])
def process_form():
    text = request.form['user_input']
    session['user_input'] = text

    from nltk import word_tokenize, pos_tag
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer

    def generate_questions(text, level):
        # Text Preprocessing
        words = word_tokenize(text.lower())
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
        pos_tags = pos_tag(lemmatized_words)

        questions = []
        count = 0

        # Mapping Bloom's Levels
        question_count = int(request.form['question-count'])  # Number of questions requested
        for word, word_pos in pos_tags:
            if count >= question_count:
                break

            if word.isalnum():
                # Bloom's Taxonomy-based Question Generation
                if level == 1:
                    # Remembering
                    if word_pos.startswith('CC'):  # Coordinating Conjunction
                        questions.append(
                            f"Can you recall a sentence from the text that uses the coordinating conjunction {word.upper()}?")
                    elif word_pos.startswith('CD'):  # Cardinal Number
                        questions.append(
                            f"{word.upper()} is used to quantify _____.")
                    elif word_pos.startswith('DT'):  # Determiner
                        questions.append(
                            f"Identify a sentence where the determiner {word.upper()} is used to specify a noun.")
                    elif word_pos.startswith('IN'):  # Preposition or Subordinating Conjunction
                        questions.append(
                            f"Recall a sentence containing the preposition {word.upper()} and describe its role.")
                    elif word_pos.startswith('JJ'):  # Adjective
                        questions.append(
                            f"Can you remember {word.upper()} used in the text to describe a noun? Provide an example.")
                    elif word_pos.startswith('NN'):  # Noun, Singular or Mass
                        questions.append(f"What is {word.upper()}? Briefly describe its significance.")
                    elif word_pos.startswith('VB'):  # Verb, Base Form
                        questions.append(f"What action does {word.upper()} convey?")
                    elif word_pos.startswith('RB'):  # Adverb
                        questions.append(
                            f"Recall {word.upper()} used in the text. How does it modify the meaning of a verb?")
                    elif word_pos.startswith('PRP'):  # Personal Pronoun
                        questions.append(
                            f"Can you remember a sentence with {word.upper()}? Who or what does it refer to?")
                    elif word_pos.startswith('UH'):  # Interjection
                        questions.append(
                            f"What interjection expresses surprise or emotion in the passage? Provide an example.")
                    elif word_pos.startswith('SYM'):  # Symbol
                        questions.append(f"Remember {word.upper()} used in the text. What does it signify?")
                    count += 1

                elif level == 2:
                    # Understanding
                    if word_pos.startswith('CC'):  # Coordinating Conjunction
                        questions.append(
                            f"Explain how the use of {word.upper()} contributes to the flow of the text.")
                    elif word_pos.startswith('CD'):  # Cardinal Number
                        questions.append(
                            f"Can you describe the role of {word} in quantifying something in this context?")
                    elif word_pos.startswith('DT'):  # Determiner
                        questions.append(
                            f"How does {word.upper()} contribute to the specificity the sentence?")
                    elif word_pos.startswith('IN'):  # Preposition or Subordinating Conjunction
                        questions.append(
                            f"Elaborate on how {word.upper()} establish relationships between elements in the passage.")
                    elif word_pos.startswith('JJ'):  # Adjective
                        questions.append(
                            f"Explain how {word.upper()} influence the tone or mood of the text.")
                    elif word_pos.startswith('NN'):  # Noun, Singular or Mass
                        questions.append(
                            f"Describe the significance of {word.upper()} in the context of the passage.")
                    elif word_pos.startswith('VB'):  # Verb, Base Form
                        questions.append(
                            f"How does {word.upper()} contribute to the overall action or meaning of the text?")
                    elif word_pos.startswith('RB'):  # Adverb
                        questions.append(
                            f"In what manner does {word.upper()} modify the action in the sentence?")
                    elif word_pos.startswith('PRP'):  # Personal Pronoun
                        questions.append(
                            f"Identify the referent of {word.upper()} and explain its role in the passage.")
                    elif word_pos.startswith('UH'):  # Interjection
                        questions.append(
                            f"How does the interjection {word.upper()} express the author's reaction or emotion in this context?")
                    elif word_pos.startswith('SYM'):  # Symbol
                        questions.append(
                            f"Explain the meaning or significance of the symbol {word.upper()} in the context of the numerical information presented.")
                    count += 1

                elif level == 3:
                    # Applying
                    if word_pos.startswith('CC'):  # Coordinating Conjunction
                        questions.append(
                            f"How does the use of {word.upper()} contribute to the coherence of the text?")
                    elif word_pos.startswith('CD'):  # Cardinal Number
                        questions.append(
                            f"Can you identify three instances where {word.upper()} is used to quantify in the text?")
                    elif word_pos.startswith('DT'):  # Determiner
                        questions.append(
                            f"What is the role of {word.upper()} in specifying a particular noun in the passage?")
                    elif word_pos.startswith('IN'):  # Preposition or Subordinating Conjunction
                        questions.append(
                            f"Describe the location or relationship conveyed by {word.upper()} in the text.")
                    elif word_pos.startswith('JJ'):  # Adjective
                        questions.append(
                            f"How does the adjective {word.upper()} describe or modify the noun it precedes in the sentence?")
                    elif word_pos.startswith('NN'):  # Noun, Singular or Mass
                        questions.append(
                            f"Explain the significance of {word.upper()} and its contribution to the overall meaning of the passage.")
                    elif word_pos.startswith('VB'):  # Verb, Base Form
                        questions.append(
                            f"In what context can {word.upper()} be practically applied?")
                    elif word_pos.startswith('RB'):  # Adverb
                        questions.append(
                            f"What impact does {word.upper()} have on the overall meaning?")
                    elif word_pos.startswith('PRP'):  # Personal Pronoun
                        questions.append(
                            f"How does {word.upper()} contribute to the coherence and flow of the passage?")
                    elif word_pos.startswith('UH'):  # Interjection
                        questions.append(
                            f"What emotional tone or expression is conveyed by {word.upper()} in the context of the passage?")
                    elif word_pos.startswith('SYM'):  # Symbol
                        questions.append(
                            f"How does the symbol {word.upper()} symbolize or represent a concept in the numerical information provided?")
                    count += 1
                elif level == 4:
                    # Analyzing
                    if word_pos.startswith('CC'):  # Coordinating Conjunction
                        questions.append(
                            f"Analyze the impact of using {word.upper()} in creating logical connections within a paragraph.")
                    elif word_pos.startswith('CD'):  # Cardinal Number
                        questions.append(
                            f"Compare and contrast the use of different cardinal numbers with {word.upper()} in the text. How do they vary in their roles?")
                    elif word_pos.startswith('DT'):  # Determiner
                        questions.append(
                            f"Examine the function of different determiners (e.g., {word.upper()}) in specifying nouns. How do they contribute to clarity?")
                    elif word_pos.startswith('IN'):  # Preposition or Subordinating Conjunction
                        questions.append(
                            f"Investigate how {word.upper()} affect the relationships between elements in different sentences.")
                    elif word_pos.startswith('JJ'):  # Adjective
                        questions.append(
                            f"Analyze the choice of {word.upper()} in conveying specific qualities. How do they influence the reader's perception?")
                    elif word_pos.startswith('NN'):  # Noun, Singular or Mass
                        questions.append(
                            f"How does {word.upper()} contribute to the overall meaning?")
                    elif word_pos.startswith('VB'):  # Verb, Base Form
                        questions.append(
                            f"Break down the usage of {word.upper()}, How does it contribute to the narrative or description?")
                    elif word_pos.startswith('RB'):  # Adverb
                        questions.append(
                            f"Evaluate the placement and impact of {word.upper()} on different verbs. How does it affect the pace or tone?")
                    elif word_pos.startswith('PRP'):  # Personal Pronoun
                        questions.append(
                            f"Investigate the use of {word.upper()}this context. How does its reference contribute to coherence?")
                    elif word_pos.startswith('UH'):  # Interjection
                        questions.append(
                            f"Examine the role of interjections (e.g., {word.upper()}) in expressing emotions. How do they contribute to the overall tone?")
                    elif word_pos.startswith('SYM'):  # Symbol
                        questions.append(
                            f"Break down the symbolic meanings of {word.upper()} used in numerical contexts. How do they represent different concepts?")
                    count += 1

                elif level == 5:
                    # Evaluating
                    if word_pos.startswith('CC'):  # Coordinating Conjunction
                        questions.append(
                            f"Evaluate the effectiveness of using {word.upper()} in enhancing the coherence of a paragraph.")
                    elif word_pos.startswith('CD'):  # Cardinal Number
                        questions.append(
                            f"Is {word.upper()} most effective in conveying numerical information? If yes, why?")
                    elif word_pos.startswith('DT'):  # Determiner
                        questions.append(
                            f"Assess the impact of different determiners on the precision and clarity of noun identification. Which determiner is most effective in a specific context?")
                    elif word_pos.startswith('IN'):  # Preposition or Subordinating Conjunction
                        questions.append(
                            f"Critique the use of prepositions, including '{word},' in establishing relationships. How does their use impact the overall clarity of the text?")
                    elif word_pos.startswith('JJ'):  # Adjective
                        questions.append(
                            f"Evaluate the choice of '{word},' in conveying specific qualities. How do the choice affect the reader's perception?")
                    elif word_pos.startswith('NN'):  # Noun, Singular or Mass
                        questions.append(
                            f"Critically analyze the contribution of {word.upper()} to the overall meaning and significance of the text.If any other noun has more impact, mention?")
                    elif word_pos.startswith('VB'):  # Verb, Base Form
                        questions.append(
                            f"Assess the effectiveness of {word.upper()} in conveying action. How well does it contribute to the narrative or description?")
                    elif word_pos.startswith('RB'):  # Adverb
                        questions.append(
                            f"Evaluate the use of {word.upper()} in modifying verbs. How does it enhance or detract from the overall tone and pace of the text?")
                    elif word_pos.startswith('PRP'):  # Personal Pronoun
                        questions.append(
                            f"Judge the coherence and clarity achieved through the use of {word.upper()}. Are there instances where its reference is unclear?")
                    elif word_pos.startswith('UH'):  # Interjection
                        questions.append(
                            f"Assess the effectiveness of {word.upper()} in conveying emotions. Does it enhance or detract from the overall tone and engagement?")
                    elif word_pos.startswith('SYM'):  # Symbol
                        questions.append(
                            f"Evaluate the symbolic representations of different symbols (e.g., {word.upper()}) in numerical contexts. How well do they convey the intended concepts?")
                    count += 1

                elif level == 6:
                    # Creating
                    if word_pos.startswith('CC'):  # Coordinating Conjunction
                        questions.append(
                            f"Can you devise a paragraph that effectively uses {word.upper()} to connect ideas and create coherence?")
                    elif word_pos.startswith('CD'):  # Cardinal Number
                        questions.append(
                            f"Devise a set of numerical examples using different cardinal numbers, including '{word},' to illustrate a concept or idea.")
                    elif word_pos.startswith('DT'):  # Determiner
                        questions.append(
                            f"Generate sentences that creatively use {word.upper()} to specify and identify nouns in distinct ways.")
                    elif word_pos.startswith('IN'):  # Preposition or Subordinating Conjunction
                        questions.append(
                            f"Invent new sentences that incorporate {word.upper()} to establish unique relationships between elements.")
                    elif word_pos.startswith('JJ'):  # Adjective
                        questions.append(
                            f"Design sentences that use {word.upper()} to evoke specific imagery and contribute to a desired tone.")
                    elif word_pos.startswith('NN'):  # Noun, Singular or Mass
                        questions.append(
                            f"Invent a passage that introduces and emphasizes the significance of {word.upper()} in a creative and meaningful way.")
                    elif word_pos.startswith('VB'):  # Verb, Base Form
                        questions.append(
                            f"Develop a narrative or description that creatively utilizes {word.upper()} to convey dynamic action.")
                    elif word_pos.startswith('RB'):  # Adverb
                        questions.append(
                            f"Create sentences that skillfully incorporate {word.upper()} to modify verbs and enhance the overall tone and pace.")
                    elif word_pos.startswith('PRP'):  # Personal Pronoun
                        questions.append(
                            f"Invent a short story or paragraph that uses {word.upper()} in a way that maintains clarity and coherence.")
                    elif word_pos.startswith('UH'):  # Interjection
                        questions.append(
                            f"Generate sentences or dialogue that includes {word.upper()} to express a range of emotions and reactions.")
                    elif word_pos.startswith('SYM'):  # Symbol
                        questions.append(
                            f"Create a set of numerical information where different symbols (e.g., {word.upper()}) represent various concepts.")
                    count += 1

                else:
                    questions.append(f"Invalid Bloom's Taxonomy level selected: {level}")

        return questions

    num_questions = int(request.form['selected_opt'])
    print(num_questions)
    questions = generate_questions(text, num_questions)
    session['gen_quest'] = questions

    return render_template('resultPage.html', questions=questions)


@app.route('/process_answers', methods=['POST'])
def process_answers():
    quest = session.get('gen_quest')
    user_answers = [request.form[f'answer{i}'] for i in range(len(quest))]

    user_text = session.get('user_input')

    vectorizer = TfidfVectorizer()

    def calculate_similarity(answers, user_answers):
        vectorizer_count = CountVectorizer()
        vectorizer_tfidf = TfidfVectorizer()

        vectorized_answers_count = vectorizer_count.fit_transform([answer for answer, _ in answers])
        vectorized_answers_tfidf = vectorizer_tfidf.fit_transform([answer for answer, _ in answers])
        user_answers_count = vectorizer_count.transform(user_answers)
        user_answers_tfidf = vectorizer_tfidf.transform(user_answers)

        co_occurrence_similarity_scores_count = cosine_similarity(vectorized_answers_count, user_answers_count)
        tfidf_similarity_scores = cosine_similarity(vectorized_answers_tfidf, user_answers_tfidf)

        nlp = spacy.load("en_core_web_lg")  # Load the larger spaCy model with word vectors
        syntactical_similarity_scores = []
        for answer, user_answer in zip(answers, user_answers):
            answer_doc = nlp(answer[0])
            user_answer_doc = nlp(user_answer)
            syntactical_similarity = answer_doc.similarity(user_answer_doc)
            syntactical_similarity_scores.append(syntactical_similarity)

        return co_occurrence_similarity_scores_count, tfidf_similarity_scores, syntactical_similarity_scores

    def generate_answers(questions, text):
        answers = []
        sentences = re.split(r'\.\s*', text)  # Split text into sentences

        for question in questions:
            question_text = question.split('?')[0].strip()  # Remove the question mark
            question_words = word_tokenize(question_text.lower())

            # Extract key phrase from the question
            key_phrase = ' '.join(
                [word for word in question_words if word not in ['what', 'is', 'the', 'main', 'idea', 'of', 'text']])

            matching_sentence = None

            # Find sentence that contains the key phrase
            for sentence in sentences:
                if key_phrase.lower() in sentence.lower():
                    matching_sentence = sentence
                    break

            # Append matching sentence as the answer, or "No relevant information found" if no match is found
            if matching_sentence:
                answers.append(matching_sentence)
            else:
                answers.append("No relevant information found.")

        vectorizer = TfidfVectorizer()
        vectorized_answers = vectorizer.fit_transform(answers)

        return list(zip(answers, vectorized_answers))

    gen_answers = generate_answers(quest, user_text)
    answers_list = [answer for answer, _ in gen_answers]
    vectorizer.fit([answer for answer, _ in gen_answers])

    similarity_score = 0
    count = 0
    score_ = []
    sc = 0
    for i, (generated_answer, user_answer) in enumerate(zip(gen_answers, user_answers)):
        generated_answer_text, generated_answer_vector = generated_answer
        user_answer_vector = vectorizer.transform([user_answer])
        score_.append(round(cosine_similarity(generated_answer_vector, user_answer_vector)[0][0] * 5, 2))
        sc = sc + round(cosine_similarity(generated_answer_vector, user_answer_vector)[0][0] * 5, 2)
        similarity_score = similarity_score + cosine_similarity(generated_answer_vector, user_answer_vector)[0][0]
        count = count + 1
    sc=round(sc)
    similarity_score = round((similarity_score / count) * 100)

    checkbox_value = request.form.get('checkbox', 'off')
    if checkbox_value == 'on':
        quest_string = "\n\n".join(quest)
        gen_answers_string = "\n\n".join(answers_list)
        user_ans_string = "\n\n".join(user_answers)
        email = request.form.get('email')
        recipients = [email]
        email_body = (f"GENERATED QUESTIONS\n-------------------\n{quest_string}\n\nGENERATED "
                      f"ANSWERS\n-------------------\n{gen_answers_string}\n\nYOUR ANSWERS\n-------"
                      f"------------\n{user_ans_string}")

        mail.send_message("ASQAG",
                          sender='asqag.cutm@gmail.com',
                          recipients=recipients,
                          body=email_body
                          )
    return render_template('greet.html', sc=sc, s=similarity_score, score=score_, count=count, gen_answers=gen_answers,
                           user_answers=user_answers)


app.run()