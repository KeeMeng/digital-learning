##expression = input("input: ")
##single_frames = set()
##
##for element in expression.split(','):
##    parts = [int(x) for x in element.split('-')]
##    if len(parts) == 1:
##        single_frames.add(parts[0])
##    else:
##        for frame in range(min(parts), max(parts) + 1):
##            single_frames.add(frame)
##
##print(list(single_frames))

single = []
for item in input("Pages: ").split(','):
    ranges = item.split('-')
    if len(ranges) == 1:
        single.append(int(ranges[0]))
    else:
        [single.append(i) for i in range(int(ranges[0]), int(ranges[-1]) + 1)]
print(list(single))
