a = list(map(int, input().strip().split()))
b = list(map(int, input().strip().split()))
score_alice = 0
score_bob = 0
if a[0] > b[0]:
    score_alice += 1
else:
    score_bob += 1
if a[1] > b[1]:
    score_alice += 1
else:
    score_bob += 1
if a[2] > b[2]:
    score_alice += 1
else:
    score_bob  += 1
print(str(2)+ " " + str(0))