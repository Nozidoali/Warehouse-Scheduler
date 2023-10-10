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
        print(ans)

problem = challenge()
cityCount = int(input(''))
capacityCount = int(input(''))
timeCount = int(input(''))
problem.SetTime(timeCount)
problem.SetCapacity(capacityCount)
initial = [int(x) for x in input().split()]
increase = [int(x) for x in input().split()]
capacity = [int(x) for x in input().split()]
for city in range(cityCount):
    problem.AddWarehouse(str(city),initial[city],increase[city],capacity[city])
problem.Solve()
