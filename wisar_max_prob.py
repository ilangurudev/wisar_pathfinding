import sys
import numpy as np

filename = sys.argv[1]
start_pos = (0, 0)
fn = filename.split(".")[0]
probs = []
nodes = []
prob_dict = {}
non_zero_nodes_dict = {}

file = open(filename,'r') 

def euclid_distance(a, b):
    return(((a[0] - b[0])**2 + (a[1] - b[1])**2)**(1/2))

for l in file:
    contents = l.split(" ")
    x = int(contents[0])
    y = int(contents[1])
    point = (x, y)
    prob = float(contents[2])
    probs.append(prob)
    nodes.append(point)
    prob_dict[point] = prob
    
    if(prob > 0):
        if(x in non_zero_nodes_dict.keys()):
            x_ys = non_zero_nodes_dict[x]
            x_ys.append(y)
            x_ys.sort()
            non_zero_nodes_dict[x] = x_ys
        else:
            non_zero_nodes_dict[x] = [y]

    
probs = np.array(probs)
nodes = np.array(nodes)

prev_pos = start_pos
non_zero_nodes = nodes[probs > 0.0]
# direction_up = True
# total_distance = 0.0
# total_probability = prob_dict[prev_pos]
cum_prob = 0.0
cum_dist = 0.0
dist_snaps = []
prob_snaps = []
covered_nodes = [prev_pos]


f = open('results/' + fn + '_max_prob_path.txt','w')
# f.write("x,y")
# f.write("\n")
f.write("0 0")
f.write("\n")


while not len(covered_nodes) == (len(non_zero_nodes)+1):
    high_prob_nodes = nodes[probs == max(probs)]
    d = 0.0
    next_pos = (0, 0)
    for n in high_prob_nodes:
        n = tuple(n)
        if d == 0.0:
            d = euclid_distance(prev_pos, n)
            next_pos = n
        if euclid_distance(prev_pos, n) < d:
            d = euclid_distance(prev_pos, n)
            next_pos = n
    
#     print(prev_pos, next_pos)
    
    index = "a"
    for j in range(len(nodes)):
        if (nodes[j] == next_pos).all():
#             print(j)
            index = j
            break
    
    cum_prob += max(probs)
    cum_dist += euclid_distance(prev_pos, next_pos)
    prob_snaps.append(cum_prob)
    dist_snaps.append(cum_dist)
    probs = np.delete(probs, index, axis = 0)
    nodes = np.delete(nodes, index, axis = 0)
    covered_nodes.append(next_pos)
    st = str(next_pos[0]) + " " + str(next_pos[1])
    f.write(st)
    f.write("\n")

    prev_pos = next_pos
    
    
f.close()

import matplotlib.pyplot as plt
fig1 = plt.figure()
ax1 = fig1.add_subplot(111)
ax1.plot(dist_snaps, prob_snaps, "-")
plt.title('Time vs Cumulative Probability')
plt.xlabel('Time')
plt.ylabel('Cumulative Probability')
# plt.show()
plt.savefig('results/' + fn + "_max_prob_timeVprob.png", dpi = 200)

#closest non-zero prob nodes:

d = 0

for x in non_zero_nodes_dict.keys():
    for y in non_zero_nodes_dict[x]:
        if d == 0:
            d = euclid_distance((x, y), start_pos)  
        else:
            if euclid_distance((x, y), start_pos)  < d:
#                 print(x,y)
                d = euclid_distance((x, y), start_pos)
                
# d

#Efficiency LB calculcation
import numpy as np
import pandas as pd

all_probs = list(prob_dict.values())
all_probs.sort()
all_probs.reverse()

dist_snaps_np = np.array(dist_snaps)
prob_snaps_np = np.array(prob_snaps)
ts = [100, 200, 300, 600, 900]
# ts = range(100, 5000, 50)
B = []
PC = []
efficiencyLB = []

for t in ts:
    N = int(t + 1 - d)
    
    Bt = sum(all_probs[:N]) 
    
    a = dist_snaps_np - t
    Pt = prob_snaps_np[abs(a) == min(abs(a))]
    Pt = Pt[0]
    Pt = float(Pt)
    
    B.append(Bt)
    PC.append(Pt)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)
ax2.plot(ts, B, 'g-', label='B')
ax2.plot(ts, PC, 'b-', label='PC')
plt.title('Time vs Cumulative Probability')
plt.xlabel('Time')
plt.ylabel('Cumulative Probability')
plt.legend(loc='upper left')
plt.savefig('results/' + fn + "_max_prob_BPt_coverageVtime.png", dpi = 200)


B = np.array(B)
PC = np.array(PC)
efficiencyLB = PC/B

fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
ax3.plot(ts, efficiencyLB, 'g-')
plt.title('Time vs EfficiencyLB')
plt.xlabel('Time')
plt.ylabel('EfficiencyLB')
plt.savefig('results/' + fn + "_max_prob_efficiencyLB.png", dpi = 200)

efficiency = pd.DataFrame({'T':ts, 'B': B, 'PC': PC, 'efficiencyLB': efficiencyLB})
efficiency.to_csv('results/' + fn + '_max_prob_efficiency_LB.csv')
