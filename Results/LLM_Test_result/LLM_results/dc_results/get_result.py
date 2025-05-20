import os
import sys

def check_area(report_dir):
    area_file = os.path.join(report_dir, "area.rpt")
    if not os.path.exists(area_file):
        return None, None
    
    num_cells = "N/A"
    total_area = "N/A"
    
    with open(area_file, 'r') as f:
        for line in f:
            if "Number of cells:" in line:
                num_cells = line.split(":")[1].strip()
            elif "Total cell area:" in line:
                total_area = line.split(":")[1].strip().split()[0]
    
    return num_cells, total_area

def check_power(report_dir):
    power_file = os.path.join(report_dir, "power.rpt")
    if not os.path.exists(power_file):
        return None
    
    power_value = "N/A"
    
    with open(power_file, 'r') as f:
        for line in f:
            if "Total Dynamic Power" in line and "=" in line:
                parts = line.split("=")
                if len(parts) > 1:
                    power_value = parts[1].split("(100%)")[0].strip()
    
    return power_value

def check_timing(report_dir):
    qor_file = os.path.join(report_dir, "qor.rpt")
    if not os.path.exists(qor_file):
        return None, None
    
    wns = "N/A"
    tns = "N/A"
    
    with open(qor_file, 'r') as f:
        for line in f:
            if "Design  WNS:" in line:
                parts = line.split()
                try:
                    wns_index = parts.index("WNS:") + 1
                    tns_index = parts.index("TNS:") + 1
                    wns = parts[wns_index]
                    tns = parts[tns_index]
                except (ValueError, IndexError):
                    pass
    
    return wns, tns

def process_folder(folder):
    results_dir = os.path.join(folder, "results")
    report_dir = os.path.join(folder, "report")
    
    if not os.path.exists(results_dir) or len(os.listdir(results_dir)) == 0:
        return "Fail", None, None, None, None, None
    
    if not os.path.exists(report_dir):
        return "Pass (No report)", None, None, None, None, None
    
    num_cells, total_area = check_area(report_dir)
    power = check_power(report_dir)
    wns, tns = check_timing(report_dir)
    
    return "Pass", num_cells, total_area, power, wns, tns


# def main():
#     # 获取要统计的文件夹列表
#     if len(sys.argv) > 1:
#         folders = sys.argv[1:]
#     else:
#         folders = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]
    
#     # 打印表头
#     print(f"{'Folder':<20} {'Status':<15} {'Num Cells':<15} {'Total Area':<15} {'Power':<15} {'WNS':<10} {'TNS':<10}")
#     print("-" * 100)
    
#     # 处理每个文件夹
#     for folder in sorted(folders):
#         status, num_cells, total_area, power, wns, tns = process_folder(folder)
        
#         # 格式化输出
#         num_cells = num_cells if num_cells is not None else "N/A"
#         total_area = total_area if total_area is not None else "N/A"
#         power = power if power is not None else "N/A"
#         wns = wns if wns is not None else "N/A"
#         tns = tns if tns is not None else "N/A"
        
#         print(f"{folder:<20} {status:<15} {str(num_cells):<15} {str(total_area):<15} {str(power):<15} {str(wns):<10} {str(tns):<10}")

def main():
    # 获取要统计的文件夹列表
    if len(sys.argv) > 1:
        folders = sys.argv[1:]
    else:
        folders = [f for f in os.listdir('.') if os.path.isdir(f) and not f.startswith('.')]
    
    # 打开文件准备写入
    with open("./dc_results_dsr.txt", "w") as f:
        # 写入表头
        f.write(f"{'Folder':<25} {'Status':<15} {'Num Cells':<15} {'Total Area':<15} {'Power':<15} {'WNS':<10} {'TNS':<10}\n")
        f.write("-" * 100 + "\n")
        
        # 处理每个文件夹
        for folder in sorted(folders):

            if folder.endswith(("_dsr")):#, "_ds")):
                    # continue

                status, num_cells, total_area, power, wns, tns = process_folder(folder)
                
                # 格式化输出
                num_cells = num_cells if num_cells is not None else "N/A"
                total_area = total_area if total_area is not None else "N/A"
                power = power if power is not None else "N/A"
                wns = wns if wns is not None else "N/A"
                tns = tns if tns is not None else "N/A"
                
                # 写入文件
                line = f"{folder:<25} {status:<15} {str(num_cells):<15} {str(total_area):<15} {str(power):<15} {str(wns):<10} {str(tns):<10}\n"
                f.write(line)
                print(line, end='')  # 终端也打印结果（可选）

    
    print("结果已保存到 DC_results.txt")

if __name__ == "__main__":
    main()