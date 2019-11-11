while True:
    gyou, jump = (int(x) for x in input().split())
    if gyou==0 and jump==0:
        break
    #石の個数、配置と危険度
    stone=[]
    for i in range(gyou):
        a=input().split()
        a=[int(s) for s in a]
        stone.append(a)
    #危険度表を空の辞書として定義
    danger_now=[dict() for _ in [0]*(jump+1)]#現在の行までの最小危険度表
    danger_one=[dict() for _ in [0]*(jump+1)]#1行先までの最小危険度表
    danger_two=[dict() for _ in [0]*(jump+1)]#2行先までの最小危険度表
   
    #石の配置とすべりやすさを辞書化
    nows=[dict() for _ in [0]*gyou]
    for i in range(gyou):
        stone_num=stone[i][0]
        for k in range(stone_num):
            nows[i][stone[i][2*k+1]]=stone[i][2*k+2]
    
    for i in range(stone[0][0]):#最初の1行をwalk
        danger_now[0][stone[0][2*i+1]]=0
    if jump>=1:
        for i in range(stone[1][0]):#最初の1行をjump
            danger_one[1][stone[1][2*i+1]]=0
   
    #ここからDP開始
    for k in range(gyou-1):#行をn-1回分繰り返す
        #walkでの距離計算
        for l in range(jump+1):#その行までのジャンプ回数が0回からjump回までの場合について考える
            for i,j in danger_now[l].items():#iは現在位置、jはそれまでの最小危険度
                for x,y in nows[k+1].items():#xは移動先、yは移動先の滑りやすさ
                    plus=j+(nows[k][i]+y)*abs(i-x)
                    if x in danger_one[l].keys():#すでに到達していた場合
                        danger_one[l][x]=min(danger_one[l][x],plus)
                    else:#未到達だった場合
                        danger_one[l][x]=plus
        if k==gyou-2:
            continue
        #jumpでの距離計算
        for l in range(jump):#その行までのジャンプ回数が0回からjump-1回までの場合について考える
            for i,j in danger_now[l].items():
                for x,y in nows[k+2].items():
                    plus=j+(nows[k][i]+y)*abs(i-x)
                    if x in danger_two[l+1].keys():#ジャンプをするのでlの格納先はl+1
                        danger_two[l+1][x]=min(danger_two[l+1][x],plus)
                    else:
                        danger_two[l+1][x]=plus
        
        danger_now=danger_one
        danger_one=danger_two
        danger_two=[dict() for _ in [0]*(jump+1)]

    cost=10**8
    for i in danger_now[:-1]:#最後はwalk
        if len(i.values())>0:
            cost=min(cost,min(i.values()))#最後の行に石がない場合、デフォルト値(10**8)を返す
    for i in danger_one:#最後はjump
        if len(i.values())>0:
            cost=min(cost,min(i.values()))
    
    print(cost)
    