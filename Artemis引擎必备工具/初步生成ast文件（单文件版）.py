def generate_ast_file(num_blocks, output_filename="chapter-单文件.ast"):
    # 生成文件的开头部分
    ast_header = '''astver = 2.0
astname = "ast"
ast = {
'''

    # 生成每个block的内容
    blocks = []
    for i in range(num_blocks):
        block_id = f"block_{i:05d}"
        
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
    






    # 生成文件的结尾部分
    ast_footer = '''
    label = {
        z00 = { block="block_00000", label=2 },
		z01 = { block="block_00000", label=46 },
		top = { block="block_00000", label=1 },
    },
}
'''
    # 将所有部分合并
    ast_script = ast_header + ''.join(blocks) + ast_footer

    # 写入文件
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(ast_script)

    print(f"AST file '{output_filename}' has been generated with {num_blocks} blocks.")

# 输入块的数量
num_blocks = int(input("请输入你想生成的block的数量: "))
generate_ast_file(num_blocks)
