## Assignment 8

### The question: So far we've investigated the ages dataset. Try answering some basic questions about the salaries dataset using the (very simple and slightly broken) Laplace mechanism we've defined here. Some starting points might be:

1. What is the average salary? - 48961.53 
    Using the following code. No dp applied. (I am assuming we wanted no noise, just the raw values)  
```
average_salary_no_dp = np.mean(salaries)
average_salary_no_dp
```
2. What is the average salary of people over 40? - 48184.029411764706
```
# Filter the salaries of employees over 40, no noise
ages = np.array(ages)
salaries = np.array(salaries)
salaries_over_40_no_dp = salaries[ages > 40]

average_salary_over_40_no_dp = np.mean(salaries_over_40_no_dp)
average_salary_over_40_no_dp
```
3. What is the average salary for people under 40? - 50613.71875

```
# Filter the salaries of employees under 40, no noise
ages = np.array(ages)
salaries = np.array(salaries)
salaries_under_40_no_dp = salaries[ages <= 40]

average_salary_under_40_no_dp = np.mean(salaries_under_40_no_dp)
average_salary_under_40_no_dp
```
PS. Technically should've used ages < 40 for "under" I suppose, but its a bit weird to not include the people that are exactly 40 years old. The answer is 50727.6129032258 if you change <= to <.
48168.07246376811 would be the answer if you were to change > to >= instead, depending on which end you'd want to include the exactly 40 years old.

Note : Jupyter notebook server is preferred. Nbterm doesn't work on pandas plots (does it work on any graph?) so you need to use something that plots the graphs.
