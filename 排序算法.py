def merge(A, B):
    '''
    合并两个已排序数组
    思路:
        分别定义i,j两个整形变量,作为指针, 指向当前A, B数组位置
        循环比较A[i], B[j]位置上的值,小的则提取值放在结果数据, 同时对应的指针+1
        另一个的指针不变.

    Args:
        list A:一个已排序数组
        list B:一个已排序数组

    Returns:
        result:一个已经排序的数组
    '''

    #将要返回的结果数组
    result = []
    #分别为A,B两个数组的遍历指针, 初始指向为0索引位置
    i, j = 0, 0
    while i<len(A) and j<len(B):
        if A[i]<B[j]:
            result.append(A[i])
            i += 1
        else:
            result.append(B[j])
            j += 1
    result += A[i:]
    result += B[j:]
    return result


count=count1+count2
        llist=[]
        for i in range(0,count1):
            ttuple=(parking_financials[i].paring_end_time,parking_financials[i].charge_cost,parking_financials[i].parking_cost,parking_financials[i].total_price,garage_name)
            llist.append(ttuple)
        for j in range(count1+1,count)
            ttuple2=(records[j].recharge_time,records[j].recharge_num,records[j].red_packet)
            llist.append(ttuple2)
        end_list=sorted(llist,key=itemgetter(0),reverse=True)
        for k in range(0,count):
            end_list[k]=list(endlist[k])
