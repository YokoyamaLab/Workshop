import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {

        Scanner scan = new Scanner(System.in);
        
        while(true){
            //parts number
            int supply = scan.nextInt();
            int motor = scan.nextInt();
            int cable = scan.nextInt();
            if (supply==0){
                break;
            }
            

            int len = scan.nextInt();
            int[] res = new int[supply+motor+cable];
			Arrays.fill(res, 2);
			ArrayList<Integer> intList = new ArrayList<Integer>();
            int len2 = 0;
            
            // pass 
            for (int i=0; i<len; i++){
                int no1 = scan.nextInt()-1;
                int no2 = scan.nextInt()-1;
                int no3 = scan.nextInt()-1;
                int ans = scan.nextInt();
                if (ans==1){
                    res[no1]=1;
                    res[no2]=1;
                    res[no3]=1;
                }else{
                    intList.add(no1);
                    intList.add(no2);
                    intList.add(no3);
                    len2+=3;
                }
            }
            
            //not pass
            for (int i=0; i<len2; i+=3){
                int no1 = intList.get(i);
                int no2 = intList.get(i+1);
                int no3 = intList.get(i+2);
                if (res[no1]==1 && res[no2]==1){
                    res[no3]=0;
                }
                else if (res[no3]==1 && res[no2]==1){
                    res[no1]=0;
                }
                else if (res[no1]==1 && res[no3]==1){
                    res[no2]=0;
                }
            }
            
            for (int i=0;i<supply+motor+cable; i++){
                System.out.println(res[i]);
            }
            
            
        }
    }
}
