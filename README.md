# BOOTH-ALGORITHM
Booth's multiplication algorithm.

Given two integers and number of bits (at least the necessary to represent the two integers), this code will show how Booth's Algorithm for binary multiplication works.

The example below shows how 3 and 5 are multiplied according to Booth's Algorithm.

```Multiplicand: 0011```

```Multiplier: 0101```

```--- | 000001010```<br/>
```SUB | 110101010```<br/>
```>>> | 111010101```<br/>
```SUM | 000110101```<br/>
```>>> | 000011010```<br/>
```SUB | 110111010```<br/>
```>>> | 111011101```<br/>
```SUM | 000111101```<br/>
```>>> | 000011110```<br/>
```END |  00001111```<br/>


