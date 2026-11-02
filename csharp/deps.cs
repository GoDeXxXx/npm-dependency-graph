using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

// обход графа тестового репозитория в ширину без рекурсии
class deps_tool
{
    const int args_count = 5;

    // чтение файла, проверка формата и обход графа
    // File_Path - файл с описанием графа, Start_Name - анализируемый пакет,
    // Max_Depth - глубина, Filter_Text - подстрока для пропуска пакетов,
    // Reverse_Mode - искать обратные зависимости,
    // Comment_Char и Separator - символы комментария и двоеточия в файле,
    // Out и Err - потоки для вывода
    static int run_bfs(string File_Path, string Start_Name, int Max_Depth, string Filter_Text, bool Reverse_Mode, string Comment_Char, string Separator, TextWriter Out, TextWriter Err)
    {
        string[] Lines;
        try
        {
            Lines = File.ReadAllLines(File_Path);
        }
        catch (Exception)
        {
            Err.WriteLine("Ошибка: не удалось прочитать файл " + File_Path);
            return 1;
        }
        // слишком большие файлы не читаем
        if (Lines.Length > 100000)
        {
            Err.WriteLine("Ошибка: слишком большой файл " + File_Path);
            return 1;
        }
        // разбор строк вида "A: B C", порядок пакетов храним отдельно
        var Repo = new Dictionary<string, List<string>>();
        var Names = new List<string>();
        for (int i = 0; i < Lines.Length; i++)
        {
            string Line = Lines[i];
            int Comment_Pos = Line.IndexOf(Comment_Char, StringComparison.Ordinal);
            if (Comment_Pos >= 0)
            {
                Line = Line.Substring(0, Comment_Pos);
            }
            Line = Line.Trim();
            if (Line.Length == 0)
            {
                continue;
            }
            string Where = File_Path + ", строка " + (i + 1);
            int Colon_Pos = Line.IndexOf(Separator, StringComparison.Ordinal);
            if (Colon_Pos < 0)
            {
                Err.WriteLine("Ошибка: " + Where + ": нет двоеточия после имени пакета");
                return 1;
            }
            string Package_Name = Line.Substring(0, Colon_Pos).Trim();
            var Deps = Regex.Split(Line.Substring(Colon_Pos + 1), @"\s+").Where(Item => Item.Length > 0).ToList();
            foreach (string Item in new[] { Package_Name }.Concat(Deps))
            {
                if (!Regex.IsMatch(Item, "^[A-Z]+$"))
                {
                    Err.WriteLine("Ошибка: " + Where + ": имя пакета '" + Item + "' должно состоять из больших латинских букв");
                    return 1;
                }
            }
            if (Repo.ContainsKey(Package_Name))
            {
                Err.WriteLine("Ошибка: " + Where + ": пакет " + Package_Name + " описан повторно");
                return 1;
            }
            if (Deps.Distinct().Count() != Deps.Count)
            {
                Err.WriteLine("Ошибка: " + Where + ": у пакета " + Package_Name + " повторяется зависимость");
                return 1;
            }
            Repo[Package_Name] = Deps;
            Names.Add(Package_Name);
        }
        if (Names.Count == 0)
        {
            Err.WriteLine("Ошибка: в файле " + File_Path + " нет ни одного пакета");
            return 1;
        }
        // все зависимости должны быть описаны в файле
        foreach (string Package_Name in Names)
        {
            foreach (string Dep in Repo[Package_Name])
            {
                if (!Repo.ContainsKey(Dep))
                {
                    Err.WriteLine("Ошибка: пакет " + Dep + ", от которого зависит " + Package_Name + ", не описан в файле " + File_Path);
                    return 1;
                }
            }
        }
        if (!Repo.ContainsKey(Start_Name))
        {
            Err.WriteLine("Ошибка: пакет " + Start_Name + " не описан в файле " + File_Path);
            return 1;
        }
        // для обратных зависимостей разворачиваем все ребра
        var Graph = Repo;
        if (Reverse_Mode)
        {
            Graph = new Dictionary<string, List<string>>();
            foreach (string Package_Name in Names)
            {
                Graph[Package_Name] = new List<string>();
            }
            foreach (string Package_Name in Names)
            {
                foreach (string Dep in Repo[Package_Name])
                {
                    Graph[Dep].Add(Package_Name);
                }
            }
        }
        // обход в ширину: очередь и глубина каждого пакета
        var Depth = new Dictionary<string, int> { [Start_Name] = 0 };
        var Queue = new Queue<string>();
        Queue.Enqueue(Start_Name);
        while (Queue.Count > 0)
        {
            string Current = Queue.Dequeue();
            if (Depth[Current] >= Max_Depth)
            {
                continue;
            }
            var Result = new List<string>();
            foreach (string Dep in Graph[Current])
            {
                if (Filter_Text.Length > 0 && Dep.Contains(Filter_Text))
                {
                    continue;
                }
                Result.Add(Dep);
                if (!Depth.ContainsKey(Dep))
                {
                    Depth[Dep] = Depth[Current] + 1;
                    Queue.Enqueue(Dep);
                }
            }
            Out.Write((Current + ": " + string.Join(" ", Result)).TrimEnd() + "\n");
        }
        Out.Flush();
        return 0;
    }

    // разбор аргументов командной строки и запуск обхода
    static int Main(string[] args)
    {
        if (args.Length != args_count)
        {
            Console.Error.WriteLine("Использование: dotnet csharp/bin/deps.dll <файл репозитория> <пакет> <глубина> <фильтр или -> <forward или reverse>");
            return 1;
        }
        if (!int.TryParse(args[2], out int Max_Depth) || Max_Depth < 1 || Max_Depth > 100)
        {
            Console.Error.WriteLine("Ошибка: глубина анализа должна быть целым числом от 1 до 100");
            return 1;
        }
        if (args[4] != "forward" && args[4] != "reverse")
        {
            Console.Error.WriteLine("Ошибка: направление должно быть forward или reverse");
            return 1;
        }
        string Filter_Text = args[3] == "-" ? "" : args[3];
        if (Filter_Text.Length > 0 && args[1].Contains(Filter_Text))
        {
            Console.Error.WriteLine("Ошибка: анализируемый пакет " + args[1] + " сам содержит подстроку " + Filter_Text);
            return 1;
        }
        return run_bfs(args[0], args[1], Max_Depth, Filter_Text, args[4] == "reverse", "#", ":", Console.Out, Console.Error);
    }
}
