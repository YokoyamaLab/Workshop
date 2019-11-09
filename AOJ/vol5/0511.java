import java.util.*;

class Main0511 {
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        // 出席番号，入力値をそれぞれ保存するArrayList配列
        // 可変長配列ArrayListは要素追加や削除などの操作ができる
        ArrayList<Integer> students = new ArrayList<Integer>();
        ArrayList<Integer> inputs = new ArrayList<Integer>();

        for (int i = 1; i <= 30; i++) {
            students.add(i);
        }

        while(true) {
            // int型の入力値受け取り
            int number = scan.nextInt();
            inputs.add(number);

            for (int i = 0; i < students.size(); i++) {
                if (students.get(i) == number) {
                    students.set(i, 0);
                }
            }

            if (inputs.size() == 28) {
                break;
            }
        }
        for (int i = 0; i < students.size(); i++) {
            if (students.get(i) != 0) {
                System.out.println(students.get(i));
            }
        }
    }
}