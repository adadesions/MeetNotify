import deepcut

sample = "Hi! today we have a meeting at R35 meeting room"
words = sample.split(" ")
print(words)

thai_sample = "เรียนเชิญ ประชุมผู้บริหาร ประจำการประชุมวาระที่ ๓ นัดหมายเร่งด่วน"
x = deepcut.tokenize(thai_sample)
bank = ["ประชุม", "นัดหมาย"]
count = {
    "ประชุม": 0,
    "นัดหมาย": 0,
}

for w in x:
    for s in bank:
        if w == s:
            count[s] += 1
print(count)