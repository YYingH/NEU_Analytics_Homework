import pandas as pd

def is_Q(q):
    return (q > 750)
def is_S(s):
    return (s < 15)
def is_C(c):
    return (c < 222000)

def part_1(df):
    totalNum = df.count()
    # P[Q] --- Count    Probability
    countP = df[df[events['Q']]>750].count()
    probabilityP = countP/totalNum
    print("The Number of Event Q: ", countP[events['Q']],
          ", The Probability of Event Q: ", probabilityP[events['Q']])

    # P[S] --- Count    Probability
    countS = df[df[events['S']] < 15].count()
    probabilityS = countS / totalNum
    print("The Number of Event S: ", countS[events['S']],
          ", The Probability of Event S: ", probabilityS[events['S']])

    # P[C] --- Count    Probability
    countC = df[df[events['C']] < 222000].count()
    probabilityC = countC / totalNum
    print("The Number of Event C: ", countC[events["C"]],
          ", The Probability of Event C: ", probabilityC[events['C']])

def part_2(df):
    # Calculate score for each project
    def score_cal(q, s, c):
        score = 0
        if not is_Q(q) and not is_C(c) and not is_S(s): score = 0
        elif is_Q(q) and not is_C(c) and not is_S(s): score = 1
        elif is_S(s) and not is_C(c) and not is_Q(q): score = 2
        elif is_C(c) and not is_Q(q) and not is_S(s): score = 3
        elif is_Q(q) and is_S(s) and not is_C(c): score = 4
        elif is_Q(q) and is_C(c) and not is_S(s): score = 5
        elif is_S(s) and is_C(c) and not is_Q(q): score = 6
        elif is_Q(q) and is_C(c) and is_S(s): score = 7
        return score
    # Get probability for each score
    def count_prob_cal (df, score):
        total = len(df)
        count = len(df[df['score']==score])
        prob = count/total
        return count,prob

    df['score'] = df.apply(lambda x: score_cal(x[events['Q']], x[events['S']], x[events['C']]), axis=1)
    for score in range(0,8):
        count, prob = count_prob_cal(df, score)
        print("P(Score = %d)\t Count: %d\t Probability: %.2f"%(score, count, prob))

def part_3(df):
    def split_group(q, s, c):
        if not is_C(c) and not is_Q(q) and not is_S(s): return 0
        elif is_Q(q) and not is_S(s) and not is_C(c): return 1
        elif is_S(s) and not is_Q(q) and not is_C(c): return 2
        elif is_C(c) and not is_Q(q) and not is_S(s): return 3
        elif is_S(s) and is_Q(q) and not is_C(c): return 4
        elif is_Q(q) and is_C(c) and not is_S(s): return 5
        elif is_C(c) and is_S(s) and not is_Q(q): return 6
        elif is_Q(q) and is_C(c) and is_S(s): return 7
    df['group'] = df.apply(lambda x: split_group(x[events['Q']], x[events['S']], x[events['C']]), axis=1)
    group_count_0 = len(df[df['group'] == 0])
    print("The Count of num 0 in Venn :",group_count_0)
    group_count_1 = len(df[df['group'] == 1])
    print("The Count of num 1 in Venn :", group_count_1)
    group_count_2 = len(df[df['group'] == 2])
    print("The Count of num 2 in Venn :", group_count_2)
    group_count_3 = len(df[df['group'] == 3])
    print("The Count of num 3 in Venn :", group_count_3)
    group_count_4 = len(df[df['group'] == 4])
    print("The Count of num 4 in Venn :", group_count_4)
    group_count_5 = len(df[df['group'] == 5])
    print("The Count of num 5 in Venn :", group_count_5)
    group_count_6 = len(df[df['group'] == 6])
    print("The Count of num 6 in Venn :", group_count_6)
    group_count_7 = len(df[df['group'] == 7])
    print("The Count of num 7 in Venn :", group_count_7)

def part_4(df):
    satisfied_Q = df[df[events['Q']]> 750].copy()
    satisfied_C = df[df[events['C']]< 222000].copy()
    satisfied_S = df[df[events['S']]< 15].copy()

    # a) Of those who satisfied Cost, what percentage also satisfied Quality?
    ans_a = satisfied_C[satisfied_C[events['Q']]>750]
    percent_a = len(ans_a)/len(satisfied_C)
    print("Answer 4.a : %.4f"%(percent_a))

    # b) Of those who satisfied Quality, what percentage also satisfied Speed?
    ans_b = satisfied_Q[satisfied_Q[events['S']]<15]
    percent_b = len(ans_b)/len(satisfied_Q)
    print("Answer 4.b : %.4f"%(percent_b))

    # c) Of those who satisfied Cost, what percentage also satisfied Speed but did not satisfy the Quality?
    def ans4_c_helper(s, q):
        if is_S(s) and not is_Q(q): return True
        return False

    satisfied_C['Ans4C'] = satisfied_C.apply(lambda x: ans4_c_helper(x[events['S']], x[events['Q']]),axis=1)
    ans_c = satisfied_C[satisfied_C['Ans4C']]
    percent_c = len(ans_c)/len(satisfied_C)
    print("Answer 4.c : %.4f"%(percent_c))

    # d) Of those who satisfied Speed, what percentage also satisfied Quality but did not satisfy the Cost?
    def ans4_d_helper(q, c):
        if is_Q(q) and not is_C(c): return True
        return False
    satisfied_S ['Ans4D'] = satisfied_S.apply(lambda x: ans4_d_helper(x[events['Q']], x[events['C']]), axis=1)
    ans_d = satisfied_S[satisfied_S['Ans4D']]
    percent_d = len(ans_d)/len(satisfied_S)
    print("Answer 4.d : %.4f" % (percent_d))

    # e) Of those who did not satisfy Speed, what percentage satisfied Quality and Cost?
    def ans4_e_helper(q,c):
        if is_Q(q) and is_C(c): return True
        return False
    not_satisfied_S = df[df[events['S']]>=15].copy()
    not_satisfied_S['Ans4E'] = not_satisfied_S.apply(lambda x: ans4_e_helper(x[events['Q']], x[events['C']]), axis=1)
    ans_e = not_satisfied_S[not_satisfied_S['Ans4E']]
    percent_e = len(ans_e)/len(not_satisfied_S)
    print("Answer 4.e : %.4f" % (percent_e))

    # f) What percentage satisfied at least two of the three criteria?
    def ans4_f_helper(q,s,c):
        if is_Q(q) and is_S(s) and not is_C(c): return True
        if is_Q(q) and is_C(c) and not is_S(s): return True
        if is_S(s) and is_C(c) and not is_Q(q): return True
        if is_Q(q) and is_C(c) and is_S(s): return True
        return False
    satisfied_at_least_two = df.copy()
    satisfied_at_least_two['Ans4F'] = satisfied_at_least_two.apply(lambda x:ans4_f_helper(x[events['Q']], x[events['S']], x[events['C']]), axis=1)
    ans_f = satisfied_at_least_two[satisfied_at_least_two['Ans4F']]
    percent_f = len(ans_f)/len(satisfied_at_least_two)
    print("Answer 4.f : %.4f" % (percent_f))

    # g) Of those who satisfied at least one of the three criteria, what percentage satisfied exactly one criterion?
    def ans4_g_helper(q,s,c):
        if is_Q(q) and not is_S(s) and not is_C(c): return True
        if is_C(c) and not is_Q(q) and not is_S(s): return True
        if is_S(s) and not is_C(c) and not is_Q(q): return True
        return False
    def ans4_g_helper1(q,s,c):
        if not is_Q(q) and not is_C(c) and not is_S(s): return False
        return True

    df['Least1'] = df.apply(lambda x: ans4_g_helper1(x[events['Q']],x[events['S']], x[events['C']]), axis=1)
    satisfied_at_least_one = df[df['Least1']].copy()
    satisfied_at_least_one['Ans4G'] = satisfied_at_least_one.apply(lambda x: ans4_g_helper(x[events['Q']],x[events['S']], x[events['C']]), axis=1)
    satisfied_one_in_at_least_one = satisfied_at_least_one[satisfied_at_least_one['Ans4G']]
    percent_g = len(satisfied_one_in_at_least_one)/len(satisfied_at_least_one)
    print("Answer 4.g : %.4f" % (percent_g))

    # h) Of those who did not satisfy Speed, what percentage satisfied the Cost criterion?
    def ans4_h_helper(c):
        if is_C(c): return True
        return False
    not_satisfied_S['Ans4H'] = not_satisfied_S.apply(lambda x: ans4_h_helper(x[events['C']]), axis=1)
    ans_h = not_satisfied_S[not_satisfied_S['Ans4H']]
    percent_h = len(ans_h)/len(not_satisfied_S)
    print("Answer 4.h : %.4f" % (percent_h))

if __name__ == '__main__':
    df = pd.read_csv('Performance_v3.csv')
    events = {
        'Q' : " Quality Score ",
        'S' : " Process Days ",
        'C' : " Project Cost "
    }
    part_1(df)
    part_2(df)
    part_3(df)
    part_4(df)
