import json
import numpy as np
import unittest


def compute_mccs_stats(results):
    output ={}
    for key, data in results.items():
        mean, sem, ci= compute_mean_sem_ci(data)
        output[key] = {'mean': mean, 'sem': sem, 'ci': ci}
    return output

def compute_mean_sem_ci(data, ci_value=2.576):
    mean = np.mean(data)
    sem = np.std(data) / np.sqrt(len(data))
    ci = ci_value * sem
    return mean, sem, ci

def dict_to_json(d, filename):
    with open(filename, 'w') as f:
        json.dump(d, f)

def overlap(s1,e1,s2,e2, strict = False):
    if not strict:
        if s1 < s2 and e1 < s2: return False
        if s1 > e2 and e1 > e2: return False
        return True
    if s1 <= s2 and e1 <= s2: return False
    if s1 >= e2 and e1 >= e2: return False
    return True

def overlap_duration(s1,e1,s2,e2):
    max_start = max(s1,s2)
    min_end = min(e1,e2)
    duration = min_end - max_start
    return duration


class TestOverlap(unittest.TestCase):
    def test_true_overlap(self):
        self.assertEqual(overlap(1,3,3,4),True, 'should be True')
        self.assertEqual(overlap(4,5,3,4),True, 'should be True')
        self.assertEqual(overlap(3,5,2,5),True, 'should be True')
        self.assertEqual(overlap(1,5,2,5),True, 'should be True')
        self.assertEqual(overlap(1,6,2,5),True, 'should be True')
        self.assertEqual(overlap(3,4,2,5),True, 'should be True')
        self.assertEqual(overlap(1,2,0,4),True, 'should be True')
        self.assertEqual(overlap(1,2,0,1),True, 'should be True')
        self.assertEqual(overlap(1,2,0,2),True, 'should be True')

    def test_non_overlap(self):
        self.assertEqual(overlap(1,2,3,4),False, 'should be False')
        self.assertEqual(overlap(5,6,3,4),False, 'should be False')
        self.assertEqual(overlap(1,2,-3,0),False, 'should be False')
        self.assertEqual(overlap(5,6,30,40),False, 'should be False')

    def test_strict_true_overlap(self):
        self.assertEqual(overlap(3,5,2,5,True),True, 'should be True')
        self.assertEqual(overlap(1,5,2,5,True),True, 'should be True')
        self.assertEqual(overlap(1,6,2,5,True),True, 'should be True')
        self.assertEqual(overlap(3,4,2,5,True),True, 'should be True')
        self.assertEqual(overlap(1,2,0,4,True),True, 'should be True')
        self.assertEqual(overlap(1,2,0,2,True),True, 'should be True')

    def test_strict_non_overlap(self):
        self.assertEqual(overlap(1,2,3,4),False, 'should be False')
        self.assertEqual(overlap(5,6,3,4),False, 'should be False')
        self.assertEqual(overlap(1,2,-3,0),False, 'should be False')
        self.assertEqual(overlap(5,6,30,40),False, 'should be False')
        self.assertEqual(overlap(1,3,3,4),True, 'should be False')
        self.assertEqual(overlap(4,5,3,4),True, 'should be False')
        self.assertEqual(overlap(1,2,0,1),True, 'should be False')
        self.assertEqual(overlap(-1,0,0,1),True, 'should be False')

if __name__ == '__main__':
    print('testing overlap')
    unittest.main()
