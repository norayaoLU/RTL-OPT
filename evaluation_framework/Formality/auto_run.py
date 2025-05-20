import os
import re

def process_designs(input_design):
    base_path = "XXX"
    design_info = []

    for element in [input_design, f'{input_design}_ref']:
        folder_path = os.path.join(base_path, element)
        if not os.path.isdir(folder_path):
            print(f"Directory {element} not found, skipping")
            continue

        files = [f for f in os.listdir(folder_path) if f.startswith(element) and os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            print(f"No files starting with {element} found, skipping")
            continue

        print(f"Files in {element}: {files}")
        
        module_name = None
        file_format = "verilog"
        for file in files:
            if file.startswith(element):
                try:
                    with open(os.path.join(folder_path, file), "r") as f:
                        content = f.read()
                        match = re.search(r"module\s+(\w+)", content)
                        if match:
                            module_name = match.group(1)
                            if file.endswith(".sv"):
                                file_format = "sverilog"
                            break
                except Exception as e:
                    print(f"Error reading {file}: {e}")
        
        if not module_name:
            print(f"No module found in {element}, skipping")
            continue

        # design_info.append((element, module_name, file_format))
        design_info.append((element, file_format))

    update_sh_file(design_info)

    os.system("source /XXX/run_fm.sh")


def update_sh_file(design_info):

    if not design_info or len(design_info) < 2 or len(design_info[0]) < 2 or len(design_info[1]) < 2:
        raise ValueError("design_info Error")
    
    print(design_info)
    design_name = design_info[0][0]
    file_format = design_info[0][1]
    file_format_ref = design_info[1][1]
    
    with open('run_fm.sh', 'r') as f:
        content = f.read()
    

    content = re.sub(r'design_name=".*?"', f'design_name="{design_name}"', content)
    content = re.sub(r'design_name_i=".*?"', f'design_name_i="{design_name}{suffix}"', content)

    content = re.sub(r'file_format=".*?"', f'file_format="{file_format}"', content)

    content = re.sub(r'file_format_ref=".*?"', f'file_format_ref="{file_format_ref}"', content)
    
    with open('run_fm.sh', 'w') as f:
        f.write(content)



def check_results(input_designs):
    passed = []
    failed = []
    error_message = "Error: Diagnosis and analysis can only be performed after an unsuccessful verification (FM-006)"
    
    for design in input_designs:
        results_dir = f"{design}_rpt"
        report_file = os.path.join(results_dir, "points.rpt")
        
        if not os.path.exists(results_dir):
            failed.append(design)
            print(f"[FAIL] {design}: results directory not found")
            continue
            
        if not os.path.isfile(report_file):
            failed.append(design)
            print(f"[FAIL] {design}: report file not found")
            continue
        
        try:
            with open(report_file, 'r') as f:
                first_line = f.readline().strip()
                if error_message in first_line:
                    passed.append(design)
                    # print(f"[PASS] {design}: found expected error message")
                else:
                    failed.append(design)
                    # print(f"[FAIL] {design}: unexpected result in report")
        except Exception as e:
            failed.append(design)
            print(f"[FAIL] {design}: error reading report file - {str(e)}")
    

    print("\n===== FM Verification Summary =====")
    print(f"Total designs: {len(input_designs)}")
    print(f"Passed: {len(passed)} ({', '.join(passed) if passed else 'None'})")
    print(f"Failed: {len(failed)} ({', '.join(failed) if failed else 'None'})")
    
    return passed, failed
    

if __name__ == "__main__":
    suffix = "_gpt" #_dsr,_mini,_ds,_gpt
    input_designs = ["adder"] 
    for item in input_designs:
        process_designs(item)

    check_results(input_designs)