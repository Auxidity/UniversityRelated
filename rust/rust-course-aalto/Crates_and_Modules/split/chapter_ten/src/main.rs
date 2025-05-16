use application::quiz::practice_problems;

fn main() {
    let problems = [
        ("What is the capital of Finland?", "Helsinki"),
        ("What is the capital of Sweden?", "Stockholm"),
        ("What is the capital of Norway?", "Oslo"),
        ("What is the capital of Estonia?", "Tallinn"),
        ("What is the capital of Denmark?", "Kopenhagen"),
        ("What is the capital of Iceland?", "Reykjavik"),
        ("What is the capital of Latvia?", "Riga"),
        ("What is the capital of Lithuania?", "Vilnius"),
        ("What is the capital of France?", "Paris"),
        ("What is the capital of Germany?", "Berlin"),
        ("What is the capital of Italy?", "Rome"),
        ("What is the capital of Spain?", "Madrid"),
        ("What is the capital of the United Kingdom?", "London"),
        ("What is the capital of Ireland?", "Dublin"),
    ];
    practice_problems(&problems);
}
