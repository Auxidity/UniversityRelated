
## Task 1 from powerpoint (preliminary)

```mermaid
graph TD
A[Login] --> B[User prompt for credentials]
B --> |Matching username with db| C[Proceed to check for password match]
B --> |No username found| D[Username not found. Please check for typos or create a new account]
C --> |Password matches with username from db| E[Authenticate login]
C --> |Password doesn't match with username from db| F[Password doesn't match with username, please try again or reset password.]
D --> B
F --> B
```


## Task 2 from powerpoint (preliminary)


```mermaid
graph TD
A[Login] --> B[User prompt for date & month]
B --> |Valid date| C[Proceed to search db for given year & month]
B --> |Invalid date| D[Date given is not valid. Please check for typos]
C --> |Date is found in db| E[find min & max temperature and return it]
C --> |date doesn't match with any date from db| F[Date doesn't match with any date in db. Try another date]
D --> B
F --> B
```

## TRAK Exercises 1

### 1. 
```mermaid
graph TD 

A[Prompt for numbers A & B] --> B[Verify that given inputs are numbers] 
B --> |Verified as numbers| C[Give A*B as output]
B --> |Not verified as numbers| D[Prompt user to input numbers]
D --> A

```

### 2. 

```mermaid
graph TD 

A[Prompt for numbers A & B] --> B[Verify that given inputs are numbers] 
B --> |Verified as numbers| C[Give A mod b as output]
B --> |Not verified as numbers| D[Prompt user to input numbers]
D --> A

```

### 3. 

```mermaid
graph TD 

A[Prompt for length of base & height] --> B[Verify that given inputs are numbers] 
B --> |Verified as numbers| C[Give base*height as output and call it area]
B --> |Not verified as numbers| D[Prompt user to input numbers]
D --> A

```

### 4. 

```mermaid
graph TD 

A[Prompt for length & height of all rectangle walls] --> B[Verify that given inputs are numbers] 
B --> |Verified as numbers| C[Give length*height of each wall and sum them together as output and call it area for the room]
B --> |Not verified as numbers| D[Prompt user to input numbers]
D --> A

```

### 5. 

```mermaid
graph TD 

A[Prompt for radius of the circle] --> B[Verify that given inputs are numbers] 
B --> |Verified as numbers| C[Give pi*2r as output for perimeter and pi*r² as area]
B --> |Not verified as numbers| D[Prompt user to input numbers]
D --> A

```

### 6.  
Side note, Herons formula 
$$
A = \sqrt{s\cdot (s-a)\cdot(s-b)\cdot(s-c)}
$$
$$
s = \frac{a+b+c}{2}
$$

```mermaid
graph TD 

A[Prompt for length of all sides of the triangle] --> B[Verify that given inputs are numbers] 
B --> |Verified as numbers| C[Give area using Herons formula]
B --> |Not verified as numbers| D[Prompt user to input numbers]
D --> A

```

### 7. 
```mermaid
graph TD 

A[Prompt for length of a side of square] --> B[Verify that given input is a number] 
B --> |Verified as number| C[Give area using length² and perimeter as 4x length]
B --> |Not verified as number| D[Prompt user to input number]
D --> A

```

### 8. 

```mermaid
graph TD 

A[Prompt for length and width of rectangle] --> B[Verify that given inputs are numbers] 
B --> |Verified as numbers| C[Give total cost as cost per meter * perimeter which is 2*length + 2*width]
B --> |Not verified as numbers| D[Prompt user to input numbers]
D --> A

```

### 9. 
```mermaid
graph TD 

A[Prompt for radius of base and height of cone] --> B[Verify that given inputs are numbers] 
B --> |Verified as numbers| C[Give area as pi*r*l + pi*r²]
B --> |Not verified as numbers| D[Prompt user to input numbers]
D --> A

```

### 10. 
Note due to mermaid being bad with brackets inside a box, ill type the math for volume seperately here for clarity
$$
V = \frac{4}{3}\pi r³
$$

```mermaid
graph TD 

A[Prompt for radius of sphere] --> B[Verify that given input is number] 
B --> |Verified as number| C[Give volume as 4/3 *pi*r³ and surface area as 4*pi*r²]
B --> |Not verified as number| D[Prompt user to input number]
D --> A

```

### 11. 

```mermaid
graph TD 

A[Prompt for meters] --> B[Verify that given input is number] 
B --> |Verified as number| C[Give kilometers as input * 0.001]
B --> |Not verified as number| D[Prompt user to input number]
D --> A

```

### 12. 
Note to self, ask if we use any or all interpretations?

Interpretation 1:

Math for the graph

$$
P_{12bananas} = x
$$
$$
P_{1banana} = \frac{x}{12}
$$
where x is arbitrary number that is representing the cost of 12 bananas and P_1bananas is representing the price of 1 banana.

```mermaid
graph TD 

A[Prompt for how many bananas are being purchased] --> B[Verify that given input is number] 
B --> |Verified as number| C[Give price using input * P1banana]
B --> |Not verified as number| D[Prompt user to input number]
D --> A

```

### 15. 
Conversion formula

$$
\frac{C}{5}=\frac{F-32}{9}
$$

```mermaid
graph TD 

A[Prompt for temperature in celcius] --> B[Verify that given input is number] 
B --> |Verified as number| C[Give temperature using conversion formula]
B --> |Not verified as number| D[Prompt user to input number]
D --> A

```