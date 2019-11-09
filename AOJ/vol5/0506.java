// パッケージインポート
import java.util.*;

class Main0506 {
    // mainメソッド
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in); // 入力受取準備

        while(true) {
            int n = s.nextInt(); // int型の入力値はnextInt()で受け取り
            if (n == 0) {
                System.exit(0); // Javaの処理自体を終了させる
            }
            String str = s.next(); // String型の入力値はnext()で受け取り

            for (int i = 0; i < n; i++) {
                char now = str.charAt(0); // 入力された初期文字列から0番目の文字を取り出す
                int times = 0; // 数え上げ用の値
                StringBuffer next = new StringBuffer(""); // 操作可能な文字列StringBuffer型の""を定義

                for (int j = 0; j < str.length(); j++) {
                    if (now == str.charAt(j)) {
                        times++;
                    } else {
                        next.append(times + "" + now); // 文字列結合
                        now = str.charAt(j);
                        times = 1;
                    }
                }

                if (times > 0) {
                    // 最後の文字のカウント数とその文字自体を結合
                    next.append(times + "" + now);
                    str = next.toString(); // StringBuffer型をString型に変換
                }
            }
            System.out.println(str);
        }
    }
}