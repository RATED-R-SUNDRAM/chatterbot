import sys, json, numpy as np
import random
import json
from gtts import gTTS
import os 
import torch
import wikipedia
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])


def main():
    #get our data as an array from read_in()
    lines = read_in()
    if lines[:6]=="/start":
        print("WELCOME TO THE CHATBOT......")
        print()
        print("please spare some time in reading the instructions for smooth usage of me....")
        print()
        print("TRY WRITING YOUR QUERY IN FULL SENTENCES AND IF POSSIBLE TRY FINSIHING with 'in/at IIT MANDI' if ques is related to iit mandi ")
        print()
        print("TO GET ANSWERS FROM THE WEB ABOUT ANY TOPIC type '/gen' before the question to get a general response from the internet")
        print()
        print("IN CASE YOU ARE STILL STUCK TYPE '/help' TO GET THE RESOURCES WHERE YOU CAN FIND YOUR QUERIES")
    elif lines[:5]=="/help":
        print("Welcome to my help section.....")
        print()
        print("IF YOUR QUES IS RELATED TO PROGRAMMING THEN 'https://kamandprompt.zulipchat.com/' IS THE PLACE YOU CAN GET THE ANSWERS FROM OUR SENIORS")
        print()
        print("IF YOUR QUES IS RELATED TO ANY QUERY ABOUT IIT MANDI THEN 'https://wiki.iitmandi.co.in/p/Main_Page' IS THE PLACE WHERE ALL OF YOUR QUERIES WILL FIND A SOLUTION")
        print()
        print("IF YOU HAVE ANY QUERY ABOUT THE BOT CONTACT US AT 'https://github.com/mrkhan02/chatterbot/issues' ")
    elif lines[:4]=="/gen":
        print(wikipedia.summary(lines[4:], sentences = 4))
         

    else:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        with open('intents.json', 'r') as json_data:
            intents = json.load(json_data)
        FILE = "data.pth"
        data = torch.load(FILE)
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        all_words = data['all_words']
        tags = data['tags']
        model_state = data["model_state"]

        model = NeuralNet(input_size, hidden_size, output_size).to(device)
        model.load_state_dict(model_state)
        model.eval()

        bot_name = "VABAMS"

        sentence = lines
        sentence = tokenize(sentence)
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    mytext = random.choice(intent['responses'])
                    print(mytext)
                    
                    
        else:
            print("I am extremely sorry.... i didn't understood your question")
            print()
            print("Try /help for more help related to your query...")
    

    
#start process
if __name__ == '__main__':
    main()

