import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {

        Scanner scan = new Scanner(System.in);
        int  num = scan.nextInt();
        
        while(num != 0){
            //make a dictionaly
            String d_b[] = new String[num];
            String d_a[] = new String[num];
            for (int i=0; i<num; i++){
                d_b[i] = scan.next();
                d_a[i] = scan.next();
            }
            
            //read a sentence
            int len = scan.nextInt();
            String sentence[] = new String[len];
            for (int i=0; i<len; i++){
                sentence[i] = scan.next();
            }
            
            //change a sentence
            for (int i=0; i<len; i++){
                for (int j=0; j<num; j++){
                    if(sentence[i].equals(d_b[j])){//ccan't use ==
                        sentence[i] = d_a[j];
                        break;
                    }
                }
            }
            String str = String.join("", sentence);
            
            System.out.println(str);
            
            num = scan.nextInt();
        }
    }
}
