import java.io.File
import java.io.PrintStream
import kotlin.system.exitProcess

const val args_count = 5
val Name_Regex = Regex("[A-Z]+")

// обход графа тестового репозитория в ширину без рекурсии
// File_Path - файл с описанием графа, Start_Name - анализируемый пакет,
// Max_Depth - глубина, Filter_Text - подстрока для пропуска пакетов,
// Reverse_Mode - искать обратные зависимости,
// Comment_Char и Separator - символы комментария и двоеточия в файле,
// Out и Err - потоки для вывода
fun Run_Bfs(File_Path: String, Start_Name: String, Max_Depth: Int, Filter_Text: String, Reverse_Mode: Boolean, Comment_Char: String, Separator: String, Out: PrintStream, Err: PrintStream): Int {
    val Lines: List<String>
    try {
        Lines = File(File_Path).readLines(Charsets.UTF_8)
    } catch (e: Exception) {
        Err.println("Ошибка: не удалось прочитать файл $File_Path")
        return 1
    }
    // слишком большие файлы не читаем
    if (Lines.size > 100000) {
        Err.println("Ошибка: слишком большой файл $File_Path")
        return 1
    }
    // разбор строк вида "A: B C"
    val Repo = LinkedHashMap<String, List<String>>()
    for (i in Lines.indices) {
        var Line = Lines[i]
        val Comment_Pos = Line.indexOf(Comment_Char)
        if (Comment_Pos >= 0) {
            Line = Line.substring(0, Comment_Pos)
        }
        Line = Line.trim()
        if (Line.isEmpty()) {
            continue
        }
        val Where = "$File_Path, строка ${i + 1}"
        val Colon_Pos = Line.indexOf(Separator)
        if (Colon_Pos < 0) {
            Err.println("Ошибка: $Where: нет двоеточия после имени пакета")
            return 1
        }
        val Package_Name = Line.substring(0, Colon_Pos).trim()
        val Deps = Line.substring(Colon_Pos + 1).split(Regex("\\s+")).filter { it.isNotEmpty() }
        for (Item in listOf(Package_Name) + Deps) {
            if (!Name_Regex.matches(Item)) {
                Err.println("Ошибка: $Where: имя пакета '$Item' должно состоять из больших латинских букв")
                return 1
            }
        }
        if (Repo.containsKey(Package_Name)) {
            Err.println("Ошибка: $Where: пакет $Package_Name описан повторно")
            return 1
        }
        if (Deps.toSet().size != Deps.size) {
            Err.println("Ошибка: $Where: у пакета $Package_Name повторяется зависимость")
            return 1
        }
        Repo[Package_Name] = Deps
    }
    if (Repo.isEmpty()) {
        Err.println("Ошибка: в файле $File_Path нет ни одного пакета")
        return 1
    }
    // все зависимости должны быть описаны в файле
    for ((Package_Name, Deps) in Repo) {
        for (Dep in Deps) {
            if (!Repo.containsKey(Dep)) {
                Err.println("Ошибка: пакет $Dep, от которого зависит $Package_Name, не описан в файле $File_Path")
                return 1
            }
        }
    }
    if (!Repo.containsKey(Start_Name)) {
        Err.println("Ошибка: пакет $Start_Name не описан в файле $File_Path")
        return 1
    }
    // для обратных зависимостей разворачиваем все ребра
    var Graph: Map<String, List<String>> = Repo
    if (Reverse_Mode) {
        val Reversed = LinkedHashMap<String, MutableList<String>>()
        for (Name in Repo.keys) {
            Reversed[Name] = mutableListOf()
        }
        for ((Package_Name, Deps) in Repo) {
            for (Dep in Deps) {
                Reversed.getValue(Dep).add(Package_Name)
            }
        }
        Graph = Reversed
    }
    // обход в ширину: очередь и глубина каждого пакета
    val Depth = HashMap<String, Int>()
    Depth[Start_Name] = 0
    val Queue = ArrayDeque<String>()
    Queue.addLast(Start_Name)
    while (Queue.isNotEmpty()) {
        val Current = Queue.removeFirst()
        if (Depth.getValue(Current) >= Max_Depth) {
            continue
        }
        val Result = mutableListOf<String>()
        for (Dep in Graph.getValue(Current)) {
            if (Filter_Text.isNotEmpty() && Dep.contains(Filter_Text)) {
                continue
            }
            Result.add(Dep)
            if (!Depth.containsKey(Dep)) {
                Depth[Dep] = Depth.getValue(Current) + 1
                Queue.addLast(Dep)
            }
        }
        Out.print(("$Current: " + Result.joinToString(" ")).trimEnd() + "\n")
    }
    Out.flush()
    return 0
}

// разбор аргументов командной строки и запуск обхода
fun main(args: Array<String>) {
    if (args.size != args_count) {
        System.err.println("Использование: java -jar kotlin/deps.jar <файл репозитория> <пакет> <глубина> <фильтр или -> <forward или reverse>")
        exitProcess(1)
    }
    val Max_Depth = args[2].toIntOrNull() ?: 0
    if (Max_Depth < 1 || Max_Depth > 100) {
        System.err.println("Ошибка: глубина анализа должна быть целым числом от 1 до 100")
        exitProcess(1)
    }
    if (args[4] != "forward" && args[4] != "reverse") {
        System.err.println("Ошибка: направление должно быть forward или reverse")
        exitProcess(1)
    }
    val Filter_Text = if (args[3] == "-") "" else args[3]
    if (Filter_Text.isNotEmpty() && args[1].contains(Filter_Text)) {
        System.err.println("Ошибка: анализируемый пакет ${args[1]} сам содержит подстроку $Filter_Text")
        exitProcess(1)
    }
    exitProcess(Run_Bfs(args[0], args[1], Max_Depth, Filter_Text, args[4] == "reverse", "#", ":", System.out, System.err))
}
