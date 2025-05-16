Exercise 1

Write an algorithm (using pseudocode or any known programming language) for the following computational tasks:

1) Given a matrix, print the element at (0,0).

2) Given a matrix, double all elements of its first row.

3) Given a matrix, double all elements of the entire matrix.

Analyze the (theoretical) time complexity of these three algorithms. If you wish, you can also test the empirical time complexity using the same method as shown during lectures (using Python libraries pandas, numpy and matplotlib).

Exercise 2

Consider the following time complexity functions:

1) 𝑇(𝑛)=2𝑛2−3𝑛+2

2) 𝑇(𝑛) = 3𝑛−7

3) 𝑇(𝑛)=2𝑛−1

4) 𝑇(𝑛)=2𝑛+2𝑛log𝑛

5) 𝑇(𝑛)=2𝑛2+2𝑛log𝑛

6) 𝑇(𝑛)=0.28𝑛+256

To which complexity classes do these time complexity functions belong? Justify your answer.

Exercise 3

Suppose it takes one second for your computer to put 1000 items in order.

How long does it take to order 10000 items, if the running time of the algorithm is about

a) 𝑛2

b) log2 𝑛 ?

Exercise 4

The leftmost column gives the expression for function 𝑇(𝑛), which describes the running time of the algorithm. The unit of 𝑇 is one microsecond. The top row gives the size of an input. Calculate the performance time for every algorithm (if possible) with given 𝑛. Convert the results to suitable units.

    10  1000    10 000  100 000
log2n
sqrtn
n
n²
n!

T = 1us

Exercise 5

Sort the following functions by their asymptotic rate of growth in increasing order.

HINT: It is not a bad idea to graph these functions…

𝑛2 log10 𝑛

2𝑛

100𝑛

50

log2 𝑛

𝑛0,5

Exercise 6

Which of the following tasks is

a) hardest to perform?

b) easiest to perform?

TASK 1: To find the greatest number of the unordered list of some integers.

TASK 2: To find the middle number when the integers are ordered from the smallest to the greatest.

Justify your answer.

Exercise 7

It is known that finding all possible permutations of a given set / string has complexity of 𝑛!

Write an algorithm for finding all the permutations of a given set/substring and then justify using the code, why the complexity of the algorithm is as bad as 𝑛!