# if文
x = 123
if x % 2 == 0:
    res = '偶数です。'
else:
    res = '奇数です。'
str(x) + 'は、' + res

# elif
month = 8
res = month // 3
if month == 12:
    res = 0

if res== 0:
    season = '冬'
elif res == 1:
    season ='春'
elif res == 2:
    season = '夏'
elif res == 3:
    season = '秋'
else:
    season  = '？'
str(month) + '月は、' + season + 'です。'

# while文
end = 100
total = 0
count = 1
while count <= end:
    total += count
    count+= 1
'１から' + str(end) + 'までの合計は、' + str(total) + 'です。'
