import os


class CallingCalledUMLGenerator:
    def __init__(self, class_repository):
        self.class_repository = class_repository

    def generate(self):
        for the_class in self.class_repository.get_classes():
            for_dot_file = []
            the_class_name = the_class.get_name()

            for_dot_file.append(
                'graph {\n'
                '\tgraph [pad="1"];\n' +
                '\tlabelloc=t;\n' +
                '\tlabeljust=l;\n' +
                '\tlabel="Class: ' + the_class_name + '"\n' +
                '\tnodesep=0.5;\n' +
                '\tnode [shape=plaintext]\n'
            )

            for_dot_file.append("0")

            for_dot_file.append(
                "\t\tnode[shape=plaintext]\n"
                + "\t\t" + the_class_name + " [\n"
                + "\t\tlabel=<\n"
                + "\t\t<table border='1' cellborder='0'>\n"
                + "\t\t<tr border='0'><td border='0' bgcolor=\"cornflowerblue\" port=\"0\"><font color='white'>" + the_class_name + "</font></td></tr>\n"
            )

            called_by_fields_str = ""
            i = 0
            for field_in_class in the_class.get_fields():
                if i < 4:
                    called_by_fields_str = called_by_fields_str + "<tr border='0'><td border='0'>+ "+field_in_class+"</td></tr>"
                elif i == 4:
                    called_by_fields_str = called_by_fields_str + "<tr border='0'><td border='0'>...</td></tr>"
                i += 1

            for_dot_file.append("\t\t" + called_by_fields_str + "\n")
            for_dot_file.append("\t\t<tr border='0'><td border='0' port='blank'>&nbsp;</td></tr>\n")

            called_by_methods_str = ""
            matched_methods = []
            relationships = []
            j = 0
            for class_method in the_class.get_methods():

                for called_by_class in the_class.get_called_by():
                    if called_by_class[1] == class_method:
                        if called_by_class[1] not in matched_methods and called_by_class[0] != the_class_name:
                            called_by_methods_str = called_by_methods_str + "\t\t\t<tr border='0'><td border='0' port='" + \
                                                    called_by_class[1].lower() + "'><font color=\"cornflowerblue\">+ " + \
                                                    called_by_class[1] + "()</font></td></tr>\n"
                            matched_methods.append(called_by_class[1])
                        relationships.append(
                            "\t\t"
                            + called_by_class[0]
                            + ":"
                            + called_by_class[1].lower()
                            + " -- "
                            + the_class_name
                            + ":blank"
                            + " [style=dotted];\n"
                        )
                        break

                for called_class in the_class.get_calls():
                    if called_class[1] == class_method:
                        if called_class[1] not in matched_methods and the_class_name != called_class[0]:
                            called_by_methods_str = called_by_methods_str + "\t\t\t<tr border='0'><td border='0' port='" + \
                                                    called_class[1].lower() + "'><font color=\"cornflowerblue\">+ " + \
                                                    called_class[1] + "()</font></td></tr>\n"
                            matched_methods.append(called_class[1])
                        relationships.append(
                            "\t\t " + the_class_name + ":" + called_class[1].lower() + " -- " + called_class[0] + ":blank [color=cornflowerblue]"
                            + ";\n"
                        )
                        break

                if class_method not in matched_methods:
                    if j < 4:
                        called_by_methods_str = called_by_methods_str+"<tr border='0'><td border='0' port='"+str(j)+"'>+ "+class_method+"()</td></tr>"
                    if j == 4:
                        called_by_methods_str = called_by_methods_str+"<tr border='0'><td border='0' port='"+str(j)+"'>...</td></tr>"
                    j += 1

            for_dot_file.append(
                "\t\t" + called_by_methods_str + "\n"
                + "\t\t</table>\n"
                + "\t\t>];\n"
            )

            matched_classes = []
            for called_by_class in the_class.get_called_by():
                if called_by_class[0] != the_class.get_name() and called_by_class[0] not in matched_classes:

                    for_dot_file.append(
                        "\t\tnode[shape=plaintext]\n"
                        + "\t\t" + called_by_class[0] + " [\n"
                        + "\t\tlabel=<\n"
                        + "\t\t<table border='1' cellborder='0'>\n"
                        + "\t\t<tr border='0'><td border='0' bgcolor=\"black\"><font color='white'>" +
                        called_by_class[0] + "</font></td></tr>\n"
                    )

                    called_by_fields_str = ""
                    i = 0
                    for field_in_class in self.class_repository.get_class(called_by_class[0]).get_fields():
                        if i < 4:
                            called_by_fields_str = called_by_fields_str + "<tr border='0'><td border='0'>+ " + field_in_class + "</td></tr>"
                        elif i == 4:
                            called_by_fields_str = called_by_fields_str + "<tr border='0'><td border='0'>...</td></tr>"
                        i += 1

                    for_dot_file.append("\t\t" + called_by_fields_str + "\n")
                    for_dot_file.append("\t\t<tr border='0'><td border='0' port='blank'>&nbsp;</td></tr>\n")

                    matched_methods = []
                    called_by_methods_str = ""
                    j = 0
                    for called_by_calls in self.class_repository.get_class(called_by_class[0]).get_calls():
                        for called_by_methods in self.class_repository.get_class(called_by_class[0]).get_methods():
                            if called_by_calls[0] == the_class.get_name():
                                if called_by_methods not in matched_methods:
                                    if j < 4:
                                        called_by_methods_str = called_by_methods_str + "<tr border='0'><td border='0' port='" + str(j) + "'>+ " + called_by_methods + "()</td></tr>"
                                    elif j == 4:
                                        called_by_methods_str = called_by_methods_str + "<tr border='0'><td border='0' port='" + str(j) + "'>...</td></tr>"
                                    j += 1
                                if called_by_class[1] not in matched_methods and called_by_class[0] != the_class.get_name():
                                    called_by_methods_str = called_by_methods_str + "\t\t\t<tr border='0'><td border='0' port='" + \
                                                            called_by_class[1].lower() + "'><font color=\"cornflowerblue\">+ " + \
                                                            called_by_class[1] + "()</font></td></tr>\n"
                                    matched_methods.append(called_by_class[1])
                                    relationships.append(
                                        "\t\t" + called_by_class[0] + ":" + called_by_class[1].lower()
                                        + " -- "
                                        + the_class.get_name() + ":blank"
                                        + "[style=dotted];\n"
                                    )

                    for_dot_file.append(
                        "\t\t" + called_by_methods_str + "\n"
                        + "\t\t</table>\n"
                        + "\t\t>];\n"
                    )
                    matched_classes.append(called_by_class[0])

            master_matched_classes = matched_classes
            matched_classes = []
            for called_by_class in the_class.get_calls():
                if called_by_class[0] != the_class.get_name() and called_by_class[0] not in matched_classes:

                    for_dot_file.append(
                        "\t\tnode[shape=plaintext]\n"
                        + "\t\t" + called_by_class[0] + " [\n"
                        + "\t\tlabel=<\n"
                        + "\t\t<table border='1' cellborder='0'>\n"
                        + "\t\t<tr border='0'><td border='0' bgcolor=\"black\"><font color='white'>" +
                        called_by_class[0] + "</font></td></tr>\n"
                    )

                    called_by_fields_str = ""
                    i = 0
                    for field_in_class in self.class_repository.get_class(called_by_class[0]).get_fields():
                        if i < 4:
                            called_by_fields_str = called_by_fields_str + "<tr border='0'><td border='0'>+ " + field_in_class + "</td></tr>"
                        elif i == 4:
                            called_by_fields_str = called_by_fields_str + "<tr border='0'><td border='0'>...</td></tr>"
                        i += 1

                    for_dot_file.append("\t\t" + called_by_fields_str + "\n")
                    for_dot_file.append("\t\t<tr border='0'><td border='0' port='blank'>&nbsp;</td></tr>\n")

                    matched_methods = []
                    called_by_methods_str = ""
                    j = 0
                    for called_by_calls in self.class_repository.get_class(called_by_class[0]).get_called_by():
                        for called_by_methods in self.class_repository.get_class(called_by_class[0]).get_methods():
                            if called_by_calls[0] == the_class.get_name():
                                if called_by_methods not in matched_methods:
                                    if j < 4:
                                        called_by_methods_str = called_by_methods_str + "<tr border='0'><td border='0' port='" + str(
                                            j) + "'>+ " + called_by_methods + "()</td></tr>"
                                    elif j == 4:
                                        called_by_methods_str = called_by_methods_str + "<tr border='0'><td border='0' port='" + str(
                                            j) + "'>...</td></tr>"
                                    j += 1
                                if called_by_class[1] not in matched_methods and called_by_class[0] != the_class.get_name():
                                    called_by_methods_str = called_by_methods_str + "\t\t\t<tr border='0'><td border='0' port='" + \
                                                            called_by_class[
                                                                1].lower() + "'><font color=\"cornflowerblue\">+ " + \
                                                            called_by_class[1] + "()</font></td></tr>\n"
                                    matched_methods.append(called_by_class[1])
                                    relationships.append(
                                        "\t\t" + called_by_class[0]
                                        + ":" + called_by_class[1].lower()
                                        + " -- " + the_class.get_name()
                                        + ":blank"
                                        + "[style=dotted];\n"
                                    )

                    for_dot_file.append(
                        "\t\t" + called_by_methods_str + "\n"
                        + "\t\t</table>\n"
                        + "\t\t>];\n"
                    )
                    matched_classes.append(called_by_class[0])

            matched_classes = set(matched_classes + master_matched_classes)
            matched_classes = list(matched_classes)
            classes = []
            if len(matched_classes) != 0:
                classes = classes + matched_classes[:len(matched_classes)//2]

            classes.append(the_class_name)

            if len(matched_classes) != 0:
                classes = classes + matched_classes[len(matched_classes)//2:]

            rank_same = ""
            for matched_class in classes:
                rank_same = rank_same + " -- " + matched_class

            rank_same = "{rank=same; " + rank_same[4:] + " [color=transparent] rankdir=LR};"

            dotFile = open(os.path.dirname(__file__)+"/../export.dot", "w+")
            for item in for_dot_file:
                if item == "0":
                    dotFile.write("\t\t " + rank_same + "\n")
                    relationships = list(set(relationships))
                    for relationship in relationships:
                        dotFile.write(relationship)
                else:
                    dotFile.write(item)

            dotFile.write("\t}\n")
            dotFile.close()


            output_image = os.path.dirname(__file__)+"/../Export/uml/" + the_class.get_name() + ".png"
            os.system("sfdp -T png -o " + output_image + " export.dot")

