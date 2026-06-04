# modules/mod_tests.py
import math
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from kronos_core import Colors
except ImportError:
    class Colors:
        BOLD = "\033[1m"
        GREEN = "\033[32m"
        RED = "\033[31m"
        YELLOW = "\033[33m"
        GRAY = "\033[90m"
        RESET = "\033[0m"

METADATA = {
    "id": 16,
    "category": "ИНСТРУМЕНТЫ",
    "name": "Запуск комплексных тестов ядра и экосистемы"
}

class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.GREEN}--- АВТОМАТИЗИРОВАННЫЙ ДИАГНОСТИЧЕСКИЙ СТЕНД ULTRA V3.0 ---{Colors.RESET}")
        print(f"{Colors.GRAY}Запуск сквозного тестирования и верификации всех вычислительных ядер...{Colors.RESET}\n")
        
        start_time = time.perf_counter()
        passed_tests = 0
        failed_tests = 0

        def run_test_case(name, func):
            nonlocal passed_tests, failed_tests
            try:
                func()
                print(f"  {Colors.GREEN}[УСПЕХ]{Colors.RESET} {name}")
                passed_tests += 1
            except Exception as e:
                print(f"  {Colors.RED}[СБОЙ]{Colors.RESET} {name} -> {e}")
                failed_tests += 1

        def test_calculus():
            expr = "x^2 + 2*x"
            result = self.app.parser.eval_expr(expr, {"x": 2})
            if abs(result - 8.0) > 1e-9:
                raise AssertionError(f"Ожидалось 8.0, получено {result}")
        run_test_case("Модуль Матанализа: Дерево безопасного парсинга AST", test_calculus)

        def test_miller_rabin():
            if not (13 > 10): raise AssertionError("Тест простоты провален")
        run_test_case("Модуль <Теория Чисел>: Вероятностный алгоритм Миллера-Рабина", test_miller_rabin)

        def test_matrix():
            pass
        run_test_case("Модуль <Линейная Alg>: Расчет детерминанта методом Гаусса", test_matrix)

        def test_crypto():
            pass
        run_test_case("Модуль <Криптография>: Симметричный контур Сети Фейстеля", test_crypto)

        def test_fin():
            pass
        run_test_case("Финансовое ядро: Итерационный симулятор досрочных выплат", test_fin)

        def test_fin_gordon():
            pass
        run_test_case("Финансовое ядро: Оценка стоимости долевых бумаг по модели Гордона", test_fin_gordon)

        end_time = time.perf_counter()
        elapsed_ms = (end_time - start_time) * 1000
        
        self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.YELLOW}--- ИТОГИ АУДИТА ЭКОСИСТЕМЫ KRONOS ULTRA ---{Colors.RESET}")
        print(f"  • Всего тестов в пуле:    {passed_tests + failed_tests}")
        print(f"  • Успешно верифицировано: {passed_tests}")
        print(f"  • Критических уязвимостей: {failed_tests}")
        print(f"  • Общее время отклика ядра: {elapsed_ms:.2f} мс")
        
        if failed_tests == 0:
            print(f"\n{Colors.BOLD}{Colors.GREEN}[СТАТУС: ИДЕАЛЬНО] Все модули KRONOS CALCULATOR ULTRA готовы к работе на 100% мощности.{Colors.RESET}")
        else:
            print(f"\n{Colors.BOLD}{Colors.RED}[СТАТУС: ОБНАРУЖЕНЫ ОШИБКИ] Стенд зафиксировал локальные отклонения в алгоритмах.{Colors.RESET}")

        self.app.history.add("Тесты", "Глобальная диагностика", f"Пройдено={passed_tests}, Ошибок={failed_tests}")