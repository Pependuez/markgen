# markgen

*Markov's chain generator*

Script markgen.py generates Markov's chan using external text files and use this chain to complete words sequences.

*Usage:*
    
    Learn mode:
        
        python markgen.py -l urls_file chain_order chain_file
            -l - flag for learn mode (building Markov's chain and save it to file)
            urls_file - file containing URLs to text files placed each on new string (string)
            chain_order - Markov's chain order (integer)
            chain_file - file to wite Markov's chain (string)

    Use mode:
        
        python markgen.py -u chain_file phrase_length word1 dord2 ...
            -u - flag for use mode (read Markov's chain from file and build the phrase)
            chain_file - file containing prebuilded Markov's chain (string)
            phrase_length - number of words in output sentence (integer)
            word1, word2, etc. - first words of sentence (stings)
