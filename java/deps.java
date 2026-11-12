import java.io.IOException;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

// обход графа тестового репозитория в ширину без рекурсии
public class deps {

    static final int args_count = 5;

    // чтение файла, проверка формата и обход графа
    // File_Path - файл с описанием графа, Start_Name - анализируемый пакет,
    // Max_Depth - глубина, Filter_Text - подстрока для пропуска пакетов,
    // Reverse_Mode - искать обратные зависимости,
    // Comment_Char и Separator - символы комментария и двоеточия в файле,
    // Out и Err - потоки для вывода
    static int Run_Bfs(String File_Path, String Start_Name, int Max_Depth, String Filter_Text, boolean Reverse_Mode, String Comment_Char, String Separator, PrintStream Out, PrintStream Err) {
        List<String> Lines;
        try {
            Lines = new ArrayList<>(Files.readAllLines(Paths.get(File_Path), StandardCharsets.UTF_8));
        } catch (IOException e) {
            Err.println("Ошибка: не удалось прочитать файл " + File_Path);
            return 1;
        }
        // метку порядка байтов (BOM) в начале файла пропускаем
        if (!Lines.isEmpty() && Lines.get(0).startsWith("\uFEFF")) {
            Lines.set(0, Lines.get(0).substring(1));
        }
        // слишком большие файлы не читаем
        if (Lines.size() > 100000) {
            Err.println("Ошибка: слишком большой файл " + File_Path);
            return 1;
        }
        // разбор строк вида "A: B C"
        Map<String, List<String>> Repo = new LinkedHashMap<>();
        for (int i = 0; i < Lines.size(); i++) {
            String Line = Lines.get(i);
            int Comment_Pos = Line.indexOf(Comment_Char);
            if (Comment_Pos >= 0) {
                Line = Line.substring(0, Comment_Pos);
            }
            Line = Line.strip();
            if (Line.isEmpty()) {
                continue;
            }
            String Where = File_Path + ", строка " + (i + 1);
            int Colon_Pos = Line.indexOf(Separator);
            if (Colon_Pos < 0) {
                Err.println("Ошибка: " + Where + ": нет двоеточия после имени пакета");
                return 1;
            }
            String Package_Name = Line.substring(0, Colon_Pos).strip();
            String Rest = Line.substring(Colon_Pos + 1).strip();
            List<String> Deps = new ArrayList<>();
            if (!Rest.isEmpty()) {
                Deps.addAll(Arrays.asList(Rest.split("\\s+")));
            }
            List<String> All_Names = new ArrayList<>();
            All_Names.add(Package_Name);
            All_Names.addAll(Deps);
            for (String Item : All_Names) {
                if (!Item.matches("[A-Z]+")) {
                    Err.println("Ошибка: " + Where + ": имя пакета '" + Item + "' должно состоять из больших латинских букв");
                    return 1;
                }
            }
            if (Repo.containsKey(Package_Name)) {
                Err.println("Ошибка: " + Where + ": пакет " + Package_Name + " описан повторно");
                return 1;
            }
            if (new HashSet<>(Deps).size() != Deps.size()) {
                Err.println("Ошибка: " + Where + ": у пакета " + Package_Name + " повторяется зависимость");
                return 1;
            }
            Repo.put(Package_Name, Deps);
        }
        if (Repo.isEmpty()) {
            Err.println("Ошибка: в файле " + File_Path + " нет ни одного пакета");
            return 1;
        }
        // все зависимости должны быть описаны в файле
        for (Map.Entry<String, List<String>> Entry : Repo.entrySet()) {
            for (String Dep : Entry.getValue()) {
                if (!Repo.containsKey(Dep)) {
                    Err.println("Ошибка: пакет " + Dep + ", от которого зависит " + Entry.getKey() + ", не описан в файле " + File_Path);
                    return 1;
                }
            }
        }
        if (!Repo.containsKey(Start_Name)) {
            Err.println("Ошибка: пакет " + Start_Name + " не описан в файле " + File_Path);
            return 1;
        }
        // для обратных зависимостей разворачиваем все ребра
        Map<String, List<String>> Graph = Repo;
        if (Reverse_Mode) {
            Graph = new LinkedHashMap<>();
            for (String Name : Repo.keySet()) {
                Graph.put(Name, new ArrayList<>());
            }
            for (Map.Entry<String, List<String>> Entry : Repo.entrySet()) {
                for (String Dep : Entry.getValue()) {
                    Graph.get(Dep).add(Entry.getKey());
                }
            }
        }
        // обход в ширину: очередь и глубина каждого пакета
        Map<String, Integer> Depth = new HashMap<>();
        Depth.put(Start_Name, 0);
        ArrayDeque<String> Queue = new ArrayDeque<>();
        Queue.add(Start_Name);
        while (!Queue.isEmpty()) {
            String Current = Queue.poll();
            if (Depth.get(Current) >= Max_Depth) {
                continue;
            }
            List<String> Result = new ArrayList<>();
            for (String Dep : Graph.get(Current)) {
                if (!Filter_Text.isEmpty() && Dep.contains(Filter_Text)) {
                    continue;
                }
                Result.add(Dep);
                if (!Depth.containsKey(Dep)) {
                    Depth.put(Dep, Depth.get(Current) + 1);
                    Queue.add(Dep);
                }
            }
            Out.print((Current + ": " + String.join(" ", Result)).stripTrailing() + "\n");
        }
        Out.flush();
        return 0;
    }

    // разбор аргументов командной строки и запуск обхода
    public static void main(String[] args) {
        if (args.length != args_count) {
            System.err.println("Использование: java -cp java/out deps <файл репозитория> <пакет> <глубина> <фильтр или -> <forward или reverse>");
            System.exit(1);
        }
        int Max_Depth;
        try {
            Max_Depth = Integer.parseInt(args[2]);
        } catch (NumberFormatException e) {
            Max_Depth = 0;
        }
        if (Max_Depth < 1 || Max_Depth > 100) {
            System.err.println("Ошибка: глубина анализа должна быть целым числом от 1 до 100");
            System.exit(1);
        }
        if (!args[4].equals("forward") && !args[4].equals("reverse")) {
            System.err.println("Ошибка: направление должно быть forward или reverse");
            System.exit(1);
        }
        String Filter_Text = args[3].equals("-") ? "" : args[3];
        if (!Filter_Text.isEmpty() && args[1].contains(Filter_Text)) {
            System.err.println("Ошибка: анализируемый пакет " + args[1] + " сам содержит подстроку " + Filter_Text);
            System.exit(1);
        }
        System.exit(Run_Bfs(args[0], args[1], Max_Depth, Filter_Text, args[4].equals("reverse"), "#", ":", System.out, System.err));
    }
}
