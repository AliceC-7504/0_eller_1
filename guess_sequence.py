from functions import maxSeq, seqs

class Sequence_guesser():
    def __init__(self, filepath):
        file = open(filepath, 'r')
        input = file.readline()
        '''
        self.sequence = input[:5]
        self.correction = input[5:]
        '''
        self.sequence = input[:len(input) // 2] # Sequence to be analysed
        self.correction = input[len(input) // 2:] # Sequence used to determine correctness of guesses
        
        
        self.correct_frequency = [0, 0] # Keeps track of guess correctness. Index 0: amount of correct guesses, index 1: incorrect
        self.correct_expectation = 0 # Amount of guesses the model expects to have correct
        self.amount_guesses = 0 # Amount of guesses that have been made
    
    def guess_next(self, method):       
        # Use method 1 or two in order to calculate the probability that next number is 0
        if method == 1:
            probability = self.probability_last_five()
        elif method == 2:
            # Determine current streak
            streak = 0
            current = self.sequence[-1]
            while current == self.sequence[-1]:
                streak += 1
                if streak < len(self.sequence):
                    current = self.sequence[-1 - streak]
                else:
                    current = -1
            probability = self.probability_streak(streak)     
        
        # Guess 0 or 1 depending on probability
        if probability >= 0.5:
            guess = '0'
        else:
            guess = '1'
        
        self.correct_expectation += max(probability, 1 - probability)
        self.amount_guesses += 1
        
        # Determine if guess was correct
        if guess == self.correction[0]:
            self.correct_frequency[0] += 1
        else:
            self.correct_frequency[1] += 1
        
        # Add answer to sequence to be analysed, and remove answer from correction sequence
        self.sequence = self.sequence + self.correction[0]
        self.correction = self.correction[1:]
     
    # Return probability that next number is 0, method 1       
    def probability_last_five(self):
        # Get subsequence of last few numbers
        last_chars = self.sequence[len(self.sequence) - 5:]
        while last_chars not in self.sequence[:-1]:
            last_chars = last_chars[1:]
        
        frequency = [0, 0] # Frequency of 0s (index 0) and 1s (index 1) after the last_chars substring
        index = 0
        started = False
        while index != -1:
            # Find index of next subsequence
            if started:
                index = self.sequence.find(last_chars, index + 1)
            else:
                index = self.sequence.find(last_chars, index)
                started = True
            if index != -1: # If index != -1, then subsequence exists in string
                frequency[int(self.sequence[min(index + len(last_chars), len(self.sequence) - 1)])] += 1
        return frequency[0] / (frequency[0] + frequency[1]) # return probability that next num is 0
    # Return probability that next number is 0, method 2
    def probability_streak(self, streak):
        sequences = seqs(self.sequence) # List containing amount of each streak length that appears in sequence
        index = streak
        change = sequences[index - 1] # Amount of times a streak of size streak is interrupted (i.e the number gets switched)
               
        if len(sequences) > index:
            stay = sequences[index]
        else:
            stay = 0

        stay = 0 # Variable for amount of times a streak of size streak is continued (i.e stay on same number)
        while index < len(sequences):
            stay = stay+sequences[index]
            index += 1

        if self.sequence[-1] == '1':
            return change / (change + stay)
        elif self.sequence[-1] == '0':
            return stay / (change + stay)
    
    # Returns % correct guesses
    def report_correctness(self):
        return (self.correct_frequency[0] / (self.correct_frequency[0] + self.correct_frequency[1])) * 100
    # Returns % expected correctness
    def report_correctness_expectation(self):
        return (self.correct_expectation / self.amount_guesses) * 100

sequence_guesser = Sequence_guesser('sequence.txt') # Replace with filepath to sequence
while sequence_guesser.correction != "":
    sequence_guesser.guess_next(2) # Use argument 1 or 2 depending on which model should be used

print("Correctness: " + str(sequence_guesser.report_correctness()) + ' %')
print("Expectation: " + str(sequence_guesser.report_correctness_expectation()) + ' %')
