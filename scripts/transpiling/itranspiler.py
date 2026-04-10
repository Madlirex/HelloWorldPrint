from scripts.misc.node import *
from abc import ABC, abstractmethod


class ITranspiler(ABC):
    #region Visits

    #region Basics

    @abstractmethod
    def visit_block(self, node: Block) -> str:
        pass

    @abstractmethod
    def visit_assignment(self, node: Assignment) -> str:
        pass

    @abstractmethod
    def visit_attribute(self, node: Attribute) -> str:
        pass

    @abstractmethod
    def visit_call(self, node: Call) -> str:
        pass

    @abstractmethod
    def visit_index(self, node: Index) -> str:
        pass

    @abstractmethod
    def visit_slice(self, node: Slice) -> str:
        pass

    #endregion

    #region Simple Keywords

    @abstractmethod
    def visit_pass(self) -> str:
        pass

    @abstractmethod
    def visit_continue(self) -> str:
        pass

    @abstractmethod
    def visit_break(self) -> str:
        pass

    @abstractmethod
    def visit_return(self, node: Return) -> str:
        pass

    @abstractmethod
    def visit_yield(self, node: Yield) -> str:
        pass

    @abstractmethod
    def visit_raise(self, node: Raise) -> str:
        pass

    @abstractmethod
    def visit_del(self, node: DelNode) -> str:
        pass

    #endregion

    #region Logical Expressions

    @abstractmethod
    def visit_in(self, node: InNode) -> str:
        pass

    @abstractmethod
    def visit_is(self, node: IsNode) -> str:
        pass

    @abstractmethod
    def visit_or(self, node: OrNode) -> str:
        pass

    @abstractmethod
    def visit_and(self, node: AndNode) -> str:
        pass

    @abstractmethod
    def visit_not(self, node: NotNode) -> str:
        pass

    @abstractmethod
    def visit_operation(self, node: Operation) -> str:
        pass

    #endregion

    #region Data Types

    @abstractmethod
    def visit_none(self, node: NoneNode) -> str:
        pass

    @abstractmethod
    def visit_bool(self, node: Boolean) -> str:
        pass

    @abstractmethod
    def visit_number(self, node: Number) -> str:
        pass

    @abstractmethod
    def visit_string(self, node: String) -> str:
        pass

    @abstractmethod
    def visit_variable(self, node: Variable) -> str:
        pass

    @abstractmethod
    def visit_list(self, node: ListNode) -> str:
        pass

    @abstractmethod
    def visit_tuple(self, node: TupleNode) -> str:
        pass

    @abstractmethod
    def visit_set(self, node: SetNode) -> str:
        pass

    @abstractmethod
    def visit_dict(self, node: DictionaryNode) -> str:
        pass

    @abstractmethod
    def visit_keyarg(self, node: KeyArg) -> str:
        pass

    #endregion

    #region Advanced Keywords

    @abstractmethod
    def visit_if(self, node: IfStatement) -> str:
        pass

    @abstractmethod
    def visit_elif(self, node: tuple[Node, Block]) -> str:
        pass

    @abstractmethod
    def visit_else(self, body: Block) -> str:
        pass

    @abstractmethod
    def visit_while(self, node: While) -> str:
        pass

    @abstractmethod
    def visit_class(self, node: ClassDef) -> str:
        pass

    @abstractmethod
    def visit_function(self, node: FunctionDef) -> str:
        pass

    @abstractmethod
    def visit_try(self, node: TryExcept) -> str:
        pass

    @abstractmethod
    def visit_except(self, node: tuple[Node, Block]) -> str:
        pass

    @abstractmethod
    def visit_for(self, node: ForLoop) -> str:
        pass

    @abstractmethod
    def visit_lambda(self, node: Lambda) -> str:
        pass

    @abstractmethod
    def visit_ternary(self, node: TernaryOp) -> str:
        pass

    @abstractmethod
    def visit_list_comp(self, node: ListComprehension) -> str:
        pass

    @abstractmethod
    def visit_import(self, node: Import) -> str:
        pass

    @abstractmethod
    def visit_from_import(self, node: FromImport) -> str:
        pass

    @abstractmethod
    def visit_match(self, node: MatchNode) -> str:
        pass

    #endregion

    #endregion
