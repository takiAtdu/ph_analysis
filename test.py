diagonal = []
for i in range(64):
    if i == 0:
        diagonal.append(i)
    else:
        x = diagonal[i-1] + i + 1
        diagonal.append(x)

print(diagonal)