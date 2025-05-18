import sys
import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def parse_input_file(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            print(f"[DEBUG] 已读取输入文件: {input_file}")
            return f.readlines()
    except Exception as e:
        print(f"[ERROR] 文件读取失败: {str(e)}")
        return None

def is_tlid_line(line):
    return "@@@TLID_" in line

def extract_tlid(line):
    match = re.search(r'@@@TLID_(\d+)_', line)
    return match.group(1) if match else None

def extract_vo_info(line):
    match = re.search(r'KOE\(([^,]+),\d+\)', line)
    return match.group(1) if match else None

def extract_character_name(line):
    match = re.search(r'【(.+?)】', line)
    return match.group(1) if match else None

def extract_dialogue(line):
    match = re.search(r'@@@TLID_\d+_(.+?)R', line)
    if match:
        text = match.group(1).strip()
        text = text.replace('　', '')  # 去除全角空格
        return text
    return None

def extract_bg_file(line):
    match = re.search(r'@CGS\(([^)]+)\)', line)
    return match.group(1) if match else None

def convert_lines_to_ast(lines, start_block, start_line, line_step, output_file):
    blocks = []
    pending_vo = None
    pending_ch = None
    current_bg = None
    prev_bg = None
    block_id = start_block
    line_number = start_line

    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith('@CGS('):
                current_bg = extract_bg_file(line)
                print(f"[DEBUG] 检测到背景切换: {current_bg}")
                continue
                
            if 'KOE(' in line:
                pending_vo = extract_vo_info(line)
                pending_ch = extract_character_name(line)
                print(f"[DEBUG] 提取语音信息 - 角色: {pending_ch}, 文件: {pending_vo}")
                continue

            if is_tlid_line(line):
                text = extract_dialogue(line)
                if not text:
                    continue

                block_lines = []
                
                if current_bg and current_bg != prev_bg:
                    bg_name = current_bg.replace('SI', 'CGM_SI') + '_010a_0000'
                    block_lines.append(f'    {{"bg",id=4,lv=5,file="{bg_name}",time=300, path=":fg/",sync=0,x=420,y=0}},')
                    prev_bg = current_bg

                block_lines.append('    {"text"},')
                block_lines.append('    text = {')
                
                if pending_vo and pending_ch:
                    block_lines.append(f'        vo = {{ {{"vo", ch="{pending_ch}", file="{pending_vo}"}} }},')
                    print(f"[DEBUG] 为 block_{block_id:05d} 添加语音: {pending_ch}/{pending_vo}")
                    pending_vo = None
                    pending_ch = None
                
                block_lines.append(f'        ja = {{"{text}"}},')
                
                if current_bg and current_bg != prev_bg and block_id > start_block:
                    block_lines.append('        pagebreak = true,')
                
                block_lines.append('    },')
                
                block_text = f'block_{block_id:05d} = {{\n' + "\n".join(block_lines) + \
                            f'\n    linkback = "block_{block_id-1:05d}",\n    linknext = "block_{block_id+1:05d}",\n    line = {line_number},\n}},\n'

                blocks.append(block_text)
                block_id += 1
                line_number += line_step

        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("{\n")
            for block in blocks:
                f.write(block + "\n")
            f.write("}\n")
        print(f"[SUCCESS] 文件已生成: {output_file}")
        return True

    except Exception as e:
        print(f"[ERROR] 转换过程中发生错误: {str(e)}")
        return False

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AST 文件生成工具")
        self.geometry("600x400")
        
        # 参数预设值
        self.start_block = 504
        self.start_line = 1104
        self.line_step = 2
        
        self.create_widgets()
    
    def create_widgets(self):
        # 输入文件选择
        tk.Label(self, text="输入文件:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.input_entry = tk.Entry(self, width=50)
        self.input_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="浏览...", command=self.select_input).grid(row=0, column=2, padx=10)

        # 输出目录选择
        tk.Label(self, text="输出目录:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.output_entry = tk.Entry(self, width=50)
        self.output_entry.grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="浏览...", command=self.select_output).grid(row=1, column=2, padx=10)

        # 参数设置
        tk.Label(self, text="起始块号:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.block_entry = tk.Entry(self)
        self.block_entry.insert(0, str(self.start_block))
        self.block_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self, text="起始行号:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.line_entry = tk.Entry(self)
        self.line_entry.insert(0, str(self.start_line))
        self.line_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self, text="行号步长:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.step_entry = tk.Entry(self)
        self.step_entry.insert(0, str(self.line_step))
        self.step_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # 运行按钮
        tk.Button(self, text="开始转换", command=self.run_conversion).grid(row=5, column=1, pady=20)

        # 日志输出
        self.log_text = tk.Text(self, height=10, width=70)
        self.log_text.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    def select_input(self):
        file_path = filedialog.askopenfilename(
            title="选择输入文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

    def select_output(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, dir_path)

    def run_conversion(self):
        # 获取输入参数
        input_file = self.input_entry.get()
        output_dir = self.output_entry.get()
        
        try:
            self.start_block = int(self.block_entry.get())
            self.start_line = int(self.line_entry.get())
            self.line_step = int(self.step_entry.get())
        except ValueError:
            messagebox.showerror("错误", "参数必须为整数")
            return

        if not input_file or not output_dir:
            messagebox.showerror("错误", "请先选择输入文件和输出目录")
            return

        # 生成输出文件名
        base_name = os.path.basename(input_file).replace('.txt', '.ast')
        output_file = os.path.join(output_dir, base_name)

        # 处理文件
        lines = parse_input_file(input_file)
        if not lines:
            messagebox.showerror("错误", "文件读取失败")
            return

        # 重定向日志到文本框
        original_stdout = sys.stdout
        sys.stdout = TextRedirector(self.log_text, "stdout")
        
        success = convert_lines_to_ast(
            lines=lines,
            start_block=self.start_block,
            start_line=self.start_line,
            line_step=self.line_step,
            output_file=output_file
        )
        
        sys.stdout = original_stdout
        
        if success:
            messagebox.showinfo("输出文件ast已经完成", f"文件已生成到:\n{output_file}")
        else:
            messagebox.showerror("错误", "转换过程中发生错误，请查看日志")

class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see("end")

if __name__ == "__main__":
    app = Application()
    app.mainloop()