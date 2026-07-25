import sys
from .platform_utils import get_tool_dir
from .config import get_conf_path
from .menu import run_menu

if __name__ == "__main__":
    tool_dir = get_tool_dir()
    conf_path = get_conf_path()
    if not tool_dir.exists() or not conf_path.exists():
        print("错误：工具未安装，请先运行 install.py")
        sys.exit(1)
    run_menu()
