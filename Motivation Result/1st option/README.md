
We use the cobbs-douglas utility function like this : 
```python
G = (EcologicalFactor_a_b**Exponen)*(TrustFactor_a_b**(2-Exponen))
``` 

The difference is at how the exponen is choosen
- Random Option (7 choice) : 
```python
Exponen = random.choice([0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75]) 
```
- Split into 3 choice (equal size) : 
```python
Exponen = [0.5, 0.75, 1, 1.25, 1.5]
Exponen = Exponen[(int(a)-1)//40]
```
- Split into 3 choice (equal size)
```python
Exponen = [0.5, 1, 1.5]
if int(a) < 67 :
    Exponen = Exponen[0]
elif int(a) > 133 :
    Exponen = Exponen[2]
else:
    Exponen = Exponen[1]
```

