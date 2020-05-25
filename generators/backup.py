import os, uuid


class CallingCalledUMLGenerator:
    def __init__(self, class_repository):
        self.class_repository = class_repository

    def generate(self):
        for the_class in self.class_repository.get_classes():
            the_class_name = the_class.get_name()

            dotFile = open(os.path.dirname(__file__)+"/../export.dot", "w+")
            dotFile.write("digraph {\n")
            dotFile.write('\t\trankdir="LR;"\n')
            dotFile.write('\t\tlabelloc=t;\n')
            dotFile.write('\t\tlabeljust=l \n')
            dotFile.write('\t\tlabel="Class: ' + the_class_name + '"\n')
            dotFile.write('\t\tnode [shape=record]\n')

            for called_by_class in the_class.get_called_by():
                unique_hash = uuid.uuid4().hex
                calling_method_node = called_by_class[1]+"_"+unique_hash

                dotFile.write("\tsubgraph {\n")
                dotFile.write('\t\trankdir="LR;"\n')

                # called_by_fields_str = "\l "
                # for called_by_fields in self.class_repository.get_class(called_by_class[0]).get_fields():
                #     called_by_fields_str = called_by_fields_str+"+ "+called_by_fields+" \l "
                #
                # called_by_methods_str = "\l "
                # j = 0
                # for called_by_method in self.class_repository.get_class(called_by_class[0]).get_methods():
                #     if called_by_class[1] == called_by_method:
                #         called_by_methods_str = called_by_methods_str[:-3] + "<"+called_by_method+"> + " + called_by_method + "() \l "
                #     else:
                #         called_by_methods_str = called_by_methods_str[:-3] + "|<l_"+str(j)+"> + " + called_by_method + "() \l "
                #         j += 1

                # dotFile.write(
                #     "\t\t"
                #     +called_by_class[0]+" [label = \"{"
                #     +called_by_class[0]+"| "
                #     +called_by_fields_str+"| "
                #     +called_by_methods_str+
                #     "}\" color=cornflowerblue fontcolor=cornflowerblue ]\n"
                # )

                called_by_fields_str = ""
                i = 0
                for called_by_field in self.class_repository.get_class(called_by_class[0]).get_fields():
                    if i < 4:
                        called_by_fields_str = called_by_fields_str + "<tr border='0'><td border='0'>+ "+called_by_field+"</td></tr>"
                    elif i == 4:
                        called_by_fields_str = called_by_fields_str + "<tr border='0'><td border='0'>...</td></tr>"
                    i += 1

                called_by_methods_str = ""
                j = 0
                for called_by_method in self.class_repository.get_class(called_by_class[0]).get_methods():
                    if j < 4 and called_by_class[1] != called_by_method:
                        called_by_methods_str = called_by_methods_str+"<tr border='0'><td border='0' port='"+str(j)+"'>"+called_by_method+"</td></tr>"
                    if j == 4:
                        called_by_methods_str = called_by_methods_str+"<tr border='0'><td border='0' port='"+str(j)+"'>...</td></tr>"
                    if called_by_class[1] == called_by_method:
                        called_by_methods_str = called_by_methods_str+"<tr border='0'><td border='0' port='"+called_by_method.lower()+"'><font color=\"cornflowerblue\">+ "+called_by_method+"()</font></td></tr>"
                    j += 1

                dotFile.write(
                    "\t\tnode[shape=plaintext]\n"
                    + "\t\t" + called_by_class[0] + " [\n"
                    + "\t\tlabel=<\n"
                    + "\t\t<table border='1' cellborder='0'>\n"
                    + "\t\t<tr border='0'><td border='0' bgcolor=\"cornflowerblue\"><font color='white'>" + called_by_class[0] + "</font></td></tr>\n"
                    + "\t\t" + called_by_fields_str + "\n"
                    + "\t\t<tr border='0'><td border='0'>&nbsp;</td></tr>\n"
                    + "\t\t" + called_by_methods_str + "\n"
                    + "\t\t</table>\n"
                    + "\t\t>];\n"
                )

                calling_fields_str = ""
                k = 0
                for calling_field in self.class_repository.get_class(the_class_name).get_fields():
                    if k < 4:
                        calling_fields_str = calling_fields_str + "<tr border='0'><td border='0'>+ "+calling_field+"</td></tr>"
                    elif k == 4:
                        calling_fields_str = calling_fields_str + "<tr border='0'><td border='0'>...</td></tr>"
                    k += 1

                calling_methods_str = ""
                l = 0
                for calling_method in self.class_repository.get_class(the_class_name).get_methods():
                    if called_by_class[1] == calling_method:
                        calling_methods_str = calling_methods_str + "<tr><td><font color='cornflowerblue'>+ " + calling_method + "()</font></td></tr>"
                    elif l < 4:
                        calling_methods_str = calling_methods_str+"<tr><td>+ "+calling_method+"()</td></tr>"
                    elif l == 4:
                        calling_methods_str = calling_methods_str + "<tr><td>...</td></tr>"
                    l += 1

                dotFile.write(
                    "\t\tshape=plaintext\n"
                    + "\t\t" + the_class_name + " [\n"
                    + "\t\tlabel=<\n"
                    + "\t\t<table border='1' cellborder='0'>\n"
                    + "\t\t<tr border='0'><td border='0' bgcolor=\"black\"><font color='white'>" + the_class_name + "</font></td></tr>\n"
                    + "\t\t" + calling_fields_str + "\n"
                    + "\t\t<tr border='0'><td border='0'>&nbsp;</td></tr>\n"
                    + "\t\t" + calling_methods_str + "\n"
                    + "\t\t</table>\n"
                    + "\t\t>];\n"
                )

                # dotFile.write(
                #     "\t\t"
                #     + the_class_name + " [label = \"{"
                #     + the_class_name + "| "
                #     + calling_fields_str + "|"
                #     + calling_methods_str +
                #     "}\" color=cornflowerblue fontcolor=cornflowerblue penwidth=0]\n"
                # )

                dotFile.write("\t\tedge[color=cornflowerblue style=dashed] \n")

                dotFile.write("\t\t" + called_by_class[0] + ":"+called_by_class[1].lower()+" -> " + the_class_name + ";\n")

                dotFile.write("\t}\n")

            # for called_class in the_class.get_calls():
            #     unique_hash = uuid.uuid4().hex
            #     calling_method_node = called_class[1]+"_"+unique_hash
            #
            #     dotFile.write("\tsubgraph {\n")
            #     dotFile.write('\t\trankdir="LR;"\n')
            #
                # calling_fields_str = "\l "
                # for calling_fields in self.class_repository.get_class(called_class[0]).get_fields():
                #     calling_fields_str = calling_fields_str+"+ "+calling_fields+" \l "
                #
                # calling_methods_str = "\l "
                # for calling_methods in self.class_repository.get_class(called_class[0]).get_methods():
                #     calling_methods_str = calling_methods_str + "+ " + calling_methods + "() \l "
            #
            #     called_by_fields_str = "\l "
            #     for called_by_fields in self.class_repository.get_class(the_class_name).get_fields():
            #         called_by_fields_str = called_by_fields_str + "+ " + called_by_fields + " \l "
            #
            #     called_by_methods_str = "\l "
            #     for called_by_methods in self.class_repository.get_class(the_class_name).get_methods():
            #         called_by_methods_str = called_by_methods_str + "+ " + called_by_methods + "() \l "
            #
            #     dotFile.write(
            #         "\t\t"
            #         + the_class_name + " [label = \"{"
            #         + the_class_name + "| "
            #         + called_by_fields_str
            #         + "| "
            #         + called_by_methods_str
            #         + "}\" color=forestgreen fontcolor=forestgreen ]\n"
            #     )
            #     dotFile.write(
            #         "\t\t"
            #         +calling_method_node
            #         +" [label = \""
            #         +called_class[1]
            #         +"\" shape=\"box\"] \n"
            #     )
            #     dotFile.write(
            #         "\t\t"
            #         + called_class[0] + " [label = \"{"
            #         + called_class[0] + "| "
            #         + calling_fields_str
            #         + "| "
            #         + calling_methods_str
            #         + "}\"]\n"
            #     )
            #
            #     dotFile.write("\t\t" + the_class_name + " -> " + calling_method_node + " -> " + called_class[0] + ";\n")
            #     dotFile.write("\t}\n")

            # For the calls we make
            # for called_class in the_class.get_calls():
            #     unique_hash = uuid.uuid4().hex
            #
            #     calling_method_node = called_class[1] + "_" + unique_hash
            #     class_called_node = called_class[0] + "_" + unique_hash
            #
            #     dotFile.write("\tsubgraph {\n")
            #     dotFile.write('\t\trankdir="LR;"\n')
            #     dotFile.write("\t\t" + calling_method_node + " [label = \"" + called_class[1] + "\" shape=\"box\"] \n")
            #     dotFile.write("\t\t" + class_called_node + " [label = \"" + called_class[0] + "\"] \n")
            #     dotFile.write("\t\t" + the_class_name + "[label=\"" + the_class_name + "\" color=cornflowerblue style=filled fontcolor=white] \n")
            #     dotFile.write("\t\t" + the_class_name + " -> " + calling_method_node + " -> " + class_called_node + ";\n")
            #     dotFile.write("\t}\n")

            dotFile.write("}\n")
            dotFile.close()

            output_image = os.path.dirname(__file__)+"/../Export/" + the_class_name + ".png"
            # output_image = output_name if output_name is not None else "class.png"
            os.system("dot -T png -o " + output_image + " export.dot")

