# Calculate Expression
### A simple calculator dealing with expressions in string type ,using stack data structure.

# Features

 - You can custom each operator's priority and behavior.
 - Expressions both with and without algebras are supported.
 
# Caution

 - spaces in input expressions will be removed while processing.
 - each expression will be converted into (expression) before processing to avoid empty stack problems.

# Installation

    $ pip install calculate-expression

#####   \* since using f-string for formating ,could only be installed on python3.6+

# Usage

initialize a standard calculator:
(optional parameters "rule" & "regularization")

    from calculate_expression import ce
    standard = ce.Calculator()

You can custom your own operator sets ,default ones like this:

    # "operator":(priority,'behavior')
    # behavior is string type ,thus we can easily check its logic
    # we will use eval() to convert it into function later
    rules = { '+' : (0 ,'lambda x,y:x+y') ,
             '-' : (0 ,'lambda x,y:x-y') ,
             '*' : (1 ,'lambda x,y:x*y') ,
             '/' : (1 ,'lambda x,y:x/y') , 
             '^' : (2 ,'lambda x,y:x**y') }
    standard = ce.Calculator(rules)
    

#####   \* once new operator is added ,regularization function may need to be modified commensurately.
#####   \* default regularization function: `lambda x:x.replace("**","^").replace('\\','/')`

You can check operate rules and regularfunction like this ,
Thus you can easily modify it.

    > standard.printinfo()
    > 
    > defalut_regularization_function = lambda x:x.replace('**','^').replace('\\','/')
    > 
    > rules = { '+' : (0, 'lambda x,y:x+y') ,
    >           '-' : (0, 'lambda x,y:x-y') ,
    >           '*' : (1, 'lambda x,y:x*y') ,
    >           '/' : (1, 'lambda x,y:x/y') ,
    >           '^' : (2, 'lambda x,y:x**y') }
    >

Try a simple calculate

    > print( standard.calculate('1 + 2 * 3') )
    > 7

Algebra is supported

    > print( standard.calculate('a + b * c' ,a = 1 ,b = 2 ,c = 3) )
    > 7

Once introduced ,algebras will be stored in whose object's attribute as a dictionary ,
It will remain until it's updated.

    > print( standard.calculate('' ,a = 1 ,b = 2 ,c = 3 ,d = 4 ,e = 1.6) ) # update params only 
    > None
    > print( standard.calculate('d ** 4 / e') )
    > 160
    > print( standard.calculate('d ** 4 / e' ,e = 0.1625) )
    > 1575.3846153846152

Have fun.
