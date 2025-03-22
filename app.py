from flask import Flask, render_template,request,jsonify,session
from keyword1 import match_keywords
from text_sum1 import summarize_text
from int import predict_intent
from sent import predict_sentiment
import joblib
import os


# Create a Flask app
app = Flask(__name__, template_folder="templates")

# Generate a secret key
secret_key = os.urandom(24)
app.secret_key = secret_key

# Define conversation states
SENTIMENT_DETECTION = "SENTIMENT_DETECTION"
DISORDER_DETECTION = "DISORDER_DETECTION"
INTENTION_DETECTION = "INTENTION_DETECTION"
CONFIRMATION_RESPONSE = "CONFIRMATION_RESPONSE"

# Global variables to keep track of conversation state
conversation_state = SENTIMENT_DETECTION
sentiment_detected = False
model_summary = None
sentiment = None
disorder_keywords = None
intention = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/chatui')
def chatui():
    return render_template('chatui.html')

def process_user_input(user_input):
    global model_summary, sentiment, disorder_keywords, intention
    # Function to process user input
    model_summary = summarize_text(user_input)
    sentiment = predict_sentiment(model_summary)
    disorder_keywords = match_keywords(model_summary)
    intention = predict_intent(model_summary)

@app.route('/process_input', methods=['POST'])
def process_input():
    global conversation_state, sentiment_detected, model_summary, sentiment, disorder_keywords, intention
    
    user_prompt = request.json.get('user_prompt')
    user_name = extract_name(user_prompt)
    introduction_words = ["hello", "hi", "hey", "howdy"]
    
    # Check if any introduction word is present in the user input
    if any(word in user_prompt.lower() for word in introduction_words):
        if user_name:
            bot_response = {"message": f"Hello, {user_name}! How can I assist you today?"}
        else:
            bot_response = {"message": "Hello! How can I assist you today?"}
        return jsonify(bot_response)

    print("Current conversation state:", conversation_state)
    
    # Process user input
    process_user_input(user_prompt)
    
    # Check if sentiment is detected
    if conversation_state == SENTIMENT_DETECTION:
        if sentiment:
            sentiment_detected = True
            if sentiment:
                if sentiment_detected:
                    if sentiment:
                        if sentiment == "joy":
                            bot_response = {'message': "That's fantastic! What's making you so happy?"}
                        elif sentiment in ["fear", "anger", "disgust"]:
                            bot_response = {'message': f"Sounds like you're feeling {sentiment}. What's going on?"}
                        elif sentiment in ["sad", "shame", "guilt"]:
                            bot_response = {'message': "It sounds like you're going through a rough time. What's bugging you?"}
                        else:
                            bot_response = {'message': "Sorry, I couldn't understand your sentiment. Can you provide more details?"}
                        print("Response based on sentiment:", bot_response)
                        conversation_state = DISORDER_DETECTION
                        return jsonify(bot_response)

    # Check if disorder keywords are detected
    if conversation_state == DISORDER_DETECTION:
        if disorder_keywords:
            if "Depression" in disorder_keywords:
                bot_response = {"message": "Sometimes things feel overwhelming. Have you experienced that lately?"}
            elif "Anxiety" in disorder_keywords:
                bot_response = {"message": "We all face worries. What's been on your mind recently?"}
            elif "PTSD" in disorder_keywords:
                bot_response = {"message": "Difficult experiences can leave a mark. Have you ever been through something challenging?"}
            elif "ADHD" in disorder_keywords:
                bot_response = {"message": "Focusing can be tricky! What kind of things distract you the most?"}
            elif "Eating disorder" in disorder_keywords:
                bot_response = {"message": "Our relationship with food is important. How's yours been lately?"}
            else:
                bot_response = {'message': "I couldn't identify any specific keywords. How can I assist you further?"}
            print("Response based on disorder keywords:", bot_response)
            conversation_state = INTENTION_DETECTION
            return jsonify(bot_response)
    
    # Check if intention is detected
    if conversation_state == INTENTION_DETECTION:
        if intention:
            if intention == "expressing distress":
                bot_response = {"message": "It sounds like you're going through a rough time. What's bugging you? I'm here to listen without judgement."}
            elif intention == "asking for resource":
                bot_response = {"message": "Absolutely! Here are some resources that might be helpful: [List of helplines and support groups in India for teens categorized by potential disorder]"}
            elif intention == "seeking advice":
                if 'Depression' in disorder_keywords:
                    bot_response = {"message": '''Hey there, friend! Feeling a bit blue? It happens to the best of us, but don't worry—I've got some awesome self-care tips that'll have you feeling like a sunshine superhero in no time! ☀️ Check it out:
                                \nSweet Dreams: Getting enough Zzz's is like hitting the reset button for your brain! Aim for a solid 7-9 hours of sleep each night to keep your mood and energy levels on point.
                                \nNom Nom Nutrition: Fuel up with foods that make you feel like a million bucks! Load up on fruits, veggies, whole grains, and lean proteins to keep your body and mind in tip-top shape.
                                \nMove Your Groove: Exercise isn't just good for your bod—it's a total mood booster too! Whether it's dancing like nobody's watching or going for a walk in nature, find what moves you and go for it!
                                \nChillaxation Station: Stress got you down? Time to chillax! Try deep breathing exercises, meditation, or just kicking back with your favorite tunes to help melt away those worries.
                                \nSocial Butterfly: Connect with your tribe and spread those good vibes! Whether it's a virtual hangout or a socially distanced stroll with a friend, spending time with the people you love can do wonders for your mood.
                                \nHobby Time: Find what makes your heart sing and dive in headfirst! Whether it's painting, gaming, or strumming your guitar, hobbies are like soul food for your spirit.
                                \nRemember, it's okay to not be okay sometimes. But with a little self-love and these awesome self-care tips, you've got everything you need to shine bright like the star you are! ✨'''}
                elif "Anxiety" in disorder_keywords:
                    bot_response = {"message":'''Hey there! Feeling a bit overwhelmed? Totally normal, but let's tackle this anxiety together. 🌟 When things start feeling too intense, remember these chill tricks:
                                \nDeep Breathing: Take a deep breath in through your nose for 4 counts, hold it for 4, then slowly exhale through your mouth for 6. Repeat a few times. It's like hitting the reset button for your brain!
                                \nMeditation: Ever tried it? It's not just for monks! Find a comfy spot, close your eyes, and focus on your breath or a calming image. Even just a few minutes can help clear your mind and calm those racing thoughts.
                                \nRemember, it's okay to feel anxious sometimes. But with these little relaxation hacks, you've got some superpowers to help you chill out whenever you need. You got this! 🌈'''}
                elif "PTSD" in disorder_keywords:
                    bot_response = {"message":'''Hey, I'm here for you. Dealing with tough stuff like PTSD can feel super overwhelming, but you're not alone, okay? 💪 It might feel scary, but reaching out to a pro can make a world of difference:
                                \nTherapist Time: Think of them as your personal mind ninja! Therapists are awesome at helping you work through tough stuff like trauma. They're like a super safe space where you can share whatever's on your mind, without judgment.
                                \nIt might feel like a big step, but taking care of your mental health is just as important as your physical health. Plus, talking it out with someone who knows their stuff can really help lighten the load. You've totally got this! 🌟'''}
                elif "ADHD" in disorder_keywords:
                    bot_response = {"message":'''Hey, friend! Dealing with ADHD can sometimes feel like herding cats, right? But don't sweat it—we've got some tricks up our sleeves to help you stay on track! 🚀 Check these out:
                                \nRockin' Routines: Think of routines like your personal superhero cape. They keep things predictable and make it easier to stay focused. Try setting a regular schedule for things like homework, meals, and bedtime. Once you get into the groove, it'll feel like second nature!
                                \nTo-Do Lists FTW: Picture this: You're crushing your day like a boss, crossing things off your to-do list left and right. Feels pretty awesome, huh? Jot down your tasks and goals, and break 'em into bite-sized chunks. It's like your roadmap to success!
                                \nWith these supercharged strategies, you'll be owning your ADHD like a pro in no time. You've got this, rockstar! 🌟'''}
                elif "Eating disorder" in disorder_keywords:
                    bot_response = {"message":'''Hey there, warrior! Battling with eating stuff can be tough, but I'm here to help you navigate through it like a champ. Here are some self-care tips that'll have you feeling strong and unstoppable:
                                \nRegular Meals: Think of meals as your fuel stops on the road to awesomeness! Aim for regular, balanced meals throughout the day to keep your energy levels steady and your body fueled up for whatever adventures come your way.
                                \nMindful Eating: Picture this: You're savoring every bite of your favorite snack, fully present in the moment. That's what mindful eating's all about! Take your time, pay attention to how your body feels, and honor your hunger and fullness cues.
                                \nPro Guidance: You're not alone in this battle! Sometimes, a little extra backup from a pro can make all the difference. Consider reaching out to a therapist or nutritionist who specializes in eating stuff. They've got your back!
                                \nRemember, taking care of yourself is the ultimate act of bravery. You're a rockstar, and I believe in you! 💪'''}
                else:
                    bot_response = {"message": "Okay, let's explore some ways to cope. What emotion are you feeling most right now?"}
            else:
                bot_response = {"message": 'So, how are things going overall?'}
            print("Response based on intention:", bot_response)
            conversation_state = CONFIRMATION_RESPONSE
            return jsonify(bot_response)

    # Check for confirmation response
    if conversation_state == CONFIRMATION_RESPONSE:
        l1 = model_summary.lower().split()
        cnf = ['yes', 'sure', 'okay']
        res = any(word in l1 for word in cnf)

        if res:
            if "Depression" in disorder_keywords:
                bot_response = {"message": "Stay strong, my friend. Remember, storms don't last forever, and there's always a rainbow waiting on the other side. Until next time, take care and keep being the amazing person you are! 💫"}
            elif "Anxiety" in disorder_keywords:
                bot_response = {"message": "Hang in there, champ! Anxiety might be knocking on your door, but you've got the power to show it who's boss. Keep breathing, keep believing, and keep shining. Until next time, take care and know that brighter days are ahead! 🌈"}
            elif "PTSD" in disorder_keywords:
                bot_response = {"message": "You're a warrior, facing battles no one else can see. It's okay to feel overwhelmed, but remember, you're stronger than you think. Take it one step at a time, and know that healing is possible. Until next time, stay brave and know that brighter days are on the horizon! 🌟"}
            elif "ADHD" in disorder_keywords:
                bot_response = {"message": "Your uniqueness is your superpower. Embrace your quirks, stay focused on your goals, and never forget how amazing you truly are. Until next time, keep shining bright and rocking that ADHD pride! 💥"}
            elif "Eating disorder" in disorder_keywords:
                bot_response = {"message": "To my incredible warriors battling eating disorders, I see your strength and resilience. Every step forward, no matter how small, is a victory worth celebrating. Keep nourishing your body, mind, and soul with love and compassion. Until next time, stay strong and know that you are worthy of every good thing life has to offer! 💖"}
            else:
                bot_response = {"message": "*Disclaimer:* I'm not a medical professional, but if you're experiencing symptoms, it's important to seek help from a doctor or therapist."}
        else:
            bot_response = {'message': f'''Thank you for reaching out. I hope you feel better soon. Here are some additional resources that might be helpful:<br>
                    Arpita Suicide Prevention Helpline<br>
                    - Description: Arpita Suicide Prevention Helpline located at Ramaiah Hospital is one of the services of Arpita Foundation, started in 2019 by a group of Experienced Volunteers from various Institutions to reach out to those in need.<br>
                    - Helpline Number: 080-23655557<br>
                    - Time: 10:00 AM - 01:00 PM | 02:00 PM - 05:00 PM | Monday to Friday<br>
                    - Languages: English, हिंदी, اردو, ಕನ್ನಡ, தமிழ், తెలుగు, മലയാളം, कोंकणी, অহমিয়া, ગુજરતી, বাংলা<br>
                    - Email: arpita.helpline@gmail.com<br><br>
                    Vandrevala Foundation<br>
                    - Description: Cyrus & Priya Vandrevala Foundation is a non-profit organisation that aims to provide significant funding and aid contributions for those suffering from mental health problems and illnesses in India.<br>
                    - Helpline Number: 9999 666 555<br>
                    - Time: 24x7 | All days of the week<br>
                    - Languages: English, हिंदी, ગુજરતી, বাংলা, ಕನ್ನಡ, தமிழ், తెలుగు, മലമലയായാളം, ଓଡ଼ିଆ, मराठी, తుళం<br>
                    - Email: help@vandrevalafoundation.com<br>
                    - Website: <a href="https://www.vandrevalafoundation.com">https://www.vandrevalafoundation.com</a>'''}
        print("Confirmation response:", bot_response)
        conversation_state = SENTIMENT_DETECTION
        return jsonify(bot_response)

    # If none of the above conditions are met, return a default response
    bot_response = {"message": "I'm sorry, I couldn't understand your input. Can you please provide more details?"}
    return jsonify(bot_response)


def extract_name(user_input):
    # Extract name from the user's input if it follows a certain pattern
    user_input = user_input.lower()
    if 'i am' in user_input:
        name_index = user_input.index('i am') + len('i am')
        name = user_input[name_index:].strip()
    elif 'my name is' in user_input:
        name_index = user_input.index('my name is') + len('my name is')
        name = user_input[name_index:].strip()
    else:
        name = None
    return name

if __name__ == '__main__':
    app.run(debug=True)
