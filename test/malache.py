
def Manacher(s):
    t = ['$','#']
    for v in s:
        t.append(v)
        t.append('#')
    p = [0] * len(t)
    mx = 0
    id = 0
    maxSubLen = 0
    maxSubCenter = 0
    for i in range(len(p)):
        p[i] = min(p[2 * id - i], mx - i) if mx > i else 1
        while t[i + p[i]] == t[i - p[i]]:
            p[i] += 1
        if mx < i+p[i]:
            mx = i+p[i]
            id = i
        if maxSubCenter < p[i]:
            maxSubLen = p[i]
            maxSubCenter = i
    return s[(maxSubCenter - maxSubLen) / 2, maxSubLen - 1]

print(Manacher("12321"))
# string Manacher(string s) {
# 	// Insert '$' and '#'
# 	string t = "$#";
# 	for (int i = 0; i < s.size(); ++i) {
# 		t += s[i];
# 		t += "#";
# 	}
# 	// Process t
# 	vector<int> p(t.size(), 0);
# 	int mx = 0, id = 0, maxSubLen = 0, maxSubCenter = 0;
# 	for (int i = 1; i < t.size(); ++i) {
# 		//具体详见上边算法
# 		p[i] = mx > i ? min(p[2 * id - i], mx - i) : 1;
# 		//老实的一个一个往前后扩展对比
# 		while (t[i + p[i]] == t[i - p[i]])
# 			++p[i];//往前、往后一个一个的扩展
# 		if (mx < i + p[i]) {//更新mx和id
# 			mx = i + p[i];
# 			id = i;
# 		}
# 		if (maxSubLen < p[i]) {//更新最长子串内容
# 			maxSubLen = p[i];//记录最长子串半径
# 			maxSubCenter = i;//记录最长子串中心位置
# 		}
# 	}
# 	return s.substr((maxSubCenter - maxSubLen) / 2, maxSubLen - 1);
# }
