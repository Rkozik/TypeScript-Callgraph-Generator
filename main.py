from extractors.TypeScriptDirectoryExtractor import TypeScriptDirectoryExtractor
from extractors.TypeScriptClassExtractor import TypeScriptClassExtractor
from extractors.TypeScriptClassCallsExtractor import TypeScriptClassCallsExtractor
from directories.FileRepository import FileRepository
from classes.ClassRepository import ClassRepository
from generators.CallingCalledGenerator import CallingCalledGenerator
from generators.CallingCalledUMLGenerator import CallingCalledUMLGenerator
import click


@click.command()
@click.option('--root', default=None, help='Root folder of the TypeScript project.')
@click.option('--uml', default=None, help='The class accessing other classes.')
def main(root, uml):
    if root is None:
        root = "/Users/robertkozik/sites/php2/api/get/ts/"
        # root = '/Users/robertkozik/Downloads/typedoc-master/'

    file_repository = FileRepository()
    class_repository = ClassRepository()

    # Extract all directories
    directory_extractor = TypeScriptDirectoryExtractor(file_repository, root)
    directory_extractor.execute()

    # Extract all classes and methods
    class_extractor = TypeScriptClassExtractor(file_repository, class_repository)
    class_extractor.execute()

    # Extract all class calls
    class_call_extractor = TypeScriptClassCallsExtractor(file_repository, class_repository)
    class_call_extractor.execute()

    # Create dot files
    if uml is None:
        result = CallingCalledUMLGenerator(class_repository)
    else:
        result = CallingCalledGenerator(class_repository)

    result.generate()


if __name__ == '__main__':
    main()
