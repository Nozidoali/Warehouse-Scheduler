#input
package_number = int(input())
capacity = int(input())
time = int(input())
package = [int(x) for x in input().split()]
package_add = [int(x) for x in input().split()]
package_capacity = [int(x) for x in input().split()]

count_max = 10000
#memorize 
mem = [[None] * (time+1)] * count_max

def transport(_package):
    _capacity = capacity
    ret = [0] * package_number
    for index in range(package_number):
        if _package[index] > _capacity:
            ret[index] = _package[index] - _capacity
            _capacity = 0
        else:
            ret[index] = 0
            _capacity = _capacity - _package[index]
    return ret
def increase(_package,value):
    ret = [0] * package_number
    for index in range(package_number):
        ret[index] = _package[index] + value * package_add[index]
    return ret
def isvalid(_package):
    for index in range(package_number):
        if _package[index] > package_capacity[index]:
            return False
    return True
def isempty(_package):
    for index in range(package_number):
        if _package[index] > 0:
            return False
    return True
def notbad(_time, _package, _count):
    if mem[_count][_time] is None:
        mem[_count][_time] = [0] * package_number
        for index in range(package_number):
            mem[_count][_time][index] = _package[index]
        return True
    for index in range(package_number):
        if _package[index] < mem[_count][_time][index]:
            for index in range(package_number):
                mem[_count][_time][index] = _package[index]
            return True
    return False

def upbound(_time, _package, _count):
    ret = 0
    temp_package = [0] * package_number
    for index in range(package_number):
        temp_package[index] = _package[index]
    for _ in range(time - _time):
        temp_package = increase(temp_package,1)
        while isvalid(increase(temp_package,1)) is False:
            ret = ret + 1
            temp_package = transport(temp_package) 
    return ret + _count

def lowbound(_time, _package, _count):
    _bound = [(sum(_package)+(time - _time)*sum(package_add)-sum(package_capacity))/capacity + _count]
    for index in range(package_number-1,0,-1):
        if _package[index] + (time - _time)*package_add[index] > package_capacity[index]:
            _bound.append(sum(_package[0:index])/capacity + _count)
#    print('lowbound: ' + str(max(_bound))) 
    return max(_bound)

def Explore(_time, _package, _count):
    if isvalid(increase(_package,(time-_time))):
        print(_count)
        exit()
    interval = 0
    while _time + interval <= time and isvalid(_package):   
        if interval == 0 or notbad(_time+interval,_package,_count):
            Explore(_time + interval, transport(_package), _count+1)
        _package = increase(_package,1)
        interval = interval + 1

Explore(0,package,0)