import ast
import json
from typing import List

TEMPLATES_PATH = "app/templates/explanation_templates.json"

with open(TEMPLATES_PATH, 'r') as f:
    TEMPLATES = json.load(f)


class Issue:
    def __init__(self, title, category, severity, lineno, snippet, why, fix, principle):
        self.title = title
        self.category = category
        self.severity = severity
        self.lineno = lineno
        self.snippet = snippet
        self.why = why
        self.fix = fix
        self.principle = principle

    def to_dict(self):
        return {
            'title': self.title,
            'category': self.category,
            'severity': self.severity,
            'lineno': self.lineno,
            'snippet': self.snippet,
            'why': self.why,
            'fix': self.fix,
            'principle': self.principle,
        }


class OpenWithoutWithVisitor(ast.NodeVisitor):
    """Detect open() calls not inside a 'with' statement."""
    def __init__(self, source_code: str):
        self.issues: List[Issue] = []
        self._source = source_code

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id == 'open':
            if not self._is_inside_with(node):
                lineno = getattr(node, 'lineno', None)
                snippet = ast.get_source_segment(self._source, node) or 'open(...)'
                t = TEMPLATES.get('open_without_with', {})
                issue = Issue(
                    t.get('title', 'Open without with'),
                    t.get('category', 'Resource management'),
                    t.get('severity', 'Medium'),
                    lineno,
                    snippet,
                    t.get('why', ''),
                    t.get('fix', ''),
                    t.get('principle', '')
                )
                self.issues.append(issue)
        self.generic_visit(node)

    def _is_inside_with(self, node):
        cur = node
        while hasattr(cur, 'parent'):
            cur = cur.parent
            if isinstance(cur, ast.With):
                return True
        return False


def attach_parents(node: ast.AST):
    """Recursively attach parent references to AST nodes."""
    for child in ast.iter_child_nodes(node):
        child.parent = node
        attach_parents(child)


def analyze_code(source_code: str) -> List[Issue]:
    """Analyze syntax errors and patterns."""
    issues = []

    # 1️⃣ Syntax errors
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        issue = Issue(
            title="Syntax Error",
            category="Syntax",
            severity="High",
            lineno=e.lineno,
            snippet=e.text.strip() if e.text else "",
            why=e.msg,
            fix="Correct the syntax error",
            principle="Code must be valid Python syntax"
        )
        issues.append(issue)
        return issues  # Can't parse further

    # 2️⃣ Pattern checks (e.g., open without with)
    attach_parents(tree)
    visitor = OpenWithoutWithVisitor(source_code)
    visitor.visit(tree)
    issues.extend(visitor.issues)

    return issues


def analyze_runtime_errors(source_code: str) -> List[Issue]:
    """Detect runtime errors and provide exact line info."""
    issues = []
    try:
        exec(source_code, {})
    except Exception as e:
        import traceback

        tb = traceback.extract_tb(e.__traceback__)
        # Filter to lines from the user code
        user_tb = next((t for t in tb if t.filename == "<string>"), tb[-1] if tb else None)

        if user_tb:
            lineno = user_tb.lineno
            snippet = user_tb.line or ""
        else:
            lineno = None
            snippet = ""

        issue = Issue(
            title=type(e).__name__,
            category="Runtime Error",
            severity="High",
            lineno=lineno,
            snippet=snippet.strip(),
            why=str(e),
            fix="Fix the runtime error",
            principle="Code should run without exceptions",
        )
        issues.append(issue)
    return issues


def analyze_python(filename: str, source_code: str):
    """
    Full analyzer entry for FastAPI: returns filename, issues, metrics, score.
    """
    # 1) Static checks (syntax & patterns)
    issues = analyze_code(source_code)

    # 2) If there are syntax issues, skip runtime exec (can't run)
    if not any(i.category == "Syntax" for i in issues):
        issues.extend(analyze_runtime_errors(source_code))

    # 3) Convert issues to dicts for frontend
    issues_dicts = [i.to_dict() for i in issues]

    # 4) Compute metrics and score
    metrics, score = compute_metrics_and_score(source_code, issues)

    return {
        "filename": filename,
        "issues": issues_dicts,
        "metrics": metrics,
        "score": score,
    }
# --- add these imports at top if not already present ---
import statistics
import re
# -------------------------------------------------------

def _count_loc_and_comments(source_code: str):
    lines = source_code.splitlines()
    total_lines = len(lines)
    blank_lines = sum(1 for l in lines if l.strip() == "")
    comment_lines = sum(1 for l in lines if l.strip().startswith("#"))
    code_lines = total_lines - blank_lines - comment_lines
    return {
        "total_lines": total_lines,
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "blank_lines": blank_lines,
    }


def _function_stats_and_lengths(source_code: str):
    """
    Returns:
      num_functions, avg_function_length_lines, function_lengths (list),
      docstring_covered_count (functions with docstring)
    """
    try:
        tree = ast.parse(source_code)
    except Exception:
        return {
            "num_functions": 0,
            "avg_function_length": 0.0,
            "function_lengths": [],
            "docstring_covered": 0,
        }

    func_lengths = []
    docstring_covered = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # function length in source lines: lineno .. end_lineno (end_lineno is py3.8+)
            start = getattr(node, "lineno", None)
            end = getattr(node, "end_lineno", None)
            if start and end:
                func_lengths.append(end - start + 1)
            else:
                # fallback: estimate by counting child nodes' linenos
                child_lines = [getattr(n, "lineno", start) for n in ast.walk(node) if getattr(n, "lineno", None)]
                if child_lines:
                    func_lengths.append(max(child_lines) - (start or min(child_lines)) + 1)
                else:
                    func_lengths.append(0)
            # docstring
            if ast.get_docstring(node):
                docstring_covered += 1

    num_functions = len(func_lengths)
    avg_len = float(statistics.mean(func_lengths)) if func_lengths else 0.0
    return {
        "num_functions": num_functions,
        "avg_function_length": avg_len,
        "function_lengths": func_lengths,
        "docstring_covered": docstring_covered,
    }


def _approximate_cyclomatic_complexity(source_code: str):
    """
    Simple heuristic: count decision points per function and global.
    Decision nodes considered: If, For, While, With, Try, BoolOp (and/or), IfExp, Compare
    Returns average complexity per function and total complexity.
    """
    try:
        tree = ast.parse(source_code)
    except Exception:
        return {"total_complexity": 0, "avg_complexity": 0.0, "function_complexities": []}

    def complexity_counter(node):
        count = 0
        # decision keywords
        if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.IfExp)):
            count += 1
        if isinstance(node, ast.BoolOp):
            # each boolean operator is an additional path (a and b and c -> 2)
            count += max(1, len(node.ops) - 0)
        if isinstance(node, ast.Compare):
            count += 0  # comparisons alone not add much; optionally add
        return count

    func_complexities = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # count decision points inside function
            sub_count = 1  # base complexity 1
            for sub in ast.walk(node):
                sub_count += complexity_counter(sub)
            func_complexities.append(sub_count)

    total_complexity = sum(func_complexities) if func_complexities else 0
    avg_complexity = float(statistics.mean(func_complexities)) if func_complexities else 0.0
    return {"total_complexity": total_complexity, "avg_complexity": avg_complexity, "function_complexities": func_complexities}


def _count_todos_and_long_lines(source_code: str):
    lines = source_code.splitlines()
    todo_count = sum(1 for l in lines if "TODO" in l or "FIXME" in l)
    long_lines = sum(1 for l in lines if len(l) > 120)
    return {"todo_count": todo_count, "long_lines": long_lines}


def compute_metrics_and_score(source_code: str, issues: List):
    """
    Returns (metrics_dict, score_dict).
    metrics contains several measured values and a brief human-friendly explanation.
    score contains {'score': int} 0-100.
    """
    # Basic counts
    loc = _count_loc_and_comments(source_code)
    funcs = _function_stats_and_lengths(source_code)
    complexity = _approximate_cyclomatic_complexity(source_code)
    extras = _count_todos_and_long_lines(source_code)

    num_issues = len(issues)

    # Docstring coverage ratio
    doc_coverage = (funcs["docstring_covered"] / funcs["num_functions"]) if funcs["num_functions"] else 1.0

    # Heuristic penalties (you can tune weights)
    # Larger LOC slightly reduces score if enormous; more issues heavier penalty.
    issue_penalty = min(50, num_issues * 6)  # each issue ~6 points, capped
    complexity_penalty = min(20, complexity["avg_complexity"] * 2.5)  # per-function average
    todo_penalty = min(10, extras["todo_count"] * 2)
    longline_penalty = min(10, extras["long_lines"] * 0.5)
    doc_penalty = 0 if doc_coverage >= 0.8 else (1 - doc_coverage) * 15  # encourage docstrings
    func_len_penalty = 0
    # penalty for average function length > 50 lines
    if funcs["avg_function_length"] > 50:
        func_len_penalty = min(15, (funcs["avg_function_length"] - 50) * 0.2)

    # LOC penalty (only if very large)
    loc_penalty = 0
    if loc["code_lines"] > 1000:
        loc_penalty = min(10, (loc["code_lines"] - 1000) / 100)

    total_penalties = (
        issue_penalty
        + complexity_penalty
        + todo_penalty
        + longline_penalty
        + doc_penalty
        + func_len_penalty
        + loc_penalty
    )

    raw_score = max(0, 100 - total_penalties)
    final_score = int(round(raw_score))

    # Compose metrics dict
    metrics = {
        "loc": loc,
        "num_issues": num_issues,
        "functions": {
            "num_functions": funcs["num_functions"],
            "avg_function_length": funcs["avg_function_length"],
            "function_lengths": funcs["function_lengths"],
            "docstring_covered": funcs["docstring_covered"],
            "docstring_coverage": doc_coverage,
        },
        "complexity": complexity,
        "todos_and_style": extras,
        "penalties": {
            "issue_penalty": issue_penalty,
            "complexity_penalty": complexity_penalty,
            "todo_penalty": todo_penalty,
            "longline_penalty": longline_penalty,
            "doc_penalty": doc_penalty,
            "func_len_penalty": func_len_penalty,
            "loc_penalty": loc_penalty,
            "total_penalties": total_penalties,
        },
        "explanation": "Score starts at 100; penalties applied for issues, complexity, missing docstrings, TODOs, long functions/lines.",
    }

    score = {"score": final_score, "raw_score": raw_score}

    return metrics, score
