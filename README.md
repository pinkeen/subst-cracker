# Substitution cipher cracker (POC)

Uses a genetic algorithm with diphone frequency analysis. 

A ~1000 letter ciphertext is needed for best results.

Only polish frequency tables included.

## Usage

**All applications expect and output UTF-8 text.**

* `subst.py <enc|dec> <key file>`
Encodes/decodes text using key from "key file".
Feed text/ciphertext to stdin.

* `keygen.py`
Generates a random key and saves it to "random_key.txt"

* `test.py`
Generates a radom key, encodes the text fed to stdin
with it and tries to crack it. Upon era's completion
or receiving SIGINT it compares found keys to the correct
one and displays how many letters were cracked correctly.

* `crack.py`
Tries to decrypt the ciphertext. Just feed the text to stdin.

With the current (included) polish language stats it was
able to crack >20 characters in 1500 iterations when using 
a 1000+ character text.

PS If you have gnuplot use plot_test_stats.sh to get nice looking
graph of the fitness values in the ongoing cracking process. 
I do not force file buffer flushing so refresh the graph only
once in a while.

## Algo details

Defnitions:

* *cTXT* - ciphertext
* *dec(TXT, K)* - decrypt TXT with key K
* *smST* - single letter model statistics
* *dmST* - double letter model statistics
* *sstats(TXT)* - count single letter statistics
* *dstats(TXT)* - count double letter statistics
* *pcorr(ST1, ST2)* - pearsons sample correlation between statistics ST1 and ST2

Steps:

1. Take key X from current population.
2. dpTXT = dec(cTXT, X)
3. ssST = sstats(dpTXT), dsST = dstats(dpTXT)
4. fitness = (pcorr(ssST, smST) + pcorr(dmST, dsST)) * 50

Mutation is just a number of letter swaps within the key.
Crossover operator produces a valid keys and is "smart" -
uses single letter model stats in the process to speed up
convergence.

I decided not to use the dictionary checking. The module
is left there for educational purposes only ;).
It is also better to start with random keys rather
then with the naive key.

Naive key computation:
```python
for i to length(alphabet)
	a = letter which has the maximum occurence in ciphertext
	b = letter which has the maximum occurence in model stats
	add "b -> a" to the key and remove a and b from their stacks
```
	
There's probably room for more improvements, refining 
the parameters of the pool, etc. but I spent enough time
on this.
