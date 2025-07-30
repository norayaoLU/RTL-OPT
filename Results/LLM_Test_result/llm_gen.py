from openai import OpenAI
import os

# Initialize the AzureOpenAI client

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="xxxx",
  # provisioning key : xxxxx
)
    
def read_file(file_path):
    """Read content from a file"""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File {file_path} not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_to_file(file_path, content):
    """Write content to a file"""
    try:
        with open(file_path, 'a') as file:  # Append mode
            file.write(content + "\n")
        return True
    except Exception as e:
        print(f"Error writing to file: {str(e)}")
        return False

def process_optimization_request(input_file, file_type):
    """Process the optimization request and write results to file"""
    # Read input file
    input_content = read_file(input_file)
    if input_content.startswith("Error"):
        return input_content
    
    # Initialize conversation
    messages = [
        {"role": "system", "content": "You are an expert programming assistant."},
        {"role": "user", "content": f"Please try to optimize this Verilog code to achieve better PPA (Power, Performance, Area) after synthesis, while keeping the module's interface names unchanged. Add '_dsr' to the end of the original module name, and ensure the optimized code preserves identical functionality without any syntax errors.\n Please analyze and optimize this {file_type} code:\n{input_content}\n\nPlease provide the optimized Verilog code, writing the code between ###Code### and ###End code###. do not include any Markdown tags (```verilog, ```), explanations, or extra text."}
    ]
    headers = {
            "HTTP-Referer": "<YOUR_SITE_URL>", 
            "X-Title": "<YOUR_SITE_NAME>", 
        }
  
    # Get optimization from Azure OpenAI
    response = client.chat.completions.create(
        # model="google/gemini-2.5-flash-preview", #2025.4.17
        # model="google/gemini-2.5-flash",
        # model="openai/gpt-4o-mini",              #2024.7.18
        # model="deepseek/deepseek-chat-v3-0324",  #2025.3.24
        model="deepseek/deepseek-r1",            #2025.1.20
        # model="meta-llama/llama-3-70b-instruct", #2024.4.18
        # model="qwen/qwen-2.5-72b-instruct",      #2024.9.19
      
        messages=messages,
        extra_headers=headers,
        extra_body={}
    )

    assistant_response = response.choices[0].message.content
    
    return assistant_response

def main():
    base_path = "xxxxx"
    input_designs = [
        "adder"
        #
    ] 

    for design in input_designs:
        if design == "mux_encode":
            suffix = 'sv'
            file_type = 'system verilog'
        else:
            suffix = 'v'
            file_type = 'verilog'
        input_file = f"{base_path}/{design}/{design}.{suffix}"
        print(f"Processing: {input_file}")

        output_file = f"DSR/{design}.txt"  
    
        if os.path.exists(output_file):
            open(output_file, 'w').close()
        
        # Process the optimization request
        result = process_optimization_request(input_file, file_type)
        print("Optimization complete. Results written to", output_file)
        write_to_file(output_file, result)


if __name__ == "__main__":
    main()
