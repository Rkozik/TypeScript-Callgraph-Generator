import os, uuid


class CallingCalledGenerator:
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
            dotFile.write('\t\tlabel="Path: '+the_class.get_path()+'\l Class: ' + the_class_name + '"\n')

            for called_by_class in the_class.get_called_by():
                unique_hash = uuid.uuid4().hex

                calling_method_node = called_by_class[1]+"_"+unique_hash
                class_called_node = called_by_class[0]+"_"+unique_hash

                dotFile.write("\tsubgraph {\n")
                dotFile.write('\t\trankdir="LR;"\n')
                dotFile.write("\t\t" + class_called_node + " [label = \"" + called_by_class[0] + "\" color=cornflowerblue fontcolor=cornflowerblue] \n")
                dotFile.write("\t\t" + calling_method_node + " [label = \"" + called_by_class[1] + "\" color=cornflowerblue fontcolor=cornflowerblue shape=\"box\"] \n")
                dotFile.write("\t\t" + the_class_name + "[label=\"" + the_class_name + "\" color=cornflowerblue style=filled fontcolor=white] \n")
                dotFile.write("\t\tedge[color=cornflowerblue style=dashed] \n")

                dotFile.write(
                    "\t\t"
                    + class_called_node
                    + " -> "
                    + calling_method_node
                    + " [label=<<font color='cornflowerblue'>  '" + called_by_class[0] + "' uses "+called_by_class[1] + "()</font>> dir=none];\n"
                )
                dotFile.write(
                    "\t\t"
                    + calling_method_node
                    + " -> "
                    + the_class_name
                    + " [label=<<font color='cornflowerblue'>  To call " + the_class_name + "</font>>];\n"
                )

                dotFile.write("\t}\n")

            # For the calls we make
            for called_class in the_class.get_calls():
                unique_hash = uuid.uuid4().hex

                calling_method_node = called_class[1] + "_" + unique_hash
                class_called_node = called_class[0] + "_" + unique_hash

                dotFile.write("\tsubgraph {\n")
                dotFile.write('\t\trankdir="LR;"\n')
                dotFile.write("\t\t" + calling_method_node + " [label = \"" + called_class[1] + "\" shape=\"box\"] \n")
                dotFile.write("\t\t" + class_called_node + " [label = \"" + called_class[0] + "\"] \n")
                dotFile.write("\t\t" + the_class_name + "[label=\"" + the_class_name + "\" color=cornflowerblue style=filled fontcolor=white] \n")

                dotFile.write(
                    "\t\t"
                    + the_class_name
                    + " -> "
                    + calling_method_node
                    + " [label=<<font>  '" + the_class_name + "' uses " + called_class[1] + "()</font>> dir=none];\n"
                )
                dotFile.write(
                    "\t\t"
                    + calling_method_node
                    + " -> "
                    + class_called_node
                    + " [label=<<font>  To call " + called_class[0] + "</font>>];\n"
                )

                dotFile.write("\t}\n")

            dotFile.write("}\n")
            dotFile.close()

            output_image = os.path.dirname(__file__)+"/../Export/nodes/" + the_class_name + ".png"
            # output_image = output_name if output_name is not None else "class.png"
            os.system("dot -T png -o " + output_image + " export.dot")
