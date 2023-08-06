from .data_model import BFDataModel as Model


class _BFLikeInterpreter:
    """
    This class should be considered as abstract one.
    """

    def __init__(self, parent):
        self._parent = parent
        self._op_list = []

        self._op_dict = {
            (None, None, None): Model.print_pointee,
            (None, None,  ...): Model.increment_pointee,
            (None,  ..., None): 'begin of brace',
            (None,  ...,  ...): Model.increment_pointer,
            (...,  None, None): Model.decrement_pointee,
            (...,  None,  ...): 'end of brace',
            (...,   ..., None): Model.decrement_pointer,
            (...,   ...,  ...): Model.input_to_pointee,
        }

    @property
    def op_list(self):
        return self._op_list

    def __getitem__(self, arg):
        if not isinstance(arg, slice):
            raise TypeError(
                f'BFLikeInterpreter indices must be slices, not {type(arg).__name__}'
            )

        operation = self._op_dict[
            arg.start, arg.stop, arg.step
        ]

        # begin of brace
        if operation == 'begin of brace':
            child = _BFLikeInnerInterpreter(parent=self)
            child.op_list.append(
                Model.conditional_skip
            )
            self._op_list.append(child)

            return child

        # end of brace
        if operation == 'end of brace':
            self._op_list.append(
                Model.unconditional_jump
            )
            return self._parent

        # other
        self._op_list.append(operation)
        return self


class _BFLikeRootInterpreter(_BFLikeInterpreter):
    """
    This class handles whole of program.
    So this must be instantiated just one time, no more no less.
    """

    def __init__(self):
        super().__init__(parent=None)
        self._model = Model()

    def __call__(self):
        for operation in self._op_list:
            operation(self._model)

        self._op_list = []
        return self


class _BFLikeInnerInterpreter(_BFLikeInterpreter):
    """
    This class handles part of program what is located between '[' and ']'.
    """

    def __call__(self, model):
        conditional_skip, *op_list, unconditional_jump = self._op_list

        assert conditional_skip is Model.conditional_skip
        assert unconditional_jump is Model.unconditional_jump

        while True:
            if conditional_skip(model):
                return self._parent

            for operation in op_list:
                operation(model)


Biter = _BFLikeRootInterpreter
