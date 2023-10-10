# Challenge

> Course: VE477  
> Name: Wang Hanyu  
> Student-id: 517370910174  

## Part.1 -- Problem Description
**n** warehouse with initial storage **pi** and increasement rate **ai**. Find the minimum number of trucks, which clear up the first **s** packages in the warehouses, that ensures all the warehouse has storage lower than capacity **wi** in **t** hours.

#### Input
```python
    n           # number of warehouse
    t           # number of hours in a day
    p1 a1 w1    # pi,ai,wi of warehouse
    ...
    pn an wn
```

### Output
```python
    minimum      # the minimum trucks demand
```
---
## Part.2 -- Implementation
#### Analysis
This problem expect us to find the minimized trunk numbers to keep the storage under the limitation. As in the example given in **Hint 1**:
```python
3
3
2 4 10
3 3 9
4 2 8
```
```
|  # hour  | Zizhu | Qingpu | Kunshan |
| :------: | :---: | :----: | :-----: |
|    0     |   2   |   3    |    4    |
| trunk #1 |   0   |   0    |    0    |
|    1     |   4   |   3    |    2    |
|    2     |   8   |   6    |    4    |
| trunk #2 |   0   |   4    |    4    |
|    3     |   4   |   7    |    6    |
```
Then we find that we send trunk to clean `Kunshan` when:  
- `Kunshan` is about to exceed the limit  
- `Zizhu` and `Qingpu` has too many parcels that cost to clean `Kunshan` gets too large

Thus we can conclude that Greedy algorithm can not save this problem because the previous decision will affect the priority of decision in the future. 

#### Algorithm
The idea of my algorithm is applying depth first search with adequate pruning. I set the time to be the depth and branch if sending different amount of trucks:
```
| # hour |     0     |     1     |     2     |
| :----: | :-------: | :-------: | :-------: |
|        | 2,3,4 (0) | 6,6,6 (0) | 10,9,8(0) |
|        |           |           | 0,9,8 (1) |
|        |           |           | 0,0,7 (2) |
|        |           | 0,2,6 (1) | 4,5,8 (1) |
|        |           |           | 0,0,7 (2) |
|        |           | 0,0,0 (2) | 4,3,2 (2) |
|        |           |           | 0,0,0 (3) |
|        | 0,0,0 (1) | 4,3,2 (1) | 8,6,4 (1) |
|        |           |           | 0,4,4 (2) |
|        |           |           | 0,0,0 (3) |
|        |           | 0,0,0 (2) | 4,3,2 (2) |
|        |           |           | 0,0,0 (3) |
```
In the example above we set the depth to be 2. In this example we have already examine if the storage has already been reduce to 0 or has already exceed the limit. However, we still find some same elements in the table. Thus we apply memorization. Sum it up:  
- pruning when storage is lower than **0**  
- pruning when storage is greater than **wi**
- memorize the result with respect to storage  

Then the worst case complexity is: O(t\*w1\*w2\*...\*wn), however, in most of the cases the complexity is lower than that because of the descretized value.

#### Validation
Then I will briefly prove the correctness of my implementation by listing some of my code. Since I am apply depth first search, which is an recursive method. I will divide my prove into two parts, the boundary condition and the transition between conditions.

##### Boundary Condition
We search from 0. Then when `t = itinerary`, we have reach the end, thus the principal here is to find the minimum number of trucks to reduce the storage to be under the capacity. Therefore we consistenly send truck until less than capacity:

```python
    if time == self.itinerary:
        truck = 0
        self.AddPackage()
        while self.isValid() is not True:
            self.SendTruck()
            truck = truck + 1
        self.package = copy.deepcopy(package)
        return truck
```

##### Transition Equation
The basic idea is:
```python
    Search(time) = min{Search(time+1) + <truck>}
```
Here we enumarate all the possible truck number and recursively find the result of `Search(time+1)`, thus if it holds true in `time+1`, the best solution of this step is valid.

```python
    while True:
        if self.isValid():
            ans = self.Search(time+1)
            choice.append(ans + truck)
        # prun if the all warehouse is empty
        if self.isEmpty():
            break
        # recursively send truck
        self.SendTruck()
        truck = truck + 1
    # choose the best result
    self.memorize[key] = min(choice)
    return min(choice)
```

## Appendix
```python
import copy

class challenge:
    def __init__ (self):
        self.itinerary = 0          # the itinerary is a constant 
        self.truck_capacity = 0     # the capacity of the truck
        self.warehouse = []         # the list of warehouse
        self.package_add = {}       # the number of packages added to the warehouse every hour
        self.package = {}           # the number of packages
        self.capacity = {}          # the capacity of warehouse
        self.memorize = {}          # memorize
        self.stack = []

    def AddWarehouse(self,warehouse,package,package_add,capacity):
        self.warehouse.append(warehouse)
        self.package[warehouse] = package
        self.package_add[warehouse] = package_add
        self.capacity[warehouse] = capacity

    def SetTime(self,itinerary):
        self.itinerary = itinerary

    def SetCapacity(self,capacity):
        self.truck_capacity = capacity

    def isValid(self):
        for warehouse in self.warehouse:
            if self.package[warehouse] > self.capacity[warehouse]:
                return False
        return True

    def isEmpty(self):
        for warehouse in self.warehouse:
            if self.package[warehouse] > 0:
                return False
        return True   

    def SendTruck(self):
        capacity = self.truck_capacity
        for warehouse in self.warehouse:
            if capacity <= self.package[warehouse]:
                self.package[warehouse] = self.package[warehouse] - capacity
                break
            capacity = capacity - self.package[warehouse]
            self.package[warehouse] = 0

    def AddPackage(self):
        for warehouse in self.warehouse:
            self.package[warehouse] = self.package[warehouse] + self.package_add[warehouse]

    def SubPackage(self):
        for warehouse in self.warehouse:
            self.package[warehouse] = self.package[warehouse] - self.package_add[warehouse]

    # return the minimum trucks needed to survive 'time'
    def Search(self, time):
        package = copy.deepcopy(self.package)
        # finish searching
        if time == self.itinerary:
            truck = 0
            self.AddPackage()
            while self.isValid() is not True:
                self.SendTruck()
                truck = truck + 1
            self.package = copy.deepcopy(package)
            return truck
        # search in memorized hash table
        key = '.'.join([str(self.package[x]) for x in self.package]) + '.' + str(time)
        if key in self.memorize:
            return self.memorize[key]
        # search 'time + 1'
        truck = 0
        choice = []
        while True:
            # prun if the package distribution violate the limit
            if time > 0:
                self.AddPackage()
            if self.isValid():
                ans = self.Search(time+1)
                choice.append(ans + truck)
            if time > 0:      
                self.SubPackage()
            # prun if the all warehouse is empty
            if self.isEmpty():
                break
            # recursively send truck
            self.SendTruck()
            truck = truck + 1
        self.package = copy.deepcopy(package)
        # choose the best result
        self.memorize[key] = min(choice)
        return min(choice)

    
    def Solve(self):
        # initialize the prefix sum
        ans = self.Search(0)
        print('result: ', str(ans))


problem = challenge()
problem.SetTime(3)
problem.SetCapacity(10)
problem.AddWarehouse('Zizhu Science Park',2,4,10)
problem.AddWarehouse('Qingpu',3,3,9)
problem.AddWarehouse('Kunshan',4,2,8)
problem.Solve()
```