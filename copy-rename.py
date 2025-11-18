import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FileRenamer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("批量文件复制重命名工具")
        self.root.geometry("700x500")  # 增加窗口大小
        
        self.source_file = ""
        self.name_list_file = ""
        self.output_dir = ""
        
        self.setup_ui()
    
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="批量文件复制重命名工具", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # 源文件选择框架
        source_frame = ttk.LabelFrame(main_frame, text="步骤1: 选择源文件", padding="10")
        source_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(source_frame, text="选择源文件", command=self.select_source_file, width=15).pack(side=tk.LEFT, padx=5)
        self.source_label = ttk.Label(source_frame, text="未选择文件", foreground="gray")
        self.source_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # 文件名列表选择框架
        name_list_frame = ttk.LabelFrame(main_frame, text="步骤2: 选择文件名列表文件 (txt)", padding="10")
        name_list_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(name_list_frame, text="选择列表文件", command=self.select_name_list_file, width=15).pack(side=tk.LEFT, padx=5)
        self.name_list_label = ttk.Label(name_list_frame, text="未选择文件", foreground="gray")
        self.name_list_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # 输出目录选择框架
        output_frame = ttk.LabelFrame(main_frame, text="步骤3: 选择输出目录", padding="10")
        output_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(output_frame, text="选择输出目录", command=self.select_output_dir, width=15).pack(side=tk.LEFT, padx=5)
        self.output_label = ttk.Label(output_frame, text="未选择目录", foreground="gray")
        self.output_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # 进度条框架
        progress_frame = ttk.LabelFrame(main_frame, text="进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # 开始按钮 - 现在放在更明显的位置
        self.start_button = ttk.Button(main_frame, text="开始处理", command=self.start_processing, style="Accent.TButton")
        self.start_button.pack(pady=20)
        
        # 日志框架
        log_frame = ttk.LabelFrame(main_frame, text="操作日志", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 日志文本框和滚动条
        log_container = ttk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_container, height=10, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(log_container, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # 底部按钮框架
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(bottom_frame, text="清空日志", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(bottom_frame, text="退出", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def select_source_file(self):
        file_path = filedialog.askopenfilename(
            title="选择源文件",
            filetypes=[("所有文件", "*.*")]
        )
        if file_path:
            self.source_file = file_path
            self.source_label.config(text=os.path.basename(file_path), foreground="black")
            self.log(f"✓ 选择源文件: {file_path}")
            self.check_ready_status()
    
    def select_name_list_file(self):
        file_path = filedialog.askopenfilename(
            title="选择文件名列表文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if file_path:
            self.name_list_file = file_path
            self.name_list_label.config(text=os.path.basename(file_path), foreground="black")
            self.log(f"✓ 选择文件名列表: {file_path}")
            self.check_ready_status()
    
    def select_output_dir(self):
        dir_path = filedialog.askdirectory(title="选择输出目录")
        if dir_path:
            self.output_dir = dir_path
            self.output_label.config(text=dir_path, foreground="black")
            self.log(f"✓ 选择输出目录: {dir_path}")
            self.check_ready_status()
    
    def check_ready_status(self):
        """检查是否所有条件都满足，启用开始按钮"""
        if self.source_file and self.name_list_file and self.output_dir:
            self.start_button.config(state=tk.NORMAL)
            self.log("✓ 所有条件已满足，可以开始处理")
        else:
            self.start_button.config(state=tk.DISABLED)
    
    def log(self, message):
        """添加日志信息"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def clear_log(self):
        """清空日志"""
        self.log_text.delete(1.0, tk.END)
    
    def read_name_list(self):
        """读取文件名列表"""
        try:
            with open(self.name_list_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 处理不同的换行符
            names = [name.strip() for name in content.replace('\r\n', '\n').split('\n') if name.strip()]
            
            self.log(f"📄 读取到 {len(names)} 个文件名")
            return names
        
        except Exception as e:
            self.log(f"❌ 错误: 读取文件名列表失败 - {e}")
            return []
    
    def get_file_extension(self, file_path):
        """获取文件扩展名"""
        return os.path.splitext(file_path)[1]
    
    def start_processing(self):
        """开始处理文件"""
        # 禁用开始按钮防止重复点击
        self.start_button.config(state=tk.DISABLED)
        
        # 读取文件名列表
        new_names = self.read_name_list()
        if not new_names:
            messagebox.showerror("错误", "文件名列表为空或读取失败")
            self.start_button.config(state=tk.NORMAL)
            return
        
        # 获取源文件扩展名
        file_extension = self.get_file_extension(self.source_file)
        
        # 开始处理
        self.log("🚀 开始批量复制重命名...")
        success_count = 0
        error_count = 0
        
        # 设置进度条
        self.progress['maximum'] = len(new_names)
        self.progress['value'] = 0
        
        for i, new_name in enumerate(new_names, 1):
            try:
                # 构建新文件名（保留原扩展名）
                new_filename = new_name + file_extension
                new_file_path = os.path.join(self.output_dir, new_filename)
                
                # 复制文件
                shutil.copy2(self.source_file, new_file_path)
                
                self.log(f"✅ [{i:3d}/{len(new_names)}] 成功: {new_filename}")
                success_count += 1
                
            except Exception as e:
                self.log(f"❌ [{i:3d}/{len(new_names)}] 失败: {new_name} - {e}")
                error_count += 1
            
            # 更新进度条
            self.progress['value'] = i
            self.root.update()
        
        # 显示结果
        self.log(f"\n🎉 处理完成!")
        self.log(f"✅ 成功: {success_count} 个文件")
        self.log(f"❌ 失败: {error_count} 个文件")
        
        messagebox.showinfo("完成", f"处理完成!\n成功: {success_count} 个文件\n失败: {error_count} 个文件")
        
        # 重新启用开始按钮
        self.start_button.config(state=tk.NORMAL)
    
    def run(self):
        """运行程序"""
        # 初始禁用开始按钮
        self.start_button.config(state=tk.DISABLED)
        self.root.mainloop()

if __name__ == "__main__":
    app = FileRenamer()
    app.run()