#!/bin/sh
# сборка реализаций обхода на Java, Kotlin, C#, Go и Rust
# (JavaScript и Python сборки не требуют)
cd "$(dirname "$0")" || exit 1

if command -v javac > /dev/null; then
    echo "Java: javac"
    javac -d java/out java/deps.java
else
    echo "Java: javac не найден, сборка пропущена"
fi
if command -v kotlinc > /dev/null; then
    echo "Kotlin: kotlinc"
    kotlinc kotlin/deps.kt -include-runtime -d kotlin/deps.jar
else
    echo "Kotlin: kotlinc не найден, сборка пропущена"
fi
if command -v dotnet > /dev/null; then
    echo "C#: dotnet build"
    dotnet build csharp -c Release --nologo -v q
else
    echo "C#: dotnet не найден, сборка пропущена"
fi
if command -v go > /dev/null; then
    echo "Go: go build"
    (cd go && go build -trimpath -o deps .)
else
    echo "Go: go не найден, сборка пропущена"
fi
if command -v rustc > /dev/null; then
    echo "Rust: rustc"
    rustc -O -C strip=symbols -o rust/deps rust/deps.rs
else
    echo "Rust: rustc не найден, сборка пропущена"
fi
