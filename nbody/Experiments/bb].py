new = list(bin(1))
new.reverse()
for element in new:
    if not element in {"0", "1"}:
        new.remove(element)
    else:
        element = int(element)

print(new)
