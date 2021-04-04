from collections import Counter

def main():
    l1 = Counter(input())
    l2 = Counter(input())
    sticky = [c for c in l1.keys() if l1[c] != l2[c]]
    print(''.join(sticky))

main()