while True:
    supply,motor,cable=(int(x) for x in input().split())
    if supply==0 and motor==0:
        break
    checknum=int(input())
    
    reslist=[2]*(supply+motor+cable)
    stack=[]
    for i in range(checknum):
        no1,no2,no3,result=(int(x)-1 for x in input().split())
        result+=1
        if result==1:
            reslist[no1], reslist[no2], reslist[no3]=1,1,1
        else:
            stack.append((no1,no2,no3))

    for i in range(len(stack)):
        t=stack[i]
        no1,no2,no3=t[0],t[1],t[2]
        if reslist[no1]==1 and reslist[no2]==1:
            reslist[no3]=0
        elif reslist[no3]==1 and reslist[no2]==1:
            reslist[no1]=0
        elif reslist[no3]==1 and reslist[no1]==1:
            reslist[no2]=0
            
    for i in range(len(reslist)):
        print(reslist[i])