import hangman_helper
import string

def update_word_pattern(word,pattern,letter):
    """The function receives a word, a pattern and a letter and returns the an
    updated pattern containing the letter."""
    if letter in word:
        new_pattern=[]
        for j in range(len(pattern)):
            new_pattern.append(pattern[j])
        pattern=""
        for i in range(len(word)):
            if word[i]==letter:
                new_pattern[i]=letter
            pattern += new_pattern[i]
    return pattern

def run_single_game(words_list):
    """This function recieves a list of words and after choosing a random
    word out of the list, runs each stage of the game, based on the players
    interactive inputs."""
    new_word = hangman_helper.get_random_word(words_list)
    wrong_guesses = []
    error_count=0
    new_pattern = "_"*len(new_word)
    msg = hangman_helper.DEFAULT_MSG
    while("_" in new_pattern and error_count < hangman_helper.MAX_ERRORS):
        #here start each round of the game, based on the player's guesses.
        hangman_helper.display_state\
            (new_pattern,error_count,wrong_guesses,msg,ask_play=False)
        guess = hangman_helper.get_input()
        if guess[0] == hangman_helper.LETTER:
            if guess[1] not in string.ascii_lowercase or len(guess[1]) != 1:
                msg = hangman_helper.NON_VALID_MSG
            elif guess[1] in new_pattern or guess[1] in wrong_guesses:
                msg = hangman_helper.ALREADY_CHOSEN_MSG + guess[1]
            elif guess[1] in new_word:
                new_pattern = update_word_pattern\
                    (new_word,new_pattern,guess[1])
                msg = hangman_helper.DEFAULT_MSG
            else:
                error_count +=1
                wrong_guesses.append(guess[1])
                msg = hangman_helper.DEFAULT_MSG
        elif guess[0] == hangman_helper.HINT:
            hint_letter = choose_letter\
                (filter_words_list(words_list,new_pattern,wrong_guesses),\
                 new_pattern)
            msg = hangman_helper.HINT_MSG + hint_letter
    if new_word == new_pattern:
        msg = hangman_helper.WIN_MSG
    else:
        msg = hangman_helper.LOSS_MSG + new_word
    hangman_helper.display_state\
        (new_pattern,error_count,wrong_guesses,msg,True)

def main():
    """This function loads a lists of words and uses that list in order to
     start a new game. At the end of the game asks if the player wants to start
    a new game or not, and proceeds suitable with the player's choice"""
    new_words_list = hangman_helper.load_words()
    run_single_game(new_words_list)
    wants_to_play = hangman_helper.get_input()
    while wants_to_play[1] == True:
        run_single_game(new_words_list)
        wants_to_play = hangman_helper.get_input()

def count_in_word(letter,word):
    """This function receives a letter and a word/string.
    If the string includes the letter the function will return 'True'
    otherwise it will return 'False'.
    This function will help shorten other functions"""
    mone=0
    for i in range(len(word)):
        if letter == word[i]:
            mone +=1
    return mone

def filter_words_list(words,pattern,wrong_guess_lst):
    """This function receives a list of words, a given pattern and
    a list of wrong letters guessed, and returns a new list which is
    equivalent to the original list, but without any words which don't fit the
    pattern nor include any letter from the wrong guesses list."""
    filtered_words = []
    for i in range(len(words)):
        should_add_word = True
        if len(words[i]) != len(pattern):
            continue
        for j in range(len(words[i])):
            if words[i][j] in wrong_guess_lst:
                should_add_word = False
                break
            if pattern[j] != '_':
                if pattern[j] != words[i][j]:
                    should_add_word = False
                    break
                if count_in_word(words[i][j], words[i]) != count_in_word\
                            (words[i][j], pattern):
                    should_add_word = False
                    break
        if should_add_word == True:
            filtered_words.append(words[i])
    return filtered_words

def choose_letter(words,pattern):
    """This function receives a list of words and a pattern and return returns
    the letter which has the maximum showings within the list, as long as it is
    not already within the given pattern."""
    letters_count = []
    max_letter = ""
    momentary_max = 0
    for character in range(len(string.ascii_lowercase)):
        letters_count.append(0)
    for i in range(len(words)):
        for j in range(len(words[i])):
            if words[i][j] not in pattern:
                letters_count[string.ascii_lowercase.index(words[i][j])] +=1
    for k in range(len(letters_count)):
        if letters_count[k] > momentary_max:
            max_letter = string.ascii_lowercase[k]
            momentary_max = letters_count[k]
    return max_letter

if __name__ == "__main__":
    # Here Hangman window is opened and a new game begins:
    hangman_helper.start_gui_and_call_main(main)
    #Here Hangman window will be closed:
    hangman_helper.close_gui()






