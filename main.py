import pandas as pd
from ast import literal_eval
import matplotlib.pyplot as plt
import pyfpgrowth
from apriori import *
data = pd.read_csv('GroceryStore/Groceries.csv',usecols=['items'],converters={'items':lambda x:x[1:-1].split(sep=',')})
items_list=data['items'].tolist()


# print(items_list)
# # print(items_list[0])
# dummy_apriori=DummyApriori(items_list,0.01)
# apriori_1=AdvancedApriori1(items_list,0.01)
# apriori_1_2=AdvancedApriori12(items_list,0.01)
# apriori_1_2.getFreqItems(10)
# #
# cost1=[]
# cost2=[]
# cost3=[]
#
# for k in range(1,10):
#     print(k)
#     _,t1=dummy_apriori.getFreqItems(k)
#     _,t2=apriori_1.getFreqItems(k)
#     _,t3=apriori_1_2.getFreqItems(k)
#     cost1.append(t1)
#     cost2.append(t2)
#     cost3.append(t3)
#
# plt.plot(range(1,10),cost1,'r',cost2,'g',cost3,'b')
# plt.legend(['dummy_apriori','apriori_1','apriori_1_2'])
# plt.show()



# dummy_apriori.getFreqItems()
# rules=dummy_apriori.getAssociationRule(0.1)
# print(rules)
# apriori1(3)
# apriori12(3)

#
# patterns=pyfpgrowth.find_frequent_patterns(items_list,int(len(items_list)*0.01))
# rules=pyfpgrowth.generate_association_rules(patterns,0.5)
#
# for k,v in rules.items():
#     print(k,v)


aa1=AdvancedApriori1(items_list,0.01)
freqs,_=aa1.getFreqItems()
rules=aa1.getAssociationRule()
print(freqs)
print(rules)

# rules=aa1.getAssociationRule(0.5)
# for rule in rules:
#     print(rule)

# dummy_apriori(1)
# dummy_apriori(2)
# dummy_apriori(3)
# dummy_apriori(4)
# dummy_apriori(5)
# dummy_apriori(6)
# dummy_apriori(7)
# dummy_apriori(8)
# apriori12(10)
