# modules/mod_matrix.py
from kronos_core import Colors

METADATA = {
    "id": 3,
    "category": "АЛГЕБРА И ГЕОМЕТРИЯ",
    "name": "Линейная алгебра (Матричный Процессор и СЛАУ)"
}

class MatrixProcessor:
    @staticmethod
    def transpose(A: list[list[float]]) -> list[list[float]]:
        return [[A[r][c] for r in range(len(A))] for c in range(len(A[0]))]

    @staticmethod
    def multiply(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
        if len(A[0]) != len(B):
            raise ValueError("Размерности матриц несогласованы для умножения!")
        
        rows_A, cols_A = len(A), len(A[0])
        cols_B = len(B[0])
        
        result = [[0.0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                result[i][j] = sum(A[i][k] * B[k][j] for k in range(cols_A))
        return result

    @staticmethod
    def determinant(matrix: list[list[float]]) -> float:
        n = len(matrix)
        if n != len(matrix[0]):
            raise ValueError("Определитель можно вычислить только для квадратной матрицы!")
        
        if n == 1: return matrix[0][0]
        if n == 2: return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        M = [row[:] for row in matrix]
        det = 1.0
        
        for i in range(n):
            pivot_row = i
            for r in range(i + 1, n):
                if abs(M[r][i]) > abs(M[pivot_row][i]): pivot_row = r
            if pivot_row != i:
                M[i], M[pivot_row] = M[pivot_row], M[i]
                det *= -1.0
                
            if abs(M[i][i]) < 1e-11: return 0.0
                
            det *= M[i][i]
            for r in range(i + 1, n):
                factor = M[r][i] / M[i][i]
                for c in range(i, n):
                    M[r][c] -= factor * M[i][c]
        return det


class KronosPlugin:
    def __init__(self, app) -> None:
        self.app = app

    def _read_matrix(self, rows: int, cols: int, name: str) -> list[list[float]]:
        print(f"  {Colors.GRAY}Заполнение матрицы {name} ({rows}x{cols}) построчно через пробел:{Colors.RESET}")
        matrix = []
        for i in range(rows):
            while True:
                try:
                    inp = self.app.ui.get_input(f"    Строка {i+1}: ", str).strip()
                    row = [float(x) for x in inp.split()]
                    if len(row) != cols:
                        self.app.ui.print_error(f"Ошибка: ожидалось ровно {cols} чисел.")
                        continue
                    matrix.append(row)
                    break
                except ValueError:
                    self.app.ui.print_error("Ошибка: некорректный формат чисел.")
        return matrix

    def execute(self) -> None:
        self.app.ui.print_smart(f"{Colors.BOLD}{Colors.CYAN}--- ВЫЧИСЛИТЕЛЬНЫЙ МАТРИЧНЫЙ ПРОЦЕССОР ULTRA V3.0 ---{Colors.RESET}")
        print(" Доступные операции:")
        print("  [1] Транспонирование матрицы")
        print("  [2] Матричное умножение (A × B)")
        print("  [3] Решение систем линейных уравнений (Метод Гаусса)")
        print("  [4] Сложение / Вычитание матриц")
        
        choice = self.app.ui.get_input("\nВыберите тип операции: ", int, lambda x: 1 <= x <= 4)
        
        try:
            if choice == 1:
                r = self.app.ui.get_input("Количество строк: ", int, lambda x: x > 0)
                c = self.app.ui.get_input("Количество столбцов: ", int, lambda x: x > 0)
                A = self._read_matrix(r, c, "A")
                res = MatrixProcessor.transpose(A)
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТ ТРАНСПОНИРОВАНИЯ]:{Colors.RESET}")
                for row in res: print("   " + " ".join(f"{x:<8.4g}" for x in row))
                self.app.history.add("Матрицы", f"Транспонирование {r}x{c}", "Успешно")

            elif choice == 2:
                rA = self.app.ui.get_input("Строк матрицы A: ", int, lambda x: x > 0)
                cA = self.app.ui.get_input("Столбцов матрицы A: ", int, lambda x: x > 0)
                rB = self.app.ui.get_input(f"Строк матрицы B (должно быть {cA}): ", int, lambda x: x == cA)
                cB = self.app.ui.get_input("Столбцов матрицы B: ", int, lambda x: x > 0)
                
                A = self._read_matrix(rA, cA, "A")
                B = self._read_matrix(rB, cB, "B")
                
                res = MatrixProcessor.multiply(A, B)
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТ УМНОЖЕНИЯ A × B]:{Colors.RESET}")
                for row in res: print("   " + " ".join(f"{x:<8.4g}" for x in row))
                self.app.history.add("Матрицы", f"Умножение {rA}x{cA} на {rB}x{cB}", "Успешно")

            elif choice == 3:
                print(f"\n{Colors.YELLOW}--- РЕШЕНИЕ СЛАУ МЕТОДОМ ГАУССА ---{Colors.RESET}")
                n = self.app.ui.get_input("Количество неизвестных (размерность системы): ", int, lambda x: x > 0)
                aug = []
                for i in range(n):
                    while True:
                        try:
                            inp = self.app.ui.get_input(f"    Уравнение {i+1}: ", str).strip()
                            row = [float(x) for x in inp.split()]
                            if len(row) != n + 1: continue
                            aug.append(row)
                            break
                        except ValueError: continue
                
                for i in range(n):
                    pivot = i
                    for r in range(i + 1, n):
                        if abs(aug[r][i]) > abs(aug[pivot][i]): pivot = r
                    aug[i], aug[pivot] = aug[pivot], aug[i]
                    
                    if abs(aug[i][i]) < 1e-11:
                        self.app.ui.print_error("Матрица вырождена или система несовместна!")
                        return
                    for r in range(i + 1, n):
                        factor = aug[r][i] / aug[i][i]
                        for c in range(i, n + 1): aug[r][c] -= factor * aug[i][c]
                
                X = [0.0] * n
                for i in range(n - 1, -1, -1):
                    X[i] = (aug[i][n] - sum(aug[i][j] * X[j] for j in range(i + 1, n))) / aug[i][i]
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[ВЕКТОР РЕШЕНИЯ СЛАУ X]:{Colors.RESET}")
                for idx, val in enumerate(X): print(f"  • X{idx+1} = {Colors.BRIGHT_CYAN}{val:.6g}{Colors.RESET}")
                self.app.history.add("СЛАУ", f"Решена система {n}x{n}", "Успешно")

            elif choice == 4:
                r = self.app.ui.get_input("Количество строк матриц: ", int, lambda x: x > 0)
                c = self.app.ui.get_input("Количество столбцов матриц: ", int, lambda x: x > 0)
                mode = self.app.ui.get_input("Операция: 1 - Сложение, 2 - Вычитание: ", int, lambda x: x in (1, 2))
                
                A, B = self._read_matrix(r, c, "A"), self._read_matrix(r, c, "B")
                sign = 1 if mode == 1 else -1
                res = [[A[i][j] + sign * B[i][j] for j in range(c)] for i in range(r)]
                
                self.app.ui.print_smart(f"\n{Colors.BOLD}{Colors.GREEN}[РЕЗУЛЬТАТ АРИФМЕТИКИ]:{Colors.RESET}")
                for row in res: print("   " + " ".join(f"{x:<8.4g}" for x in row))
                self.app.history.add("Матрицы", "Арифметика матриц", "Успешно")

        except Exception as e:
            self.app.ui.print_error(f"Критический сбой матричного процессора: {e}")