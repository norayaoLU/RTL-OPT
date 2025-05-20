import os
import re
def find_rpt_modules():
    module_list = []
    
    for filename in os.listdir('.'):
        if filename.endswith('.rpt'):
            module_name = filename[:-4]
            
            try:
                with open(filename, 'r') as f:
                    content = f.read()
                    if f"=== {module_name} ===" in content:
                        module_list.append(module_name)
            except Exception as e:
                print(f"Warning: reading {filename} : {str(e)}")
                continue
                
    return module_list

def yosys_gen(top_module_name=None):
    try:   
        with open("run_yosys.ys", 'w') as f:
            ys_template = """read -sv /XXX/MODULE_NAME/MODULE_NAME.v
hierarchy -top MODULE_NAME

proc; fsm; opt; memory; opt

techmap; opt

dfflibmap -liberty nangate45.lib
abc -liberty nangate45.lib    

tee -o MODULE_NAME.rpt stat -top MODULE_NAME -liberty nangate45.lib

clean"""
            ys_content = ys_template.replace("MODULE_NAME", top_module_name)
            f.write(ys_content)
        
        os.system("yosys run_yosys.ys")  

    except Exception as e:
        print(f"Exception occurred while processing {top_module_name}: {str(e)}")

        
def check_results(modules, output_file="/XXX/YS_results.txt"):
    results = {}
    

    with open(output_file, 'w') as f:
      
        f.write("\n{:<25} {:<15} {:<15} {:<15}\n".format(
            "Module", "Wires", "Cells", "Area"))
        f.write("-" * 65 + "\n")
        
        for module in sorted(modules):
            rpt_file = f"{module}.rpt"
            if not os.path.exists(rpt_file):
                warning_msg = f"Warning: Report file {rpt_file} not found!\n"
                f.write(warning_msg)
                print(warning_msg, end='')  
                continue
                
            with open(rpt_file, 'r') as rpt:
                content = rpt.read()
                
                wires_match = re.search(r'Number of wires:\s+(\d+)', content)
                cells_match = re.search(r'Number of cells:\s+(\d+)', content)
                area_match = re.search(r'Chip area for module[^:]+:\s*([\d]+\.[\d]+(?:[eE][-+]?[\d]+)?)', content)
                
                results[module] = {
                    'wires': int(wires_match.group(1)) if wires_match else 0,
                    'cells': int(cells_match.group(1)) if cells_match else 0,
                    'area': float(area_match.group(1)) if area_match else 0.0
                }
                
              
                line = "{:<25} {:<15} {:<15} {:<15}\n".format(
                    module,
                    results[module]['wires'],
                    results[module]['cells'],
                    results[module]['area'])
                f.write(line)
                print(line, end='')  
    
    print(f"\nResults saved to {output_file}")  
    return results

if __name__ == "__main__":
    suffix = "" #_ref, _ds, _gpt
    input_designs = [
    "adder"
    ] 
   
    for item in input_designs:
        yosys_gen(f'{item}{suffix}')
    results = check_results([f'{item}{suffix}' for item in input_designs])


    all_rpt_files = find_rpt_modules()
    results = check_results(all_rpt_files,"XXX/YS_results.txt")
