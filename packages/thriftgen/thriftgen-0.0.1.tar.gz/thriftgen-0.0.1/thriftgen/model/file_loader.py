from typing import Optional, cast
import antlr4

from thriftgen.parser.ThriftListener import ThriftListener
from thriftgen.parser.ThriftLexer import ThriftLexer
from thriftgen.parser.ThriftParser import ThriftParser

from .comment_parser import comment_text
from .ThriftyFile import ThriftyFile
from .IFileItem import IFileItem
from .IAttributeHolder import IAttributeHolder
from .ThriftyEnum import ThriftyEnum
from .ThriftyService import ThriftyService
from .ThriftyStruct import ThriftyStruct
from .ThriftyException import ThriftyException
from .ThriftyAttribute import ThriftyAttribute
from .ThriftyType import ThriftyType
from .ThriftyMethod import ThriftyMethod
from .ThrowsHolder import ThrowsHolder


class FileLoader(ThriftListener):
    """
    Loads a Thrifty model from an AST tree.
    """

    def __init__(self, name: str) -> None:
        self.thriftgen_file = ThriftyFile(name)
        # The current_file_item is different than the attribute holder, since
        # in the case of services, the functions are the ones having the
        # attributes, while the current_file_item is still the service.
        self.current_file_item: Optional[IFileItem] = None
        self.attribute_holder: Optional[IAttributeHolder] = None
        self.current_comment: Optional[str] = None

    def enterEnum_rule(self, ctx: ThriftParser.Enum_ruleContext):
        self.current_file_item = ThriftyEnum(str(ctx.IDENTIFIER()))
        self.thriftgen_file.file_items.append(self.current_file_item)

        if self.current_comment:
            # this is set at the beginning of enterEnum_rule
            assert self.current_file_item
            self.current_file_item.comment = self.current_comment
            self.current_comment = None

    def exitEnum_rule(self, ctx: ThriftParser.Enum_ruleContext):
        self.current_file_item = None

    def enterEnum_field(self, ctx: ThriftParser.Enum_fieldContext):
        assert isinstance(self.current_file_item, ThriftyEnum)
        self.current_file_item.values.append(str(ctx.IDENTIFIER()))

    def enterService(self, ctx: ThriftParser.ServiceContext):
        self.current_file_item = ThriftyService(str(ctx.IDENTIFIER(0)))
        self.thriftgen_file.file_items.append(self.current_file_item)

    def exitService(self, ctx: ThriftParser.ServiceContext):
        self.current_file_item = None

    def enterStruct(self, ctx: ThriftParser.StructContext):
        self.current_file_item = ThriftyStruct(str(ctx.IDENTIFIER()))
        self.attribute_holder = self.current_file_item
        self.thriftgen_file.file_items.append(self.current_file_item)

        if self.current_comment:
            # we just set it at the beginning of enterStruct
            assert self.current_file_item
            self.current_file_item.comment = self.current_comment
            self.current_comment = None

    def exitStruct(self, ctx: ThriftParser.StructContext):
        self.current_file_item = None
        self.attribute_holder = None

    def enterException(self, ctx: ThriftParser.ExceptionContext):
        self.current_file_item = ThriftyException(str(ctx.IDENTIFIER()))
        self.attribute_holder = self.current_file_item
        self.thriftgen_file.file_items.append(self.current_file_item)

    def exitException(self, ctx: ThriftParser.ExceptionContext):
        self.current_file_item = None
        self.attribute_holder = None

    def enterField(self, ctx: ThriftParser.FieldContext):
        # if we're entering fields of some sort, they should better
        # be in a context of some sort.
        assert isinstance(self.attribute_holder, IAttributeHolder)

        field_type = ctx.field_type()
        attribute = ThriftyAttribute(str(ctx.IDENTIFIER()),
                                     ThriftyType(field_type.getText()))

        if self.current_comment:
            attribute.comment = self.current_comment
            self.current_comment = None

        self.attribute_holder.attributes.append(attribute)

    def enterFunction(self, ctx: ThriftParser.FunctionContext):
        assert self.current_file_item
        service: ThriftyService = cast(ThriftyService, self.current_file_item)

        method = ThriftyMethod(str(ctx.IDENTIFIER()))

        if self.current_comment:
            method.comment = self.current_comment
            self.current_comment = None

        method.return_type = ThriftyType(ctx.function_type().getText())
        self.attribute_holder = method
        service.methods.append(method)

    def exitFunction(self, ctx: ThriftParser.FunctionContext):
        self.attribute_holder = None

    def enterThrows_list(self, ctx: ThriftParser.Throws_listContext):
        # only methods can throw, so we know we're in a method now, not
        # a struct.
        method: ThriftyMethod = cast(ThriftyMethod, self.attribute_holder)
        self.attribute_holder = ThrowsHolder(method.exceptions)

    def enterDocument(self, ctx: ThriftParser.DocumentContext):
        pass

    def exitDocument(self, ctx: ThriftParser.DocumentContext):
        pass

    def enterComment_singleline(self, ctx: ThriftParser.Comment_singlelineContext):
        pass

    def enterComment_multiline(self, ctx: ThriftParser.Comment_multilineContext):
        self.current_comment = comment_text(ctx.ML_COMMENT().getText())


def load_model_from_file(file_name: str) -> ThriftyFile:
    with open(file_name, 'r', encoding='utf-8') as f:
        lexer = ThriftLexer(antlr4.InputStream(f.read()))

    token_stream = antlr4.CommonTokenStream(lexer)

    parser = ThriftParser(token_stream)

    tree_walker = antlr4.ParseTreeWalker()

    file_loader = FileLoader(name=file_name)
    tree_walker.walk(file_loader, parser.document())

    model = file_loader.thriftgen_file

    return model

