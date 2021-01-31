from collections import defaultdict
from itertools import combinations,chain
import time
import copy

def _getItemFromList(items_list):
    t = set()
    for items in items_list:
        for item in items:
            t.add(frozenset([item]))
    return t


class Apriori:
    def __init__(self, items_list, support):
        '''
        :param items_list: 一条记录所包含的集合，eg.[tropical fruit,yogurt,coffee]
        :param support: 支持度
        '''
        self.all_items_list = items_list
        self.support = support
        self.global_freq_item_set = dict()
        self.global_item_set_with_sup = defaultdict(int)

    @classmethod
    def Timer(cls,func):
        def call_func(*args, **kwargs):
            begin_time = time.time()
            ret = func(*args, **kwargs)
            end_time = time.time()
            Run_time = end_time - begin_time
            print(f"{cls.__name__}:耗时{int(Run_time * 1000)}毫秒")
            return ret,Run_time

        return call_func

    def getFreqItems(self, feq_len=99999999):
        raise NotImplementedError

    def _getUnion(self, items, length):
        return set([i.union(j) for i in items for j in items if len(i.union(j)) == length])

    def _getAboveMinSup(self, items_list):
        """
        :param items_list:
        :return:
        """
        feq_items_list = set()
        feq_items_with_sup_dict = defaultdict(int)
        for items in items_list:
            for source_items in self.all_items_list:
                if items.issubset(source_items):
                    feq_items_with_sup_dict[items] += 1

        for items, cnt in feq_items_with_sup_dict.items():
            if cnt / len(self.all_items_list) >= self.support:
                feq_items_list.add(items)
                self.global_item_set_with_sup[items] += cnt
        return feq_items_list

    def getAssociationRule(self, confidence=0.2):
        """
        :param confidence: 置信度
        :return:给定支持度和置信度下面的关联规则
        """
        if len(self.global_freq_item_set)==0 or len(self.global_freq_item_set)==0:
            raise Exception('没有调用getFreqItems吧')

        def getSubsets(items):
            return chain.from_iterable(combinations(items,r) for r in range(1,len(items)))
        # self.getFreqItems()  # 计算出self.global_freq_item_set和self.global_item_set_with_sup
        rules=[]
        for k,freq_items_list in self.global_freq_item_set.items():
            for freq_items in freq_items_list:
                subsets = getSubsets(freq_items)  # 得到频繁项集的子集，频繁项集的子集肯定也是频繁项集
                for subset in subsets:
                    conf=self.global_item_set_with_sup[freq_items]/self.global_item_set_with_sup[frozenset(subset)]
                    if conf>=confidence:
                        rules.append([frozenset(subset),freq_items.difference(subset),conf])
        rules.sort(key=lambda x:x[-1])
        return rules

    def pruning(self, candidate_items_list, prev_items_list, length):
        raise NotImplementedError


class DummyApriori(Apriori):

    @Apriori.Timer
    def getFreqItems(self, feq_len=99999999):
        c1_items_list = _getItemFromList(self.all_items_list)
        cur_items_list = self._getAboveMinSup(c1_items_list)
        # if feq_len == 1: return cur_items_list
        k = 2
        while cur_items_list:
            self.global_freq_item_set[k - 1] = cur_items_list
            if k - 1 == feq_len: break
            candidate_items_list = self._getUnion(cur_items_list, k)
            candidate_items_list = self.pruning(candidate_items_list, cur_items_list, k - 1)
            cur_items_list = self._getAboveMinSup(candidate_items_list)
            k += 1

        return self.global_freq_item_set

    def pruning(self, candidate_items_list, prev_items_list, length):
        return candidate_items_list



class AdvancedApriori1(Apriori):

    def __init__(self, items_list, support):
        super().__init__(items_list, support)
        self.source_items_list_len=len(items_list)

    @Apriori.Timer
    def getFreqItems(self, feq_len=99999999):
        self.global_freq_item_set = dict()
        self.global_item_set_with_sup = defaultdict(int)
        c1_items_list = _getItemFromList(self.all_items_list)
        cur_items_list = self._getAboveMinSup(c1_items_list)
        # if feq_len == 1: return cur_items_list
        k = 2
        while cur_items_list:
            self.global_freq_item_set[k - 1] = cur_items_list
            if k - 1 == feq_len: break
            candidate_items_list = self._getUnion(cur_items_list, k)
            candidate_items_list = self.pruning(candidate_items_list, cur_items_list, k - 1)
            cur_items_list = self._getAboveMinSup(candidate_items_list)
            k += 1

        return self.global_freq_item_set

    def pruning(self, candidate_items_list, prev_items_list, length):
        """
        频繁项的k-1项的子集必须是频繁的

        :param candidate_items_list: 当前的k项的待剪枝的频繁项集
        :param prev_items_list: k-1项的已确定的频繁项集
        :param length: 生成的子集的长度
        :return: 剪枝后的k项频繁项集
        """
        tmp_candidate_items_list = candidate_items_list.copy()
        for items in candidate_items_list:
            subsets = combinations(items, length)
            if not all((frozenset(subset) in prev_items_list for subset in subsets)):
                tmp_candidate_items_list.remove(items)
        return tmp_candidate_items_list


class AdvancedApriori12(Apriori):


    def __init__(self, items_list, support):
        '''
        :param items_list: 一条记录所包含的集合，eg.[tropical fruit,yogurt,coffee]
        :param support: 支持度
        '''
        self.all_items_list = copy.deepcopy(items_list)
        self.support = support
        self.global_freq_item_set = dict()
        self.global_item_set_with_sup = defaultdict(int)
        self.source_items_list_len = len(items_list)

    @Apriori.Timer
    def getFreqItems(self, feq_len=99999999):
        c1_items_list = _getItemFromList(self.all_items_list)
        cur_items_list = self._getAboveMinSup(c1_items_list, 1)
        # if feq_len == 1: return cur_items_list
        k = 2
        while cur_items_list:
            self.global_freq_item_set[k - 1] = cur_items_list
            if k - 1 == feq_len: break
            candidate_items_list = self._getUnion(cur_items_list, k)
            candidate_items_list = self.pruning(candidate_items_list, cur_items_list, k - 1)
            cur_items_list = self._getAboveMinSup(candidate_items_list, k)
            print(len(self.all_items_list))
            k += 1

        return self.global_freq_item_set

    def pruning(self, candidate_items_list, prev_items_list, length):
        tmp_candidate_items_list = candidate_items_list.copy()
        for items in candidate_items_list:
            subsets = combinations(items, length)
            if not all((frozenset(subset) in prev_items_list for subset in subsets)):
                tmp_candidate_items_list.remove(items)
        return tmp_candidate_items_list

    def _getAboveMinSup(self, items_list, k=-1):
        """
        :param items_list:
        :param k: 循环计算长度从[1,fre_len]的频繁项集，传入当前长度
        :return:
        """
        feq_items_list = set()
        feq_items_with_sup_dict = defaultdict(int)
        match_times = [0] * len(self.all_items_list)
        del_items_idx = []
        for items in items_list:
            for idx, source_items in enumerate(self.all_items_list):
                if items.issubset(source_items):
                    match_times[idx] += 1
                    feq_items_with_sup_dict[items] += 1

        for idx, match_time in enumerate(match_times):
            if match_time < k + 1: del_items_idx.append(idx)


        for idx in reversed(del_items_idx):
            del self.all_items_list[idx]

        for items, cnt in feq_items_with_sup_dict.items():
            if cnt / self.source_items_list_len >= self.support:
                feq_items_list.add(items)
                self.global_item_set_with_sup[items] += cnt
        return feq_items_list
