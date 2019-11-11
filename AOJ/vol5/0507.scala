object Main extends App{
    var card=Array(0)
    for{i<-1 to 30}{
        card = card :+ 0
    }

    var num=io.StdIn.readLine().toInt
    while(num>0){
        rec(0,num,num)
        num=io.StdIn.readLine().toInt
    }
    
    def rec(row:Int,left:Int,now:Int):Unit={
        var now2=now
        if (left==0){
            for{i<-0 to row-2}{
                print(card(i))
                print(" ")
            }
            println(card(row-1))
            return
        }
        if (left<now){
            now2=left
        }
        var i=now2
        while(i>0){
            card(row)=i
            rec(row+1,left-i,i)
            i -= 1
        }
    }
}
