import sys, json, numpy as np
import random
import json
from gtts import gTTS
import os 
import torch
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
    print(lines)
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
        print("I do not understand...")
    

    
#start process
if __name__ == '__main__':
    main()

