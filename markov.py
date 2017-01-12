import os
import sys
from random import choice
import twitter

# Sets api to consumer/access keys
api = twitter.Api(consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
                  consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
                  access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
                  access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


def open_and_read_file(filenames):
    """Given a list of files, open them, read the text, and return one long
        string."""

    body = ""

    for filename in filenames:
        text_file = open(filename)
        body = body + text_file.read()
        text_file.close()

    return body


def make_chains(text_string):
    """Takes input text as string; returns dictionary of markov chains."""

    chains = {}

    words = text_string.split()

    for i in range(len(words) - 2):
        key = (words[i], words[i + 1])
        value = words[i + 2]

        if key not in chains:
            chains[key] = []

        chains[key].append(value)

        # or we could replace the last three lines with:
        #    chains.setdefault(key, []).append(value)

    return chains


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""

    key = choice(chains.keys())  # randomly chooses a key from chains dict
    text = key[0] + " " + key[1]  # sets text to values 1 and 2 in tuple key

    while True:  # while text length is under 140
        word = choice(chains[key])  # randomly choosing from full list of words at value of key in chains
        temp_text = text + " " + word  # test variable so we can return to precvious var if length over 140
        if len(temp_text) > 140:  # if length of tweet is under 140 chars
            return text  # return previus state of tweet
        text += " " + word  # otherwise, add the word to the end
        key = (key[1], word)  # move key to next val

    return text


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    status = api.PostUpdate(make_text(chains))
    print status.text

    print ""
    user_choice = raw_input("Enter to tweet again [q to quit] >>> ")
    while user_choice != 'q':
        status = api.PostUpdate(make_text(chains))
        print status.text

        print ""
        user_choice = raw_input("Enter to tweet again [q to quit] >>> ")


# Get the filenames from the user through a command line prompt, ex:
# python markov.py green-eggs.txt shakespeare.txt
filenames = sys.argv[1:]

# Open the files and turn them into one long string
text = open_and_read_file(filenames)

# Get a Markov chain
chains = make_chains(text)

# Your task is to write a new function tweet, that will take chains as input
# tweet(chains)
tweet(chains)
