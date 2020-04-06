# import deepcut
import json

# sample = "Hi! today we have a meeting at R35 meeting room"
# words = sample.split(" ")
# print(words)

# thai_sample = "เรียนเชิญ ประชุมผู้บริหาร ประจำการประชุมวาระที่ ๓ นัดหมายเร่งด่วน"
# x = deepcut.tokenize(thai_sample)
# bank = ["ประชุม", "นัดหมาย"]
# count = {
#     "ประชุม": 0,
#     "นัดหมาย": 0,
# }

# for w in x:
#     for s in bank:
#         if w == s:
#             count[s] += 1
# print(count)

with open("src/bank.json", 'r', encoding='utf-8') as file:
    words_bank = json.load(file)
    all_words = [ *words_bank['thai'], *words_bank['eng'] ]
    counters = { key:0 for key in all_words}

print(all_words)
print(counters)

q = {"ประชุม": 0, "นัดหมาย": 0}
f = any(filter(lambda x: x >= 2, q.values()))

print(f)
