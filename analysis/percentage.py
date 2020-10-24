def percentage(P: dict, N: dict, I: dict, none: dict):
    """
    接收要处理的四个 字典 注意：接收者四个字典的时候，一定要按顺序
    将字典的里面统计的微博的条数，转换成百分比
    :return total列表
    列表以此存储处理好的四个字典
    """
    P_percentage = {}
    N_percentage = {}
    I_percentage = {}
    none_percentage = {}
    total = []
    for i in P.keys():
        if P[i] == 0 and N[i] == 0 :
            i+=1
        P_percentage[i] = P[i] / (P[i] + N[i])
        N_percentage[i] = N[i] / (P[i] + N[i])

    for i in I.keys():
        if I[i] == 0 and none[i] == 0 :
            i+=1
        I_percentage[i] = I[i] / (I[i] + none[i])
        none_percentage[i] = none[i] / (I[i] + none[i])
    total.append(P_percentage)
    total.append(N_percentage)
    total.append(I_percentage)
    total.append(none_percentage)
    return total
