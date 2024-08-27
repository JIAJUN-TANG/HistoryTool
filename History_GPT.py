import streamlit.web.cli as stcli
import os, sys
 
 
def resolve_path():
    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    os.chdir(current_dir)
    return current_dir
 
 
if __name__ == "__main__":
    file_path = os.path.join(resolve_path(), "Homepage.py")
    sys.argv = [
        "streamlit",
        "run",
        str(file_path),
        "--global.developmentMode=false",
    ]
    sys.exit(stcli.main())