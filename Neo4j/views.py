from nltk.sentiment.vader import SentimentIntensityAnalyzer
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from nltk.tokenize import word_tokenize,sent_tokenize
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from gingerit.gingerit import GingerIt
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.cache import cache
from googletrans import Translator
from spacy.matcher import Matcher
from neomodel import DoesNotExist
from nltk.corpus import stopwords
from neomodel import Relationship
from django.conf import settings
from nltk.corpus import wordnet
from Neo4j.Data.kernel import *
from neo4j import GraphDatabase
from django.http import Http404
from neomodel import db,config
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode
from nltk.tag import pos_tag
from Neo4j.model import *
from neomodel import Q
from io import BytesIO
from PIL import Image
import pytholog as pl
from .models import *
from Neo4j import *
import pandas as pd
import random as ra
import dns.resolver
import geocoder
import requests
import binascii
import smtplib
import socket
import base64
import spacy
import nltk
import time
import aiml
import json
import uuid
import csv
import io
import os
import re

kb = pl.KnowledgeBase("KB")
nltk.download('punkt')
nltk.download('vader_lexicon') 
nltk.download('averaged_perceptron_tagger')
nlp = spacy.load('en_core_web_sm')

urdu_pattern = r'^[\u0600-\u06FF\s]+$'

debug_file_path = os.path.join(settings.BASE_DIR, 'debug_log.txt')

chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

image_path = os.path.join(settings.BASE_DIR, 'Neo4j/images', '1.png')

end = "Goodbye, take care!"
end1 = "until next time"
end2 = "Bye"
end3 = "Bye nice to meet you"
end4 = "Goodbye, take care!"
end5 = "Have a great day!"
end6 = "Bye Bye"
end7 = "See ya!"
end8 = "Bye for now!"
end9 = "Catch you later!"
list1 = [end,end1,end2,end3,end4,end5,end6,end7,end8,end9]

question_words = ["who", "what", "where", "when", "why", "how"]

r1 = "Great"
r2 = "Oh nice"
r3 = "Very good"
r4 = "Good"
r5 = "Nice"
r6 = "That's fantastic!"
r7 = "Awesome!"
r8 = "Impressive!"
r9 = "Excellent!"
r10 = "Terrific!"
list2 = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10]


def find_zodiac_sign(mon,day):
    month = mon
    day = day
    if month == 1:
        if day <= 19:
            sign = 'Capricorn'
        else:
            sign = 'Aquarius'
    elif month == 2:
        if day <= 18:
            sign = 'Aquarius'
        else:
            sign = 'Pisces'
    elif month == 3:
        if day <= 20:
            sign = 'Pisces'
        else:
            sign = 'Aries'
    elif month == 4:
        if day <= 19:
            sign = 'Aries'
        else:
            sign = 'Taurus'
    elif month == 5:
        if day <= 20:
            sign = 'Taurus'
        else:
            sign = 'Gemini'
    elif month == 6:
        if day <= 20:
            sign = 'Gemini'
        else:
            sign = 'Cancer'
    elif month == 7:
        if day <= 22:
            sign = 'Cancer'
        else:
            sign = 'Leo'
    elif month == 8:
        if day <= 22:
            sign = 'Leo'
        else:
            sign = 'Virgo'
    elif month == 9:
        if day <= 22:
            sign = 'Virgo'
        else:
            sign = 'Libra'
    elif month == 10:
        if day <= 22:
            sign = 'Libra'
        else:
            sign = 'Scorpio'
    elif month == 11:
        if day <= 21:
            sign = 'Scorpio'
        else:
            sign = 'Sagittarius'
    else:
        if day <= 21:
            sign = 'Sagittarius'
        else:
            sign = 'Capricorn'
    return sign


friend = "Knows"
friend1 = "Friend"
parent = "Parent" 
mother = "Mother"
father = "Father"
sib = "Sibling"
sis = "Sister"
bro = "Brother"
love = "Love"

pre_rep = init_kernel()
translator = Translator()

def lower_and_capitalize(string):
    lowercased_string = string.lower()
    capitalized_string = lowercased_string.capitalize()
    return capitalized_string


def define_word(word):
    synsets = wordnet.synsets(word)
    a = "No definitions found."
    if synsets:
        definition = synsets[0].definition()
        return definition
    else:
        return a


def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return synonyms


def get_ip(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address


def ip_to_email(request):
    user_mail = request.session.get('mail')
    ip1 = get_ip(request)
    octet = ip1[0:9]
    ip_all = IP.nodes.exclude(email=user_mail)
    for i in ip_all:
        if octet == i.ip[0:9]:
            return i.email
    return None


def name_get(request):
    user_mail2 = request.session.get('mail')
    email = ip_to_email(request)
    if email is not None:
        signup_obj = signups.nodes.all()
        signups_qs = signups.nodes.exclude(email= user_mail2)
        for i in signup_obj:
            if email == i.email:
                return i.username
    return None 


def get_data(user_email):
    user = signups.nodes.filter(email=user_email).first()
    if not user:
        return []
    chat = User_Chat.nodes.filter(email=user_email).first()
    if not chat:
        return []
    chat_data = chat.chat
    return chat_data


def error_404(request, exception):
    return render(request, '404.html', status=404)


def link_bot(request, user_email):
    user = signups.nodes.filter(email=user_email).first()
    bot = Bot_resp(email = user_email,name = "Bot_Resp").save()
    user.bot.connect(bot)


def link_ip_to_user(request, user_email, ip_address):
    user = signups.nodes.filter(email=user_email).first()
    ip_node = IP.nodes.filter(ip=ip_address, email=user_email).first()
    if not ip_node:
        ip_node = IP(ip=ip_address, email=user_email).save()

    if user.email == ip_node.email:
        user.has_ip.connect(ip_node)

    chat_node = User_Chat(email=user_email, name="Chats")

    if user_email and chat_node:
        chat_node.save()
        user.chats.connect(chat_node)
    return chat_node


def chat_store(request, message):
    user_mail2 = request.session.get('mail')
    chat_store_node = User_Chat.nodes.filter(email=user_mail2).first()
    if chat_store_node:
        chat_store_node.save_message(message)
    else:
        chat_store_node = User_Chat(email=user_mail2, name="Chats")
        chat_store_node.save_message(message)


def bot_store(request, message):
    user_mail2 = request.session.get('mail')
    resp = Bot_resp.nodes.filter(email=user_mail2).first()
    if resp:
        resp.save_message(message)
    else:
        resp = Bot_resp(email=user_mail2, name="Bot_Resp").first()
        resp.save_message(message)


def detect_person_and_noun_end(text1):
    q = text1.casefold()
    text = q.capitalize()
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        tagged_tokens = nltk.pos_tag(tokens)

        if tagged_tokens[0][1] == 'NNP' and tagged_tokens[-1][1] == 'NN' or tagged_tokens[0][1] == 'PRP' and tagged_tokens[-1][1] == 'NNP':
            return True
    
    return False


def detect_person_and_noun(text1):
    q = text1.casefold()
    text = q.capitalize()
    sentences = nltk.sent_tokenize(text)
    for sentence in sentences:
        tokens = nltk.word_tokenize(sentence)
        tagged_tokens = nltk.pos_tag(tokens)

        if tagged_tokens[0][1] == 'NNP' and tagged_tokens[-1][1] == 'NN':
            verb = None
            for token in tagged_tokens:
                if token[1].startswith('VB'):
                    verb = token[0]
                    break

            person_name = tagged_tokens[0][0]
            verb_in_middle = verb
            noun_at_end = tagged_tokens[-1][0]

            return person_name, verb_in_middle, noun_at_end
        
        elif tagged_tokens[0][1] == 'PRP' and tagged_tokens[-1][1] == 'NNP':
            verb = None
            for token in tagged_tokens:
                if token[1].startswith('VB'):
                    verb = token[0]
                    break

            person_name = tagged_tokens[-1][0]      
            verb_in_middle = verb
            noun_at_end = tagged_tokens[-2][0]

            return person_name, verb_in_middle, noun_at_end
    
    return None


def add_exclusion(request):
    user_mail2 = request.session.get('mail')

    node = Exclude.nodes.filter(email=user_mail2)

    if not node:
        new_exclusion = Exclude(email=user_mail2,names = "Data")
        new_exclusion.save()

        signup_node = signups.nodes.first_or_none(email=user_mail2)
        if signup_node is not None:
            new_exclusion.user.connect(signup_node)

        signups_with_email = signups.nodes.filter(email=user_mail2)
        for signup in signups_with_email:
            signup.excluded.connect(new_exclusion)


def link_memory(request):
    user_mail2 = request.session.get('mail')
    user = signups.nodes.filter(email=user_mail2).first()
    mem = Memory(email=user_mail2,name = "Episodic Memory").save()
    user.memory.connect(mem)


def generate_bot_response(request, user, bot):
    user_mail2 = request.session.get('mail')
    mem = Memory.nodes.filter(email=user_mail2, name="Episodic Memory").first()

    if not mem:
        mem = Memory(email=user_mail2, name="Episodic Memory").save()

    memory_store = mem.rel.single()
    if not memory_store:
        memory_store = MemoryStore(email=user_mail2).save()
        mem.rel.connect(memory_store)

    if memory_store:
        name = memory_store.name
        if name is None:
            name = "Episode 1"
            memory_store.name = name
            name_updated = True
        else:
            last_session_date = memory_store.end_session.date()
            current_date = datetime.today().date()

            if current_date > last_session_date:
                episode_number = int(name.split("Episode ")[1])
                next_episode_number = episode_number + 1
                name = "Episode " + str(next_episode_number)
                new_memory_store = MemoryStore(email=user_mail2, name=name).save()
                mem.rel.connect(new_memory_store)
                memory_store = new_memory_store
                name_updated = True
            else:
                name_updated = False

    if not memory_store.start_session:
        memory_store.start_session = datetime.now()

    memory_store.end_session = datetime.now()
    memory_store.sentiments = sentiment(request)
    memory_store.save_message("User", user)
    memory_store.save_message("Bot", bot)


def fetch_data(request):
    user_mail2 = request.session.get('mail')
    memory_store = MemoryStore.nodes.filter(email=user_mail2).first()
    chat_data = []
    
    if memory_store:
        if memory_store.memory_list:
            for entry in memory_store.memory_list:
                if entry.startswith("User:") and len(entry) > len("User:"):
                    chat_data.append(entry[len("User:"):].strip())

    return chat_data


def sentiment(request):
    sia = SentimentIntensityAnalyzer()
    chat_data = fetch_data(request)
    chat_text = ' '.join(chat_data)
    scores = sia.polarity_scores(chat_text)
    
    if scores['compound'] >= 0.05:
        bot_response = 'Positive sentiments'
    elif scores['compound'] <= -0.05:
        bot_response = 'Negative sentiments'
    else:
        bot_response = 'Neutral sentiments'
        
    return bot_response


def otp_gen():
    otp = ' '.join(ra.choice(chars) for _ in range(6))
    return otp


def correct_sentence(sentence):
    parser = GingerIt()
    result = parser.parse(sentence)
    corrected_sentence = result['result']
    return corrected_sentence


def get_name_nlp(previous_response):
    sentences = sent_tokenize(previous_response)
    tokens = word_tokenize(sentences[0])
    tagged_tokens = nltk.pos_tag(tokens)

    for tagged_token in tagged_tokens:
        if tagged_token[1] == 'NNP':
            name = tagged_token[0]
            break

    return name


def extract_first_noun(text):
    phrases = ["Define","DEFINE","define","def","Def"]
    for phrase in phrases:
        if text.startswith(phrase):
            # Remove the phrase and extract the remaining text
            remaining_text = text[len(phrase):].strip()
            tokens = nltk.word_tokenize(remaining_text)
            tagged_words = nltk.pos_tag(tokens)
            for word, tag in tagged_words:
                if tag.startswith('NN'):
                    return word
            break
    
    return None


def extract_last_word(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Iterate over the tokens in reverse order
    for token in reversed(doc):
        if not token.is_punct and not token.is_space:
            return token.text

    return None


def obj_relate(text1):
    text = text1.upper()
    tokens = word_tokenize(text)
    tagged_tokens = pos_tag(tokens)
    nouns = [word for word, pos in tagged_tokens if pos.startswith('NN')]
    verbs = [word for word, pos in tagged_tokens if pos.startswith('VB')]
    noun_str = ", ".join(nouns)
    verb_str = ", ".join(verbs)
    return noun_str, verb_str


def analyze_question(question):
    stop_words = set(stopwords.words('english')) - set(question_words)
    words = word_tokenize(question.lower())
    words = [word for word in words if not word in stop_words]

    if words[0] in question_words:
        tagged_words = nltk.pos_tag(words)
        subject = " ".join(word for word, pos in tagged_words if pos.startswith('NN'))
        return words[0], subject

    else:
        return None, None




def char_det(text):
    # text1 = text.split('.')
    # text = text1[0].capitalize()
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'NOUN', 'OP': '?'}, {'POS': 'VERB', 'OP': '?'}, {'POS': 'ADJ'}]
    matcher.add('POS_PATTERN', [pattern])
    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        matched_tokens = doc[start:end]
        adj_token = None
        noun_token = None
        for token in matched_tokens:
            if token.pos_ == 'ADJ':
                adj_token = token
                if token.head.pos_ == 'NOUN':
                    noun_token = token.head
                break
        if adj_token is not None and noun_token is not None:
            return True
        elif adj_token is not None:
            return True
        else:
            return False


def char_sep(text):
    text1 = text.split('.')
    text = text1[0].capitalize()
    matcher = Matcher(nlp.vocab)
    pattern = [{'POS': 'NOUN', 'OP': '?'}, {'POS': 'VERB', 'OP': '?'}, {'POS': 'ADJ'}]
    matcher.add('POS_PATTERN', [pattern])
    doc = nlp(text)
    matches = matcher(doc)
    for match_id, start, end in matches:
        matched_tokens = doc[start:end]
        adj_token = None
        noun_token = None
        for token in matched_tokens:
            if token.pos_ == 'ADJ':
                adj_token = token
                if token.head.pos_ == 'NOUN':
                    noun_token = token.head  # Retrieve the head noun of the adjective
                break
        if adj_token is not None:
            if noun_token is not None:
                return noun_token.text + ' ' + adj_token.text
            else:
                return adj_token.text
    return None


def detect_Has_have(text):
    doc = nlp(text)
    pronoun_found = False
    aux_found = False
    noun_found = False
    for token in doc:
        if token.pos_ == "PRON":
            pronoun_found = True
        elif token.pos_ == "VERB":
            aux_found = True
        elif token.pos_ == "NOUN":
            noun_found = True

    if pronoun_found and aux_found and noun_found:
        return True
    return False


def prolog_connection(request):
    user_mail2 = request.session.get('mail')
    rule = Prolog(email=user_mail2,name="Prolog").save()
    user = signups.nodes.filter(email =user_mail2).first()
    user.u.connect(rule)


def prolog_rule_gen(request, person1, person2, rel):
    user_mail2 = request.session.get('mail')
    pro = Prolog.nodes.filter(email=user_mail2).first() 
    fact = rel + "(" + person1 + "," + person2 + ")"
    if pro:
        pro.save_message(fact)
    else:
        Prolog(email=user_mail2, rule=[fact]).save()


def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    domain = email.split('@')[1]
    try:
        records = dns.resolver.resolve(domain, 'MX')
    except:
        return False

    for record in records:
        try:
            mx_server = str(record.exchange)
            smtp_socket = smtplib.SMTP(timeout=10)
            smtp_socket.connect(mx_server)
            smtp_socket.helo(socket.gethostname())
            smtp_socket.mail(email)
            code, message = smtp_socket.rcpt(str(email))
            smtp_socket.quit()
            if code == 250:
                return True
        except:
            pass
    return False


def mood_tell(request):
    user_mail2 = request.session.get('mail')
    sia = SentimentIntensityAnalyzer()
    chat_data = get_data(user_mail2)

    if not chat_data:
        return 'neutral'

    chat_text = ' '.join(chat_data)
    scores = sia.polarity_scores(chat_text)

    if scores['compound'] >= 0.05:
        sentiment = 'positive'
    elif scores['compound'] <= -0.05:
        sentiment = 'negative'
    else:
        sentiment = 'neutral'

    return sentiment


def history(request):
    user_mail2 = request.session.get('mail')
    try:
        memory_store = MemoryStore.nodes.get(email=user_mail2)
        messages = []
        episode_number = memory_store.name.split("Episode ")[1]
        start_session = memory_store.start_session
        end_session = memory_store.end_session

        for i, message in enumerate(memory_store.memory_list, start=1):
            if message.startswith("User:"):
                messages.append(f"{i}. User: {message.split('User: ')[1]}")
            elif message.startswith("Bot:"):
                messages.append(f"{i}. Bot: {message.split('Bot: ')[1]}")

        context = {
            'messages': messages,
            'episode_number': episode_number,
            'start_session': start_session,
            'end_session': end_session,
            'episode': range(1, int(episode_number) + 1)
        }

        return render(request, 'history.html', context)

    except:
        return render(request, 'no_history.html')


def get_user_location():
    response = requests.get('https://api.ipify.org?format=json')
    if response.status_code == 200:
        data = response.json()
        ip_address = data['ip']
        g = geocoder.ip(ip_address)
        if g.ok:
            return {
                'ip': ip_address,
                'country': g.country,
                'region': g.state,
                'city': g.city,
                'latitude': g.lat,
                'longitude': g.lng
            }

    return None


def forget(request):
    if request.method == 'POST':
        email_1 = request.POST['email']
        try:
            user = signups.nodes.get(email=email_1)
            name1 = user.username
            name = name1.capitalize()
            request.session['email_1'] = email_1
            otp = otp_gen()
            email_body = f"Dear {name},\n\nWe have received a request to change your account password.If you did not make this request, please contact our support team immediately at ahmadbilalssg@gmail.com.\n\nTo complete the password change, please use this OTP : {otp} to change your password.\nNote:Dont share this code with any one.\n\nIf you have any questions or need assistance, please contact our support team.\n\nThank you for using our service.\n\nBest regards,\n\nThe ChatBot(Dexter) Team"
            email_s = EmailMessage('ChatBot(Dexter) Password Change Request', email_body, 'ahmadbilalssg@gmail.com', [email_1])
            email_s.attach_file(image_path)
            email_s.send()
            request.session['otp'] = otp
            return redirect('forget2')
        except signups.DoesNotExist:
            return render(request, 'no_mail.html')
    return render(request, 'forget.html')


# @login_required(login_url = 'forget')
def forget2(request):
    if request.method =='POST':
        otp2 = request.POST['otp']
        otp = request.session.get('otp')
        otp3 = otp2.strip()
        if otp == otp3:
            return redirect('forget3')
        else:
            return render(request, 'otp_check.html')
    return render(request,'forget2.html')

# @login_required(login_url = 'forget')
def forget3(request):
    if request.method =='POST':
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if new_password == confirm_password:
            email_1 = request.session.get('email_1')
            if email_1 is not None:
                user_p = signups.nodes.get(email=email_1)
            else:
                user_mail2 = request.session.get('mail')
                user_p = signups.nodes.get(email=user_mail2)
                if user_p.password == new_password:
                    return HttpResponse('Dont enter previous password')
                else:
                    user_p.password = new_password
                    user_p.save()
                    return render(request,'password_success.html')
        else:
            return render(request,'password_unsuccess.html')
    return render(request,'forget3.html')


def vi(request):
    return render(request, "brain.html")


# @login_required(login_url='login')
def index(request):
    user_mail2 = request.session.get('mail')
    image_data = show_pic(request)
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    file = Main_Page_Content.objects.all()
    name =  signups.nodes.filter(email = user_mail2).first()
    a = name.username
    if len(a.split()) == 2:
        b = [part.lower().capitalize() for part in a.split()]
        x = ' '.join(b)
    elif len(a.split()) == 3:
        b = [part.lower().capitalize() for part in a.split()]
        x = ' '.join(b)
    else:
        b = a.lower()
        x = b.capitalize()
    context = {
        'file': file,
        'image_data': image_base64,
        'x': x
    }
    return render(request, 'index.html', context)


def signup(request):
    if request.method == 'POST':
        n = request.POST['username']
        m = request.POST['email']
        d = request.POST['date_of_birth']
        sp = request.POST['password']

        request.session['user_birth'] = d
        m = m.lower()
        date_of_birth1 = datetime.strptime(d, '%Y-%m-%d').date()

        if signups.nodes.filter(email=m): 
            return render(request, 'email_duplicate.html')
        elif not validate_email(m):
            return render(request, 'email_not.html')
        else:
            birth_year, birth_month, birth_day = map(int, d.split('-'))
            current_year = int(str(datetime.now().year)[:4])
            current_month = int(datetime.now().strftime('%m'))
            current_day = int(datetime.now().strftime('%d'))
            age = current_year - birth_year
            if birth_month > current_month:
                age -= 1
            elif birth_month == current_month and birth_day > current_day:
                age -= 1

            if age < 18:
                return render(request, 'age_restrict.html')

            signups(username=n.capitalize(),email=m,date_of_birth =date_of_birth1,password=sp,gender=predict_gender(n)).save()
            try:
                recipient_name1 = str(n)
                recipient_name = recipient_name1.capitalize()
                email_body = f"Dear {recipient_name},\n\nThank you for your interest in signing up for our platform! We are excited to have you onboard and we appreciate the opportunity to serve you.\n\nIf you encounter any issues during the registration process or have any questions, please dont hesitate to reach out to our customer support team at ahmadbilalssg@gmail.com.\n\nThank you again for choosing our platform. We look forward to working with you!\n\nBest regards,\n\n{recipient_name}"
                email_s = EmailMessage('Account Creation Request',email_body,'ahmadbilalssg@gmail.com',[m])
                email_s.attach_file(image_path)
                email_s.send()
            except:
                obj = signups.nodes.get(email=m)
                obj.delete()
                return redirect('signup')

            request.session['user_name'] = n
            request.session['user_age'] = age
            request.session['mail'] = m
            ip = get_ip(request)      
            ip_exists = IP.nodes.filter(email = m,ip=ip)
            if ip_exists:
                return redirect('index')
            else:
                ip_obj = IP(email=m,ip=ip).save()
                ii = get_ip(request)
                link_memory(request)
                add_exclusion(request)
                link_bot(request,m)
                link_ip_to_user(request , m ,ii )
                prolog_connection(request)
                return redirect('index')
    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['Password']
        if signups.nodes.filter(email=email, password=password):
            user = signups.nodes.get(email=email, password=password)
            name = user.username
            age1 = user.date_of_birth
            age = str(age1)
            request.session['user_birth'] = age
            birth_year, birth_month, birth_day = map(int, age.split('-'))
            current_year = int(str(datetime.now().year)[:4])
            current_month = int(datetime.now().strftime('%m'))
            current_day = int(datetime.now().strftime('%d'))
            age = current_year - birth_year
            if birth_month > current_month:
                age -= 1
            elif birth_month == current_month and birth_day > current_day:
                age -= 1
            request.session['user_name'] = name
            request.session['user_age'] = age
            request.session['mail'] = email
            now = datetime.now()
            current_time = now.time()
            hour = current_time.hour
            minute = current_time.minute
            second = current_time.second
            recipient_name1 = str(name)
            recipient_name = recipient_name1.capitalize()
            email_body = f"Dear {recipient_name},\n\nWe wanted to let you know that your account was recently accessed on {current_day} at {hour}:{minute}:{second}.\n\nIf you did not make this login attempt, please contact our support team immediately at ahmadbilalssg@gmail.com.\n\nThank you for using our service\n\nBest regards,\n\nThe ChatBot(Dexter) Team"
            ip = get_ip(request)
            ip_queryset = IP.nodes.filter(email=email, ip=ip)
            if ip_queryset:
                email_s = EmailMessage('Security alert',email_body,'ahmadbilalssg@gmail.com',[email])
                email_s.attach_file(image_path)
                email_s.send()
                return redirect('index')
            else:
                ip_obj = IP(email=email, ip=ip).save()
                email_s = EmailMessage('Security alert', email_body, 'ahmadbilalssg@gmail.com',[email])
                email_s.attach_file(image_path)
                email_s.send()

                return redirect('index')
        else:
            return render(request, 'no_mail_pass.html')  
    return render(request, 'login.html')


# @login_required(login_url = 'login')
def upload_pic(request):
    if request.method == 'POST':
        image = request.FILES['image']
        user_mail2 = request.session.get('mail')
        image_data = image.read()
        image_base641 = base64.b64encode(image_data).decode('utf-8')
        image_base64 = "data:image/png;base64," + image_base641
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))
        with driver.session() as session:
            session.run("MATCH (u:signups {email: $email}) SET u.image = $image",email=user_mail2, image=image_base64)
        
        return redirect('index')
    return render(request, 'picupload.html')


def show_pic(request):
    user_mail = request.session.get('mail')
    user = signups.nodes.get_or_none(email=user_mail)
    if user is None:
        return None
    else:
        image_data = user.image
        try:
            image_data = image_data.split(",")[1]
            image_data = base64.b64decode(image_data)
        except (IndexError, binascii.Error):
            image_data = None
        return image_data


# @login_required(login_url = 'login')
def contact(request):
    user_mail2 = request.session.get('mail')
    image_data = show_pic(request)
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    file = Main_Page_Content.objects.all()
    name = signups.nodes.filter(email=user_mail2).first()
    a = name.username
    if len(a.split()) == 2:
        b = [part.lower().capitalize() for part in a.split()]
        x = ' '.join(b)
    elif len(a.split()) == 3:
        b = [part.lower().capitalize() for part in a.split()]
        x = ' '.join(b)
    else:
        b = a.lower()
        x = b.capitalize()
    context = {
        'file': file,
        'image_data': image_base64,
        'x': x
    }
    if request.method == 'POST':
        l = request.POST['Name']
        m = request.POST['Gmail']
        p = request.POST['comment']

        Contact_Us.objects.create(Name=l, Gmail=m, comment=p)
    return render(request, 'index.html', context)


def about(request):
    data = About.objects.all()
    return render(request,'about.html',{'data':data})


def help(request):
    h = Help.objects.all()
    return render(request,'help.html',{'h':h})


# @login_required(login_url = 'login')
def chat(request):
    session_id = request.session.session_key
    user_mail2 = request.session.get('mail')
    name1 = request.session.get('user_name')
    name = name1.capitalize()
    user_birth = request.session.get('user_birth')
    user_age1 = request.session.get('user_age')
    age_str = str(user_age1)
    pre_rep.setPredicate('age', age_str)
    a = predict_gender(name)
    pre_rep.setPredicate('name', name)
    pre_rep.setPredicate('gender', a)
    pre_rep.setPredicate('birthday', user_birth)
    nike_name = request.session.get('nike_name') 
    year = user_birth[:4]
    month = user_birth[5:7]
    day = user_birth[8:]
    month, day = int(month), int(day)
    ziodic = find_zodiac_sign(month, day) 
    pre_rep.setPredicate('sign', ziodic)
    pre_rep.setPredicate('m', user_mail2)
    bot_name = "Ahmed Bilal Bhatti"
    pre_rep.setPredicate('master',bot_name)
    ip = get_ip(request)
    pre_rep.setPredicate('ip', ip)
    mood = mood_tell(request)
    pre_rep.setPredicate('mood', mood)
    location = get_user_location()
    if location:
        pre_rep.setPredicate('location', location['country'])
        pre_rep.setPredicate('region', location['region']) 
        pre_rep.setPredicate('city', location['city'])  
        pre_rep.setPredicate('latitude',location['latitude']) 
        pre_rep.setPredicate('longitude',location['longitude'])
    else:
        print("Failed to retrieve the user's location.")
    image_data = show_pic(request)
    image_base64 = base64.b64encode(image_data).decode('utf-8')
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        if  re.match(urdu_pattern, user_message):
            english = translator.translate(user_message).text
            response = pre_rep.respond(english)
            bot_response = translator.translate(response, dest='ur').text
            return JsonResponse({'bot_response': bot_response})
        elif user_message.startswith(("What is the gender of","Tell me the gender of","what is the gender of")):
            name = get_name_nlp(user_message)
            a = predict_gender(name)
            bot_response = a
            generate_bot_response(request,user_message,bot_response)
            bot_store(request, bot_response)
            return JsonResponse({'bot_response': bot_response})
        elif "have another" in user_message or "have one more" in user_message:
            sentences = user_message.split(".")
            first_sentence = sentences[0].strip()
            nouns, verbs = obj_relate(first_sentence)
            a = nouns
            request.session['item'] = a
            obj_node = Items(email=user_mail2, item_name=a).save()
            user = signups.nodes.filter(email=user_mail2).first()
            user.item1.connect(obj_node)
            bot_response = "Ok you have one more great"
            bot_store(request, bot_response)
            chat_store(request, user_message)
            generate_bot_response(request,user_message,bot_response)
            return JsonResponse({'bot_response': bot_response})
        elif user_message.startswith(("Define","DEFINE","define","def","Def")):
            a = extract_first_noun(user_message)
            x = define_word(a)
            if x == "No definitions found.":
                bot_response = get_completion(user_message)
            else:
                x += "\n\nSource: Wordnet"
                bot_response = x
            chat_store(request, user_message)
            generate_bot_response(request, user_message, bot_response)
            return JsonResponse({'bot_response': bot_response})
        elif "synonyms" in user_message.lower() or "synonym" in user_message.lower():
            a = extract_last_word(user_message)
            x = get_synonyms(a)
            x.append("Source: Wordnet")
            if len(x) > 14:
                last_words = x[-14:]
                last_words = [word.replace(',', '') for word in last_words]
                last_sentence = " ".join(last_words)
                x = x[:-len(last_words)]
                x.extend(last_words)
            bot_response = " ".join(x)
            chat_store(request, user_message)
            generate_bot_response(request, user_message, bot_response)
            return JsonResponse({'bot_response': bot_response})
        elif ("have" in (user_message := user_message.lower()) or "have a" in user_message) and ("dont have" not in user_message and "don't have" not in user_message):
            sentences = user_message.split(".")
            first_sentence = sentences[0].strip()
            nouns, verbs = obj_relate(first_sentence)
            try:
                obj_node = Items.nodes.filter(email=user_mail2, item_name=nouns).first()
                if obj_node:
                    bot_response = "Yes, I already know."
                    bot_store(request, bot_response)
            except:
                    obj_node = Items(email=user_mail2, item_name=nouns).save()
                    request.session['item'] = obj_node.item_name
                    user = signups.nodes.filter(email=user_mail2).first()
                    user.item.connect(obj_node)
                    bot_response = ra.choice(list2)
                    bot_store(request, bot_response)
            chat_store(request, user_message)
            generate_bot_response(request,user_message,bot_response)
            return JsonResponse({'bot_response': bot_response})
        elif detect_person_and_noun_end(user_message) == True:
            person_name, verb_middle, noun_end = detect_person_and_noun(user_message)
            noun_end = lower_and_capitalize(noun_end)
            noun_end1 = noun_end.upper()
            s = signups.nodes.filter(email=user_mail2).first()
            gen = predict_gender(person_name)
            if noun_end1 == "PARENT" or noun_end1 == "MOTHER" or noun_end1 == "FATHER":
                if gen == "Male":
                    fri = Friends(email=user_mail2, name=person_name, gender="Male").save()
                    prolog_rule_gen(request, person_name, name, father)
                    s.ff1.connect(fri)
                    bot_response = "Ok so he is your father Great"
                    bot_store(request, bot_response)
                    generate_bot_response(request, user_message, bot_response)
                    return JsonResponse({'bot_response': bot_response})
                else:
                    fri = Friends(email=user_mail2, name=person_name, gender="Female").save()
                    prolog_rule_gen(request, person_name, name, mother)
                    s.ff.connect(fri)
                    bot_response = "Ok so she is your mother Great"
                    bot_store(request, bot_response)
                    generate_bot_response(request, user_message, bot_response)
                    return JsonResponse({'bot_response': bot_response})
            elif noun_end1 == "FRIEND" or noun_end1 == "FRIENDS":
                fri = Friends(email=user_mail2, name=person_name, gender=gen).save()
                prolog_rule_gen(request, person_name, name, friend1)
                s.friend.connect(fri)
                bot_response = "So you know him well"
                bot_store(request, bot_response)
                generate_bot_response(request, user_message, bot_response)
                return JsonResponse({'bot_response': bot_response})
            elif noun_end1.lower() == "sibling" or noun_end1.lower() == "siblings" or noun_end1.lower() == "sister" or noun_end1.lower() == "brother":
                if gen == "Male":
                    fri = Friends(email=user_mail2, name=person_name, gender=gen).save()
                    prolog_rule_gen(request, person_name, name, bro) 
                    s.fr1.connect(fri)
                    bot_response = "So he is your Brother"
                    bot_store(request, bot_response)
                    generate_bot_response(request, user_message, bot_response)
                    return JsonResponse({'bot_response': bot_response})
                else:
                    fri = Friends(email=user_mail2, name=person_name, gender="Female").save()
                    prolog_rule_gen(request, person_name, name, sis) 
                    s.fr.connect(fri)
                    bot_response = "So she is your sister good"
                    bot_store(request, bot_response)
                    generate_bot_response(request, user_message, bot_response)
                    return JsonResponse({'bot_response': bot_response})
        elif char_det(user_message) is not None:
            noun = request.session.get('item')
            chat_node = User_Chat.nodes.filter(email=user_mail2).first()
            if chat_node:
                previous_messages = chat_node.chat
                phrases_to_check = ["have", "have a", "IT HAS", "IT'S", "ITS", "ALSO"]
                if len(previous_messages) >= 3:
                    previous_message3, previous_message, previous_message1, *_ = previous_messages[-5:]
                    if all(msg is not None for msg in [previous_message, previous_message1, previous_message3]) and any(phrase in msg for phrase in phrases_to_check for msg in [previous_message, previous_message1, previous_message3]):
                        ch = char_sep(user_message)
                        st = Charistics(email=user_mail2, item_char=ch).save()
                        pre_node = Items.nodes.filter(email=user_mail2, item_name=noun).first()
                        if pre_node:
                            pre_node.charistic.connect(st)
                        else:
                            Items(email=user_mail2, item_name=noun).save()
                        bot_response = ra.choice(list2)
                        bot_store(request, bot_response)
                        chat_store(request, user_message)
                        generate_bot_response(request, user_message, bot_response)
                        return JsonResponse({'bot_response': bot_response})
                elif len(previous_messages) == 2:
                    previous_message, previous_message1 = previous_messages[-2:]
                    if all(msg is not None for msg in [previous_message, previous_message1]) and any(phrase in msg for phrase in phrases_to_check for msg in [previous_message, previous_message1]):
                        ch = char_sep(user_message)
                        st = Charistics(email=user_mail2, item_char=ch).save()
                        pre_node = Items.nodes.filter(email=user_mail2, item_name=noun).first()
                        if pre_node:
                            pre_node.charistic.connect(st)
                        else:
                            Items(email=user_mail2, item_name=noun).save()
                        bot_response = ra.choice(list2)
                        bot_store(request, bot_response)
                        chat_store(request, user_message)
                        generate_bot_response(request, user_message, bot_response)
                        return JsonResponse({'bot_response': bot_response})
                elif len(previous_messages) == 1:
                    previous_message = previous_messages[-1]
                    if previous_message is not None and any(phrase in previous_message for phrase in phrases_to_check):
                        ch = char_sep(user_message)
                        st = Charistics(email=user_mail2, item_char=ch).save()
                        pre_node = Items.nodes.filter(email=user_mail2, item_name=noun).first()
                        if pre_node:
                            pre_node.charistic.connect(st)
                        else:
                            Items(email=user_mail2, item_name=noun).save()
                        bot_response = ra.choice(list2)
                        bot_store(request, bot_response)
                        chat_store(request, user_message)
                        generate_bot_response(request, user_message, bot_response)
                        return JsonResponse({'bot_response': bot_response})              
        else:
            if user_message.upper().startswith(("YES HE IS MY", "YES SHE IS MY", "YES THEY ARE MY")):
                bot = Bot_resp.nodes.filter(email=user_mail2).first()
                user = signups.nodes.filter(email=user_mail2).first()
                res = bot.responses
                if res:
                    pre = res[-1]
                    if any(phrase in pre for phrase in ["Do you know"]):
                        name = get_name_nlp(pre)
                        G = predict_gender(name)
                        a = Friends(email=user_mail2,name=name,gender=G).save()
                        if user_message.endswith("FRIEND"):
                            prolog_rule_gen(request, name, name1, friend1) 
                            user.friend.connect(a)
                            bot_response = pre_rep.respond(user_message)
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                        elif user_message.endswith("PARENT"):
                            prolog_rule_gen(request, name, name1, parent) 
                            user.friend1.connect(a)
                            bot_response = pre_rep.respond(user_message)
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                        elif user_message.endswith("SIBLINGS") or user_message.endswith("SIBLING"):
                            user.friend2.connect(a)
                            prolog_rule_gen(request, name, name1, sib)
                            bot_response = pre_rep.respond(user_message)
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                        elif user_message.endswith("BROTHER"):
                            prolog_rule_gen(request, name, name1, bro) 
                            user.fr1.connect(a)
                            bot_response = pre_rep.respond(user_message)
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                        elif user_message.endswith("SISTER"):
                            prolog_rule_gen(request, name, name1, sis) 
                            user.fr.connect(a)
                            bot_response = pre_rep.respond(user_message)
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                    else:
                        bot_response = "Who?"
                        return JsonResponse({'bot_response': bot_response})
                else:
                    bot_response = "What are you talking about"
                    return JsonResponse({'bot_response': bot_response})
            elif user_message.upper() in ("YES","NO"):
                if user_message == "YES":
                    bot = Bot_resp.nodes.filter(email=user_mail2).first()
                    user = signups.nodes.filter(email=user_mail2).first()
                    res = bot.responses
                    if res:
                        pre = res[-1]
                        if any(phrase in pre for phrase in ["Do you know"]):
                            name1 = get_name_nlp(pre)
                            G = predict_gender(name1)
                            a = Friends(email=user_mail2,name=name1,gender = G).save()
                            prolog_rule_gen(request, name, name1, friend)
                            user.frnd.connect(a)
                            bot_response = "So you know him good"
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                        else:
                            bot_response = "Ok"
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                    else:
                        bot_response = pre_rep.respond(user_message)
                        bot_store(request, bot_response)
                        generate_bot_response(request,user_message,bot_response)
                        return JsonResponse({'bot_response': bot_response})
                else:
                    bot_response = pre_rep.respond(user_message)
                    bot_store(request, bot_response)
                    generate_bot_response(request,user_message,bot_response)
                    return JsonResponse({'bot_response': bot_response})
            elif user_message.upper().startswith(("SEARCH FOR", "SEARCH ON WEB FOR", "WHAT WEB SAYS FOR", "SEARCH ON WIKIPEDIA FOR")):
                prefixes = ("SEARCH FOR", "SEARCH ON WEB FOR", "WHAT WEB SAYS FOR", "SEARCH ON WIKIPEDIA FOR")
                for prefix in prefixes:
                    if user_message.upper().startswith(prefix):
                        user_message = user_message[len(prefix):].strip()
                        break
                bot_response = web_scraping(user_message)
                if bot_response == "I'm sorry, I didn't understand what you said." or bot_response == "I'm sorry, I didn't understand what you said.":
                    bot_response = define_word(user_message)
                    if bot_response == "No definitions found.":
                        bot_response = get_completion(user_message)
                bot_store(request, bot_response)
                generate_bot_response(request, user_message, bot_response)
                return JsonResponse({'bot_response': bot_response})
            else:
                bot_response = pre_rep.respond(user_message)
                bot_store(request, bot_response)
                new_exclusion = Exclude.nodes.filter(email=user_mail2 ,names="Data").first()
                alln = E_names.nodes.filter(email=user_mail2)
                allnames = [node.names for node in alln]
                if bot_response == "I'm sorry, I didn't understand what you said." or bot_response.endswith("I didn't understand what you said."):
                    if name_get(request) is not None and name_get(request) not in allnames:
                        bot_response = "Do you know " + name_get(request)
                        excluded_names = E_names(email=user_mail2, names=name_get(request))
                        excluded_names.save()
                        new_exclusion.of.connect(excluded_names)
                        bot_store(request, bot_response)
                        generate_bot_response(request,user_message,bot_response)
                        return JsonResponse({'bot_response': bot_response})
                    else:
                        bot_response = web_scraping(user_message)
                        if bot_response == "I'm sorry, I didn't understand what you said.":
                            bot_response = get_completion(user_message)
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                        else:
                            bot_store(request, bot_response)
                            generate_bot_response(request,user_message,bot_response)
                            return JsonResponse({'bot_response': bot_response})
                else:
                    generate_bot_response(request,user_message,bot_response)
                    return JsonResponse({'bot_response': bot_response})
    else:
        if image_data:
            image_base64 = base64.b64encode(image_data).decode('utf-8')
        else:
            image_base64 = None

        return render(request, 'temp.html',{'image_data': image_base64, 'name': name})
    return render(request, 'temp.html',{'image_data': image_base64, 'name': name})


def web_scraping(qs):
    URL = 'https://www.google.com/search?q=' + qs
    
    answer = "I'm sorry, I didn't understand what you said."
    
    try:
        page = requests.get(URL)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')

        links = soup.findAll("a")
        all_links = []
        for link in links:
            link_href = link.get('href')
            if link_href is not None and "url?q=" in link_href and not "webcache" in link_href:
                all_links.append((link.get('href').split("?q=")[1].split("&sa=U")[0]))

        flag = False
        for link in all_links:
            if 'https://en.wikipedia.org/wiki/' in link:
                wiki = link
                flag = True
                break

        div0 = soup.find_all("div", class_="kvKEAb")
        div1 = soup.find_all("div", class_="Ap5OSd")
        div2 = soup.find_all("div", class_="nGphre")
        div3 = soup.find_all("div", class_="BNeawe iBp4i AP7Wnd")

        if len(div0) != 0:
            answer = div0[0].text[:250] + "..."
        elif len(div1) != 0:
            answer = div1[0].text[:250] + "..." + "\n" + div1[0].find_next_sibling("div").text[:250] + "..."
        elif len(div2) != 0:
            answer = div2[0].find_next("span").text[:250] + "..." + "\n" + div2[0].find_next("div", class_="kCrYT").text[:250] + "..."
        elif len(div3) != 0:
            answer = div3[1].text[:250] + "..."
        elif flag:
            try:
                page2 = requests.get(wiki, timeout=10)
                soup = BeautifulSoup(page2.text, 'html.parser')
                title = soup.select("#firstHeading")[0].text

                paragraphs = soup.select("p")
                for para in paragraphs:
                    if bool(para.text.strip()):
                        answer = title + "\n" + para.text[:250] + "..."
                        break
            except ConnectTimeout as e:
                answer = "Sorry. Wikipedia page connection timed out."
    except requests.exceptions.RequestException as e:
        answer = "Sorry. An error occurred while retrieving the data."

    print(f"Search Query: {qs}")
    print(f"Answer: {answer}")
    print(f"Source: {URL}")

    return answer


def get_completion(message):
    url = "https://free.churchless.tech/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    payload = {"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": message}]}
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if 'choices' in data and data['choices']:
        completion = data['choices'][0]['message']['content']
        return completion.strip()
    else:
        return "I'm sorry, I didn't understand what you said."