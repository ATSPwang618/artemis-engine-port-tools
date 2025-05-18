def generate_ast_file(num_blocks_list, output_filename_template="chapter-{index}.ast"):
    # 生成文件的开头部分
    ast_header = '''astver = 2.0
astname = "ast"
ast = {
'''

    # 生成文件的结尾部分
    ast_footer = '''
    label = {
        z00 = { block="block_00000", label=2 },
        z01 = { block="block_00000", label=46 },
        top = { block="block_00000", label=1 },
    },
}
'''

    # 生成每个文件的内容
    for idx, num_blocks in enumerate(num_blocks_list):
        print(f"开始生成第 {idx + 1} 个文件，包含 {num_blocks} 个块")  # 调试打印，显示当前生成的文件和块数
        blocks = []
        for i in range(num_blocks):
            block_id = f"block_{i:05d}"

            print(f"  生成块 {block_id}...")  # 调试打印，显示当前块的 ID

            # 判断是否为第一个block
            if i == 0:
                # 第一个block只有linknext，没有linkback
                block_content = f'''
    {block_id} = {{
        {{"savetitle", text="XXXXXXXX"}},
        {{"user", mode="autosave", no=1}},
        {{"eval", exp="g.chap01=1"}},
        {{"cgdel", id=-1}},
        {{"fg", mode=-2}},
        {{"bg", file="black", path=":bg/"}},
        {{"savetitle", text="XXXXXXXX"}},
        {{"ex", time=1000, func="wait"}},
        {{"se", stop=1, id=0, time=2000}},
        {{"cgdel", id=-1}},
        {{"fg", mode=-2}},
        {{"msgoff"}},
        {{"cgdel", id=-1}},
        {{"fg", mode=-2}},
        {{"bg", id=1, lv=5, file="black", alpha=192, path=":bg/", sync=0}},
        {{"extrans", time=0}},
        {{"ex", time=500, func="wait"}},
        {{"text"}},
        text = {{
            ja = {{{{"XXXXXXXXXXXX-文字{i + 1}",}},}},
        }},
        linknext = "block_{(i + 1):05d}",
        line = {96 + i + i},
    }},
'''
            elif i == num_blocks - 1:
                # 最后一个block，带有特殊的内容
                block_content = f'''
    {block_id} = {{
        {{"msgoff"}},
        {{"ex", time=1000, func="wait"}},
        {{"exreturn"}},
        {{"text"}},
        linkback = "block_{(i - 1):05d}",
        line = {96 + i + i},
    }},
'''     
            else:
                # 每6个块插入pagebreak = true
                pagebreak_line = ''
                if (i + 1) % 6 == 0:
                    pagebreak_line = 'pagebreak = true,'

                # 其他block有linkback和linknext
                block_content = f'''
     {block_id} = {{
        {{"text"}},
        text = {{
            {pagebreak_line}
            --vo = {{{{"vo", ch="xxx", file="xxx"}},}},
            ja = {{{{"XXXXXXXXXXXX-文字{i + 1}",}},}},
        }},
        linkback = "block_{(i - 1):05d}",
        linknext = "block_{(i + 1):05d}",
        line = {96 + i + i},
    }},
'''
            blocks.append(block_content)

        # 生成当前文件的内容
        ast_script = ast_header + ''.join(blocks) + ast_footer

        # 生成文件名
        output_filename = output_filename_template.format(index=idx + 1)

        print(f"  写入文件: {output_filename}")  # 调试打印，显示写入的文件名

        # 将内容写入文件
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(ast_script)

        print(f"AST file '{output_filename}' has been generated with {num_blocks} blocks.")  # 生成文件的总结打印


# 从命令行获取输入的每个文件的块的数量
def get_num_blocks_list():
    num_blocks_list = []
    while len(num_blocks_list) < 5:
        try:
            num_blocks = input(f"请输入第{len(num_blocks_list) + 1}个文件的块数量（剩余{5 - len(num_blocks_list)}个文件）: ")
            num_blocks = int(num_blocks)
            if num_blocks > 0:
                num_blocks_list.append(num_blocks)
            else:
                print("请输入一个大于 0 的数字")
        except ValueError:
            print("无效输入，请输入一个有效的数字")
    return num_blocks_list


# 获取文件块数量列表
num_blocks_list = get_num_blocks_list()

# 生成文件
generate_ast_file(num_blocks_list)
