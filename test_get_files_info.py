from functions.get_files_info import get_files_info


def format_result(label: str, result: str) -> str:
    if result.startswith("Error:"):
        return f"Result for {label}:\n    {result}"

    lines = [f"Result for {label}:"]
    for line in result.splitlines():
        lines.append(f"  - {line}")
    return "\n".join(lines)


print(format_result("current directory", get_files_info("calculator", ".")))
print(format_result("'pkg' directory", get_files_info("calculator", "pkg")))
print(format_result("'/bin' directory", get_files_info("calculator", "/bin")))
print(format_result("'../' directory", get_files_info("calculator", "../")))