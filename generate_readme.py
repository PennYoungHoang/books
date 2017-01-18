# -*-encoding:utf-8 -*-
import logging
import os
import re


HeaderLine = """
```
The book list mainly contains economics, technology and psychology.
I've read them more or less.
They gave me different insights to the world, and how something works. So I'd like to share with others.
I'm not the one who sells knowledge. Knowledge is dead and everywhere.
Since the future is already here, I just wanna it to be distributed.
Hope you can find interests in the books.

```
"""

FooterLine = """

## PR

Any pull requests or issues are welcome .    
Use `python generate_readme.py` for generating readme.



"""

ignore_files = ['\..*',"generate_readme.py", "README.md"]
ignore_patterns = [re.compile(i) for i in ignore_files]
not_ignore = lambda fname: not any([p.match(fname) for p in ignore_patterns])

git_dir = os.path.dirname(os.path.abspath(__file__))
print "Git:%s, dir length:%s "%(git_dir,len(git_dir))
PREFIX = len(git_dir)


class Tree:

    def __init__(self,  path, parent=None):
        assert os.path.exists(path), "Path `{}` Not Found".format(path)
        self.path = path
        self.nodes = []
        self.parent = parent

    @property
    def name(self):
        fname = os.path.split(self.path)[-1]
        slices = fname.split('.')
        if len(slices) > 1:
        	return "".join(slices[:-1])
        else:
        	return slices[0]

    def add_node(self, node):
        self.nodes.append(node)

    def walk(self):
        if os.path.isdir(self.path):
            dir_list = os.listdir(self.path)
            add_dir_list = filter(not_ignore, dir_list)
            for d in add_dir_list:
                fpath = os.path.join(self.path, d)
                if os.path.isfile(fpath):
                    self.add_node(FileNode(fpath, parent=self))
                elif os.path.isdir(fpath):
                    self.add_node(DirectoryNode(fpath, parent=self))

            for node in self.nodes:
                node.walk()

    @property
    def level(self):
        me = self
        level = 0
        while me.parent:
            me = me.parent
            level += 1

        return level


class FileNode(Tree):
    pass


class DirectoryNode(Tree):
    pass


class MarkDownRender:
    render_level = {

        0: "#",
        1: "##",
        2: "###",
        3: "####",
    }

    def __init__(self, node):
        self.node = node
        self.lines = []

    def walk(self, lines=None):
    	if lines is None:
    		lines = []
        if self.node.__class__.__name__ == 'FileNode':
            lines.append("- [{}]({})  \n".format(self.node.name,"https://github.com/yowenter/books/blob/master%s"%self.node.path[PREFIX:]))


        elif self.node.__class__.__name__ == 'DirectoryNode':

        	lines.append("{} {}  \n".format(self.render_level.get(self.node.level," "),self.node.name))
        if self.node.nodes:
            for node in self.node.nodes:
            	MarkDownRender(node).walk(lines)

        return lines








if __name__ == "__main__":

    tree = DirectoryNode(git_dir)
    tree.walk()
    md = MarkDownRender(tree)
    readme_path = os.path.join(git_dir,"README.md")
    print readme_path
    if os.path.exists(readme_path):
    	os.system("rm %s"%readme_path)
    with open(readme_path,"w") as f:
    	f.write(HeaderLine)
    	for line in md.walk():
    		f.write(line)
    		f.write("  \n")
        f.write(FooterLine)



