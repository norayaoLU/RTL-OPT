import os
import re

def process_designs(input_list):
    base_path = "XXX"

    design_info = []

    for element in input_list:
        folder_path = os.path.join(base_path, element)
        if not os.path.isdir(folder_path):
            print(f"Directory {element} not found, skipping")
            continue

        files = [f for f in os.listdir(folder_path) if f.startswith(element) and os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            print(f"No files starting with {element} found, skipping")
            continue

        print(f"Files in {element}: {files}")
        
        # 查找模块名和文件格式
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
        design_info.append((element, element, file_format))
    # print(design_info)
    # exit()

    update_design_list(input_list)
    # exit()

    update_tcl_file(design_info)
    # exit()

    os.system("source XXX/run_dc.sh")

def update_design_list(input_list):
    try:
        with open("design_list", "r+") as f:
            content = f.read()
            new_content = re.sub(
                r"__START__\n.*?__END__",
                f"__START__\n" + "\n".join(input_list) + "\n__END__",
                content,
                flags=re.DOTALL
            )
            f.seek(0)
            f.write(new_content)
            f.truncate()
    except Exception as e:
        print(f"Error updating design_list: {e}")

def update_tcl_file(design_info):
    if not design_info:
        return


    existing_content = ""
    try:
        with open("set_rtl_path.tcl", "r") as f:
            existing_content = f.read()
    except FileNotFoundError:
        existing_content = ""
    except Exception as e:
        print(f"Error reading TCL file: {e}")
        return

    try:
        with open("set_rtl_path.tcl", "r+") as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1].rstrip()
                if not last_line.endswith('\\'):
                    lines[-1] = last_line + ' \\\n'
                else:
                    lines[-1] = last_line.rstrip('\\') + ' \\\n'
                f.seek(0)
                f.writelines(lines)
                f.truncate()
    except FileNotFoundError:
        pass  
    except Exception as e:
        print(f"Error preparing TCL file: {e}")
        return


    new_content = []
    for i, (element, module, fmt) in enumerate(design_info):
        pattern = re.compile(r'string equal \$design "{}"'.format(re.escape(element)))
        if pattern.search(existing_content):
            print(f"Design {element} already exists in TCL file, skipping")
            continue

        line = f'elseif {{ [string equal $design "{element}"] }} {{ set rtl_path "${{bench_root}}/{element}"; set design_name "{module}"; set clock_name "clk"; set file_format "{fmt}" }}'
        
     
        if i != len(design_info) - 1:
            line += ' \\'
        new_content.append(line)


    try:
        with open("set_rtl_path.tcl", "a") as f:
            f.write('\n'.join(new_content) + '\n')
            
      
        with open("set_rtl_path.tcl", "r+") as f:
            content = f.read().rstrip()
            content = content.rstrip('\\')  
            f.seek(0)
            f.write(content + '\n')  
            f.truncate()
    except Exception as e:
        print(f"Error updating TCL file: {e}")

def check_results(input_designs):
    passed = []
    failed = []
    
    for design in input_designs:
        results_dir = os.path.join(design, "results")
        report_dir = os.path.join(design, "report")
        area_rpt_path = os.path.join(report_dir, "area.rpt")
        
       
        if not os.path.isdir(results_dir):
            failed.append(design)
            print(f"[FAIL] {design}: results directory not found")
            continue
            
      
        result_files = [f for f in os.listdir(results_dir) 
                        if os.path.isfile(os.path.join(results_dir, f))]
        
       
        error_in_report = False
        if os.path.isfile(area_rpt_path):
            with open(area_rpt_path, 'r') as report_file:
                first_line = report_file.readline()
                # print(first_line)
                if "Error" in first_line:
                    error_in_report = True
        
        
        if (not result_files) or error_in_report:
            failed.append(design)
            
        else:
            passed.append(design)
            # print(f"[PASS] {design}: found {len(result_files)} result files")
    
    # 打印统计信息
    print("\n===== Verification Summary =====")
    print(f"Total designs: {len(input_designs)}")
    print(f"Passed: {len(passed)} ({', '.join(passed) if passed else 'None'})")
    print(f"Failed: {len(failed)} ({', '.join(failed) if failed else 'None'})")
    
    return passed, failed

if __name__ == "__main__":
    for suffix in ['','_ds', '_gpt', '_mini','_dsr','_ref']:
        input_designs = [
            "adder",
            "adder_carry",
            "adder_select",
            "alu_64bit",
            "alu_8bit",
            "calculation",
            "comparator_2bit",
            "comparator_4bit",
            "comparator_8bit",
            "comparator_16bit",
            "comparator",
            "decoder_6bit",
            "decoder_8bit",
            "divider_4bit",
            "divider_8bit",
            "fsm",
            "fsm_encode",
            "gray",
            "mac",
            "mul",
            "mul_subexpression",
            "mul_const",
            "mux_4to1_16bit",
            "mux_4to1_64bit",
            "mux_dead",
            "mux_encode",
            "saturating_add",
            "selector",
            "sub_16bit",
            "sub_32bit",
            "sub_4bit",
            "sub_8bit",
            "divider_16bit",
            "divider_32bit",
            "add_sub",
            "addr_calcu",
            "mult_if",
            "mux_large",
            "register",
            "ticket_machine"
            ]
        

        input_designs = [design + suffix for design in input_designs]

        process_designs(input_designs)
        check_results(input_designs)